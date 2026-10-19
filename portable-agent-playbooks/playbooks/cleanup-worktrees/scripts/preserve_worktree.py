#!/usr/bin/env python3
"""Preserve and verify one Git checkout; never remove its source files."""
import argparse,datetime as dt,hashlib,json,os,shutil,subprocess,tarfile,tempfile
from pathlib import Path

def run(repo,*args,check=True,binary=False):
    cmd=['git','-c','core.hooksPath=/dev/null','-C',str(repo),*args]
    r=subprocess.run(cmd,capture_output=True,text=not binary,timeout=180,env={**os.environ,'GIT_OPTIONAL_LOCKS':'0','GIT_TERMINAL_PROMPT':'0'})
    if check and r.returncode:raise RuntimeError('Git operation failed: '+args[0]+'; inspect locally without exposing private output')
    return r.stdout

def digest(p):
    if p.is_symlink():return 'symlink:'+os.readlink(p)
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def secret_name(name):
    p=Path(name);n=p.name.lower()
    return ((n=='.env' or n.startswith('.env.')) and not any(s in n for s in ('example','sample','template'))) or n.endswith(('.pem','.p12','.pfx','.key')) or n in {'credentials.json','service-account.json','id_rsa','id_ed25519'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--worktree',type=Path,required=True);p.add_argument('--destination',type=Path,required=True);p.add_argument('--history-bundle',type=Path);a=p.parse_args()
    repo=a.worktree.resolve();dest=a.destination.resolve()
    if dest==repo or repo in dest.parents:raise SystemExit('Recovery must be outside the source checkout.')
    if dest.exists():raise SystemExit('Recovery directory already exists; inspect/reuse it instead of overwriting.')
    head=run(repo,'rev-parse','HEAD').strip();branch=run(repo,'symbolic-ref','--quiet','--short','HEAD',check=False).strip()
    status=run(repo,'status','--porcelain=v1','--untracked-files=all')
    tracked=run(repo,'ls-files','-z').split('\0');untracked=[s for s in run(repo,'ls-files','--others','--exclude-standard','-z').split('\0') if s]
    modified=[s for s in run(repo,'diff','--name-only','-z','HEAD').split('\0') if s]
    secret_changes=[s for s in modified+untracked if secret_name(s)]
    if secret_changes:raise SystemExit('Changed/untracked credential files require separate binding preservation: '+', '.join(secret_changes))
    dest.mkdir(parents=True,mode=0o700);os.chmod(dest,0o700)
    manifest={'source':str(repo),'head':head,'branch':branch,'status':status,'created_at':dt.datetime.now(dt.timezone.utc).isoformat(),'files':{},'untracked_files':untracked,'ignored_not_preserved':run(repo,'ls-files','--others','--ignored','--exclude-standard','--directory','--no-empty-directory').splitlines(),'restore_verified':False}
    for name in tracked+untracked:
        if not name:continue
        q=repo/name
        if q.is_symlink() or q.is_file():manifest['files'][name]={'sha256_or_link':digest(q),'mode':q.lstat().st_mode & 0o777}
    if a.history_bundle:
        shared=a.history_bundle.resolve()
        if not shared.is_file():raise RuntimeError('Shared bundle missing')
        heads=run(repo,'bundle','list-heads',str(shared)).splitlines()
        if not any(line.split()[0]==head for line in heads):raise RuntimeError('Shared bundle does not advertise preserved HEAD')
        os.link(shared,dest/'history.bundle')
    else:
        run(repo,'bundle','create',str(dest/'history.bundle'),'HEAD')
    os.chmod(dest/'history.bundle',0o600)
    run(repo,'bundle','verify',str(dest/'history.bundle'))
    for fname,args in [('staged.patch',('diff','--cached','--binary')),('unstaged.patch',('diff','--binary'))]:
        (dest/fname).write_bytes(run(repo,*args,binary=True));os.chmod(dest/fname,0o600)
    with tarfile.open(dest/'untracked.tar.gz','x:gz',dereference=False) as tar:
        for name in untracked:
            # Git paths must not escape this checkout; symlinks are archived as links.
            if Path(name).is_absolute() or '..' in Path(name).parts:raise RuntimeError('Unsafe archive path')
            tar.add(repo/name,arcname=name,recursive=False)
    try:
        with tempfile.TemporaryDirectory(prefix='verify-',dir=dest) as tmp:
            restored=Path(tmp)
            run(restored,'init','--quiet')
            heads=run(repo,'bundle','list-heads',str(dest/'history.bundle')).splitlines()
            fetchref=next(line.split()[1] for line in heads if line.split()[0]==head)
            run(restored,'fetch','--quiet',str(dest/'history.bundle'),fetchref)
            run(restored,'checkout','--quiet','--detach',head)
            for fname,index in [('staged.patch',True),('unstaged.patch',False)]:
                patch=dest/fname
                if patch.stat().st_size:run(restored,'apply',*(['--index'] if index else []),str(patch))
            # Copy only reviewed source untracked paths, then verify tar contents separately.
            with tarfile.open(dest/'untracked.tar.gz','r:gz') as tar:
                members=tar.getmembers()
                for m in members:
                    if Path(m.name).is_absolute() or '..' in Path(m.name).parts:raise RuntimeError('Unsafe archive entry')
                    target=restored/m.name;target.parent.mkdir(parents=True,exist_ok=True)
                    if m.issym():
                        if any(parent.is_symlink() for parent in target.parents if parent!=restored and restored in parent.parents):raise RuntimeError('Archive path traverses a symlink')
                        target.symlink_to(m.linkname)
                    elif m.isfile():
                        if any(parent.is_symlink() for parent in target.parents if parent!=restored and restored in parent.parents):raise RuntimeError('Archive path traverses a symlink')
                        with tar.extractfile(m) as src,target.open('wb') as dst:shutil.copyfileobj(src,dst)
                        os.chmod(target,m.mode)
                    else:raise RuntimeError('Unsupported untracked archive type')
            for name,evidence in manifest['files'].items():
                q=restored/name
                # Git retains the executable bit, but not owner/group read-write
                # permissions. Restore those saved local modes before comparison.
                if q.is_file() and not q.is_symlink():os.chmod(q,evidence['mode'])
                if not (q.is_file() or q.is_symlink()) or digest(q)!=evidence['sha256_or_link'] or q.lstat().st_mode & 0o777!=evidence['mode']:raise RuntimeError('Restored content or mode differs: '+name)
            if run(restored,'status','--porcelain=v1','--untracked-files=all')!=status:raise RuntimeError('Restored Git status differs')
            if run(repo,'rev-parse','HEAD').strip()!=head or run(repo,'status','--porcelain=v1','--untracked-files=all')!=status:raise RuntimeError('Source changed during recovery')
            if any(digest(repo/name)!=evidence['sha256_or_link'] for name,evidence in manifest['files'].items()):raise RuntimeError('Source file changed during recovery')
            manifest['restore_verified']=True
    finally:
        (dest/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');os.chmod(dest/'manifest.json',0o600)
    manifest['artifacts']={q.name:hashlib.sha256(q.read_bytes()).hexdigest() for q in dest.iterdir() if q.is_file() and q.name!='manifest.json'}
    (dest/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({'source':str(repo),'recovery':str(dest),'restore_verified':manifest['restore_verified'],'files':len(manifest['files']),'ignored_not_preserved_count':len(manifest['ignored_not_preserved'])}))

if __name__=='__main__':main()
