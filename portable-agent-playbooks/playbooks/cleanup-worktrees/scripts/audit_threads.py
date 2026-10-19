#!/usr/bin/env python3
"""Read-only worktree ownership and actual message-date audit."""
import argparse,datetime as dt,json,sqlite3,re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

def last_message(path):
    p=Path(path)
    if not p.is_file():return None
    size=p.stat().st_size;limit=1024*1024
    while True:
        start=max(0,size-limit)
        with p.open('rb') as f:f.seek(start);lines=f.read().splitlines()
        if start:lines=lines[1:]
        dates=[]
        for raw in lines:
            try:
                item=json.loads(raw);q=item.get('payload',{})
                if item.get('type')=='response_item' and q.get('type')=='message' and q.get('role') in ('user','assistant'):
                    dates.append(dt.datetime.fromisoformat(item['timestamp'].replace('Z','+00:00')).timestamp())
            except (ValueError,KeyError,TypeError):continue
        if dates:return max(dates)
        if not start or limit>=128*1024*1024:return None
        limit*=4

def contains_path(path,root):
    p=Path(path)
    if not p.is_file():return False
    needle=str(root).encode();carry=b''
    with p.open('rb') as f:
        while chunk:=f.read(1024*1024):
            data=carry+chunk
            if needle in data:return True
            carry=data[-len(needle):]
    return False

def main():
    a=argparse.ArgumentParser();a.add_argument('--root',type=Path,default=Path.home()/'.codex/worktrees');a.add_argument('--days',type=float,default=30);a.add_argument('--database',type=Path);a.add_argument('--output',type=Path,required=True);args=a.parse_args()
    if args.days<=0:a.error('--days must be positive')
    databases=sorted((Path.home()/'.codex').glob('state_*.sqlite'),key=lambda p:int(re.search(r'state_(\d+)',p.name)[1]),reverse=True)
    database=args.database or (databases[0] if databases else None)
    if not database:raise SystemExit('Local metadata unavailable; use app tools and preserve unknown ownership.')
    conn=sqlite3.connect('file:'+str(database)+'?mode=ro',uri=True)
    cols={r[1] for r in conn.execute('pragma table_info(threads)')}
    if not {'id','cwd','rollout_path','updated_at','archived'}<=cols:raise SystemExit('Unsupported metadata schema; use app tools.')
    threads={r[0]:dict(zip(('id','cwd','rollout','metadata_updated_epoch','archived'),r)) for r in conn.execute('select id,cwd,rollout_path,updated_at,archived from threads')}
    attachments=[]
    if conn.execute("select 1 from sqlite_master where name='thread_attachments'").fetchone():
        for tid,identity,payload in conn.execute("select thread_id,identity_key,payload from thread_attachments where attachment_type='worktree'"):
            try:p=json.loads(payload)
            except ValueError:p={}
            attachments.append((tid,[identity,p.get('root'),p.get('workspaceRoot')]))
    conn.close();now=dt.datetime.now(dt.timezone.utc);cutoff=now.timestamp()-args.days*86400
    rows=[];ownerids=set()
    for root in sorted(p for p in args.root.iterdir() if p.is_dir() and not p.is_symlink()):
        owners={};prefix=str(root)+'/'
        for tid,t in threads.items():
            if t['cwd']==str(root) or t['cwd'].startswith(prefix):owners.setdefault(tid,[]).append('exact chat cwd')
        for tid,paths in attachments:
            if any(s and (s==str(root) or s.startswith(prefix)) for s in paths):owners.setdefault(tid,[]).append('app worktree attachment')
        if root.name in threads and contains_path(threads[root.name]['rollout'],root):owners.setdefault(root.name,[]).append('chat UUID folder and exact history path')
        ownerids.update(owners);rows.append({'path':str(root),'folder':root.name,'owner_evidence':owners})
    def activity(tid):
        t=threads.get(tid)
        if not t:return tid,None
        try:return tid,last_message(t['rollout'])
        except OSError:return tid,None
    with ThreadPoolExecutor(max_workers=4) as pool:dates=dict(pool.map(activity,ownerids))
    for row in rows:
        row['owners']=[]
        for tid,evidence in row['owner_evidence'].items():
            t=threads.get(tid,{});epoch=dates.get(tid)
            row['owners'].append({'id':tid,'evidence':evidence,'last_message_epoch':epoch,'last_message_utc':dt.datetime.fromtimestamp(epoch,dt.timezone.utc).isoformat() if epoch else None,'metadata_updated_epoch':t.get('metadata_updated_epoch'),'archived':t.get('archived')})
        if not row['owners']:row['classification']='OWNER_UNKNOWN'
        elif any(t['last_message_epoch'] is None for t in row['owners']):row['classification']='ACTIVITY_UNKNOWN'
        elif all(t['last_message_epoch']<cutoff for t in row['owners']):row['classification']='INACTIVE_CANDIDATE'
        else:row['classification']='RECENT_MESSAGE'
    report={'observed_at':now.isoformat(),'cutoff_days':args.days,'cutoff_utc':dt.datetime.fromtimestamp(cutoff,dt.timezone.utc).isoformat(),'root':str(args.root),'rows':rows,'note':'Candidates still require live app state, other task/automation ownership, code recovery and credential review before removal.'}
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n')
    from collections import Counter
    print(json.dumps({'folders':len(rows),'classification_counts':dict(Counter(r['classification'] for r in rows)),'inactive':[r['folder'] for r in rows if r['classification']=='INACTIVE_CANDIDATE'],'report':str(args.output)}))

if __name__=='__main__':main()
