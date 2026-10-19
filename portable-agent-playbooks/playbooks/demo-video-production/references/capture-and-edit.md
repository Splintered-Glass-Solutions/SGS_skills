# Capture and Edit

## Select a capture surface

Use the available authorized capture tool for the current operating system.
Verify the exact browser/profile, window and display with a short preview.
Do not assume a monitor name, device index, resolution or previous permission.
Pause if the chosen tool cannot isolate the authorized surface.

On macOS, FFmpeg AVFoundation is one optional capture path. Inspect available
devices and the installed tool's help before selecting a device. A bounded example,
after replacing the verified screen input and choosing a fresh filename:

```sh
ffmpeg -hide_banner -loglevel error \
  -f avfoundation -framerate 30 -capture_cursor 1 \
  -i "$VERIFIED_SCREEN_INPUT" -t 45 -an -r 30 \
  -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p \
  review-capture.mp4
```

`VERIFIED_SCREEN_INPUT` must select the approved screen without microphone audio.
Verify that the local FFmpeg build accepts these options. On other platforms use
an equivalent authorized recorder. Stop if capture permissions are unavailable.
Check output framing, resolution and frame rate before the full recording.

## Reuse the project editor

Inspect the current checkout and preserve unrelated work. Discover composition
registration, scene manifests and media folders instead of assuming a local path.
Read lockfiles before installation or upgrades and verify applicable licensing.

For Remotion, keep real video clips, scene audio, captions and annotations in a
manifest so narrow edits regenerate only affected scenes. A typical render,
adjusted to the project's actual entrypoint and composition:

```sh
pnpm exec remotion render remotion/index.ts Demo review-render.mp4 \
  --props=demo/sample.json --codec=h264 --crf=18 --concurrency=4
```

Verify installed CLI options and choose concurrency for available resources.
Use another existing editor if Remotion is absent; report missing capabilities.

## Validate the result

Keep capture private until clean framing is confirmed. Use H.264 video, AAC audio
and faststart when the destination supports them. Choose loudness to match the
delivery specification; a common web-video target is about -16 LUFS and -1.5 dBTP.
Keep the pre-normalized render and use measured normalization for final delivery.

Inspect with `ffprobe`, decode the complete output with FFmpeg, listen to the final
audio and inspect frames at scene boundaries and when narration names a result.
Label accelerated navigation and shortened processing accurately. Verify captions
after all timing edits. A successful render does not establish correctness,
accessibility, licensing or user acceptance.
