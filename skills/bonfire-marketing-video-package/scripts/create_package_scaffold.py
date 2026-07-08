#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "feature"


def title(value: str) -> str:
    return value.strip() or "Bonfire Feature"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(content)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--feature", required=True, help="Human-readable feature name")
    parser.add_argument("--root", required=True, help="Local output root")
    parser.add_argument(
        "--date",
        default=dt.date.today().isoformat(),
        help="Package date, default today",
    )
    args = parser.parse_args()

    feature = title(args.feature)
    slug = slugify(feature)
    package_name = f"{feature} - Marketing Package - {args.date}"
    package_dir = Path(args.root).expanduser().resolve() / package_name

    package_dir.mkdir(parents=True, exist_ok=True)
    for subdir in [
        "static-screenshots",
        "raw-assets",
        "renders",
        "remotion/src",
        "remotion/public",
    ]:
        (package_dir / subdir).mkdir(parents=True, exist_ok=True)

    write(
        package_dir / "marketing-one-pager.md",
        f"""# {feature} Marketing One-Pager

## Live Status

TODO: local/dev/production/unknown, with proof and caveat.

## One-Sentence Positioning

TODO: Explain the user-facing value in one sentence.

## User Problem

TODO

## What Changed

TODO

## Why It Matters

TODO

## Who It Helps

TODO

## Before And After

TODO

## Suggested Marketing Angles

TODO

## Example Copy

TODO

## Visual And Demo Ideas

TODO

## Static Screenshot Ideas

TODO: Name 3-6 still-image assets the marketing team should use.

## Proof And Source Evidence

TODO

## Claims To Avoid

TODO
""",
    )

    write(
        package_dir / "copy-bank.md",
        f"""# {feature} Copy Bank

## Headlines

1. TODO

## Short Social Posts

1. TODO

## Email Or Newsletter Blurbs

1. TODO

## Website Or Product Blurbs

1. TODO

## Video Captions

1. TODO

## Calls To Action

1. TODO
""",
    )

    write(
        package_dir / "video-brief.md",
        f"""# {feature} Video Brief

## Audience

TODO

## Key Message

TODO

## Target Length

TODO: 20-45 seconds by default.

## Story Arc

1. Problem opener
2. Feature reveal
3. Demo beats
4. Outcome/value statement
5. CTA

## Shot List

1. TODO

## Voiceover Draft

TODO

## On-Screen Text

1. TODO

## Asset List

1. TODO

## Static Screenshot List

1. TODO
""",
    )

    write(
        package_dir / "usage-guide.md",
        f"""# {feature} Usage Guide

## Recommended Channels

TODO

## Suggested Rollout Order

TODO

## Recommended Edits Before Publishing

TODO

## Approval Or Verification Needed

TODO

## Status Caveats

TODO
""",
    )

    write(
        package_dir / "asset-manifest.md",
        f"""# {feature} Asset Manifest

| File | Source | What It Shows | Environment | Caveat |
| --- | --- | --- | --- | --- |
| TODO | TODO | TODO | TODO | TODO |
""",
    )

    write(
        package_dir / "static-screenshots/README.md",
        f"""# Static Screenshot Assets For {feature}

Place selected, presentation-ready still images here. Use this folder for clean screenshots that marketing can drop into social posts, website sections, sales notes, decks, and internal enablement.

Keep raw or uncropped captures in ../raw-assets/. Record each selected screenshot in screenshot-captions.md and ../asset-manifest.md.
""",
    )

    write(
        package_dir / "static-screenshots/screenshot-captions.md",
        f"""# {feature} Screenshot Captions

| File | Caption | Alt Text | Recommended Use | Environment | Caveat |
| --- | --- | --- | --- | --- | --- |
| TODO | TODO | TODO | TODO | TODO | TODO |
""",
    )

    write(
        package_dir / "raw-assets/README.md",
        f"""# Raw Assets For {feature}

Place screenshots, screen recordings, image assets, exported JSON, and other source media here. Record each item in ../asset-manifest.md.
""",
    )

    write(
        package_dir / "renders/README.md",
        f"""# Rendered Videos For {feature}

Place rendered MP4/WebM files here. The default final draft path should be feature-video-draft.mp4 when rendering succeeds.
""",
    )

    write(
        package_dir / "remotion/package.json",
        """{
  "scripts": {
    "studio": "remotion studio",
    "render": "remotion render FeatureVideo ../renders/feature-video-draft.mp4"
  },
  "dependencies": {
    "@remotion/cli": "latest",
    "remotion": "latest",
    "react": "latest",
    "react-dom": "latest"
  },
  "devDependencies": {
    "typescript": "latest"
  }
}
""",
    )

    write(
        package_dir / "remotion/src/index.ts",
        """import {registerRoot} from 'remotion';
import {Root} from './Root';

registerRoot(Root);
""",
    )

    write(
        package_dir / "remotion/src/data.ts",
        f"""export const feature = {{
  name: {feature!r},
  slug: {slug!r},
  positioning: 'TODO: one-sentence user value',
  beats: [
    'TODO: problem opener',
    'TODO: feature reveal',
    'TODO: demo beat',
    'TODO: outcome statement',
  ],
}};
""",
    )

    write(
        package_dir / "remotion/src/Root.tsx",
        """import React from 'react';
import {Composition} from 'remotion';
import {FeatureVideo} from './FeatureVideo';

export const Root: React.FC = () => (
  <Composition
    id="FeatureVideo"
    component={FeatureVideo}
    durationInFrames={900}
    fps={30}
    width={1080}
    height={1920}
  />
);
""",
    )

    write(
        package_dir / "remotion/src/FeatureVideo.tsx",
        """import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {feature} from './data';

export const FeatureVideo: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const scale = spring({frame, fps, config: {damping: 18, stiffness: 90}});
  const beatIndex = Math.min(feature.beats.length - 1, Math.floor(frame / 170));
  const opacity = interpolate(frame % 170, [0, 20, 140, 169], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill
      style={{
        background: '#0f172a',
        color: '#f8fafc',
        fontFamily: 'Inter, Arial, sans-serif',
        padding: 72,
        justifyContent: 'center',
      }}
    >
      <div style={{fontSize: 34, color: '#7dd3fc', marginBottom: 28}}>Bonfire Feature</div>
      <div style={{fontSize: 76, fontWeight: 800, lineHeight: 1.02, transform: `scale(${scale})`}}>
        {feature.name}
      </div>
      <div style={{height: 36}} />
      <div style={{fontSize: 42, lineHeight: 1.22, opacity}}>{feature.beats[beatIndex]}</div>
      <div style={{height: 64}} />
      <div style={{fontSize: 28, color: '#cbd5e1', lineHeight: 1.35}}>{feature.positioning}</div>
    </AbsoluteFill>
  );
};
""",
    )

    print(package_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
