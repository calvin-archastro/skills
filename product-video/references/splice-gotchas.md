# Splice behaviours that have cost a take or an export

Seen on Splice 0.5.x while making real videos. Each may be fixed in a later
version: confirm with a small test on a saved copy before relying on a
workaround, and remove an entry here once it no longer reproduces.

## Before any large pass

1. `splice ctl save --label "<what you are about to do>"`. A labelled version
   is the only reliable way back.
2. With more than one project window open, pass `--project <name>` on every
   command. A command without it can land on the other project.

## Timeline

1. `speed` on a clip ripples the later clips on its track. Re-read the
   timeline after every speed change and re-check where the narration sits.
2. Changing a beat's duration on the story board can move clips. `read`
   after the change; `undo` if footage moved.
3. Clips that overlap by less than a frame get lifted to another track, and
   clips with a gap of less than a frame will not take a dissolve. Place
   clips on whole-frame times.
4. `import` of a file whose bytes match media already in the project returns
   the existing media. Use the media id from the reply, not an id you
   assumed was new.

## Recording

1. The camera list can be stale until the picker is opened in the app. If
   the expected camera is missing from `record sources`, ask the person to
   open the picker once.
2. A camera may deliver 24 or 25 frames a second into a 30 fps canvas. Set
   the canvas to the camera's rate (see the 5 second sample in step 5).
3. A long take at retina size is large. Stop during waits and watch free
   disk.

## Captions and matching

1. Transcription word times can drift by a second or two on a long take.
   Check the first and last word of every cut line by ear (the person) or
   by the waveform, not only by the reported times.

## Export

1. A full export of a long, caption-heavy project can fail. Export it in
   halves and join the files (ffmpeg's concat), then check the join.
2. An export can show a single wrong frame at a cut. Sample a frame on each
   side of every cut in the exported file, and nudge the cut by a frame
   where one appears.
3. After any export, confirm the file plays to its end and its length
   matches the timeline's.
