# Mac capture and editing setup

These are tested operational lessons from the September 2026 FCA workflow, not permanent device or dependency assumptions.

## Capture

Use the authorized computer-control tool for UI interaction. FFmpeg recording requires authorization when the active computer-control rules restrict alternative capture methods. The FCA session explicitly authorized it; that does not grant permission for unrelated future sessions.

On the tested Mac, the external DELL display was `Capture screen 0`, 1920×1080. Reconfirm the display before capture. AVFoundation numeric device indices changed when a phone camera disconnected; prefer the verified screen device name.

Example after verifying the target display and choosing a new output filename:

```sh
ffmpeg -hide_banner -loglevel error \
  -f avfoundation -framerate 30 -pixel_format uyvy422 -capture_cursor 1 \
  -i 'Capture screen 0:none' -t 45 -an -r 30 \
  -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p \
  test-recording.mp4
```

- Keep `-t` bounded. `none` and `-an` prevent microphone/audio capture; narration is added later.
- Keep explicit output `-r 30`; input timing alone produced misleading frame-rate behavior.
- Use an interactive terminal session if early stopping with `q` is needed; otherwise let the bounded capture finalize normally.
- Do not directly launch `com.apple.screencaptureui` on this setup: it produced repeated “application can't be opened” dialogs. Use the proven authorized capture path instead.
- Check fullscreen framing and hide browser sidebar/address history before recording. Do not use a crop to claim that an unintended capture never happened; retain originals privately and share only clean cuts.
- Refresh accessibility state after UI actions. Some Arc AX clicks focus controls without activating them; inspect the result before another action. Never blindly press Return after Send or Download. Downloads can succeed without a visible AX change.
- In the embedded PDF viewer, thumbnail clicks were reliable. Setting a page/zoom field without focus then pressing Return could send the keystroke into chat. Focus the actual field or use visible buttons/thumbnails.

## Existing reusable implementation

The established local project is `/Users/preston/Code/bonfire-video-studio`. Inspect current status before editing and preserve unrelated changes. Look for `remotion/compositions/FcaDemo.tsx`, composition registration, `fca/` timeline manifests, and `public/fca/` media. Reuse the composition and manifest pattern when it fits rather than rebuilding a video engine.

The September 2026 implementation used Remotion 4.0.464 and React 19.2.6. Read current lockfiles before installing or upgrading. Confirm current Remotion license eligibility; the user reported a two-person company during the FCA project.

Use real `OffthreadVideo` clips with scene audio, timed captions, and purposeful annotations. Make holds and compressed waits deliberate. Keep filenames, clip offsets, narration timing, and export settings in a manifest so small changes only require affected scenes to be regenerated.

A typical render, adjusted to the existing entrypoint and composition:

```sh
pnpm exec remotion render remotion/index.ts FcaDemo review-render.mp4 \
  --props=fca/sample.json --codec=h264 --crf=18 --concurrency=4
```

Final processing can use H.264 video, 48 kHz AAC, faststart, and loudness normalization targeting roughly -16 LUFS with -1.5 dBTP. Prefer measured two-pass normalization for a final delivery master. Preserve a pre-normalized render and verify the actual final file.

Inspect with `ffprobe`, decode the complete output with FFmpeg, and inspect frames at scene boundaries as well as within scenes. A successful render or transcript match is not a listening review.

- Verify exact source timestamps at important cuts. Low-frequency contact sheets can sample between nominal intervals; do not infer precise transitions solely from their grid position. Check the actual frame where narration names a result.
- Distinguish labels for accelerated navigation ("Time shortened") and real processing waits ("Processing time shortened"). Insert short sentence-boundary pauses when narration would otherwise announce a result before it appears.
