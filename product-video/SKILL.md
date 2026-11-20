---
name: product-video
description: >
  Produce a recorded video of a product journey in the Splice editor, five
  minutes at most, of one of four types: a product demo, a friction log, a
  tutorial (how-to), or a release clip of 60 seconds or less. Write the
  scenario, storyboard it as beats in Splice, write a script for the screen
  take and a full numbered transcript, record the screen journey and the
  narration (face and voice) separately, then cut the narration into lines,
  lay each on its beat and finish the video with an intro, the person's face
  in frame, fades, click zooms, callouts and persona handoffs. Scenarios,
  scripts and transcripts are kept in the project's docs/videos/ for reuse,
  and each can run against the local stack or staging. Needs the Splice video
  editor and its splice skill. Use when the user asks for a product demo
  video, a friction log video, a recorded walkthrough, a tutorial or how-to
  video, a release or changelog clip, a script or transcript to record, or to
  re-run or re-cut a saved video.
---

# Product video

One person uses the product for real on screen, then narrates it on camera
from a written transcript. You plan before the takes, fill the transcript
between them, and cut after.

```text
0 Type ─> 1 Scenario ─> 2 Storyboard ─> 3 Script and ─> 4 Screen ─> 5 Narration ─> 6 Cut ─> 7 Finish ─> 8 Run file
          repo file     Splice beats    transcript      take        take           lines    intro, zoom,  repo file
                                        repo files     (person)    (person reads)  onto     callouts,
                                                                                   beats    fades
```

Why two takes: the narration is written, so it fits each beat's time and says
exactly what it should. The screen take stays a real use of the product, and
its scratch voice track records what the person noticed.

Load the **splice** skill before step 2. It is the reference for every
`splice ctl` command used here; this skill only says which ones to use and in
what order. Recipes for the intro, persona cards and callout scenes are in
[references/splice-recipes.md](references/splice-recipes.md).

## 0. Choose the type

Ask the person which type before anything else, unless they already said.
The type decides the length, the tone of the transcript, what happens to
waits and failures, the callouts, the ending and the run file.

| | Product demo | Friction log | Tutorial | Release clip |
|---|---|---|---|---|
| For | someone deciding whether the product does what they need | the team, to see where the product costs a user time | a user learning to do one task | anyone following the changelog or social feed |
| Folder | `demos` | `friction-logs` | `tutorials` | `release-clips` |
| Length | 120 to 300 s | up to 300 s | 60 to 300 s | 20 to 60 s |
| Beats | 4 to 9 | 4 to 9 | one per step, 3 to 10 | 3 to 5 |
| Narration | what it does for you, first person, present tense | expected vs. got, plain about what hurt | instructions: "Click Members." | one problem, one change, one result |
| Screen take prompt | **CHECK**: what must be on screen to pass | **NOTICE**: say what you expected and what you got | **CHECK** | **CHECK** |
| Waits | cut, with a "4 min later" label | kept, sped up, labelled with the real time | cut, with a label | cut |
| A failure on camera | stop; fix or retake (a demo shows a clean pass) | keep it; it is the point | stop; fix or retake | stop; fix or retake |
| Callouts | neutral or green, naming a feature | red friction, amber wait, green good moment | numbered step titles; ring on each control clicked | one, on the change |
| Face | hook and close full frame, bubble during the journey | hook and verdict full frame, bubble always | hook and close only | optional; hook only |
| Ends with | a closing line, then an end card with the link to try it | a verdict with three frictions, then an end card listing them | a recap of the steps | the end card: what changed and where to read more |
| Captions | optional | optional | on | on (watched muted) |
| Aspect | 16:9 | 16:9 | 16:9 | 16:9, or 9:16 for social |
| Run file | checks table | frictions table | checks table | checks table |

Rules that hold for every type:

- Never fake a result. Every screen in the video comes from a real run of the
  product. Footage from a second run is labelled ("take 2" in the run file,
  and a dissolve where it joins).
- Cutting a wait is fine where the type allows it; the label says how long it
  really took.
- A demo, tutorial or release clip that fails on camera is not cut around.
  Record the failure in the run file, fix it or report it, and retake the
  whole video from a fresh start (a new thread, a new record) with "take 2".

## Where things live

| What | Where | Committed |
|---|---|---|
| Scenario, script, transcript, run files | `docs/videos/<folder>/<slug>/` | yes |
| Index of videos, environments | `docs/videos/README.md` | yes |
| Splice project, raw takes, exported video | `~/Movies/Splice/videos/<folder>/` | no |

`<folder>` is the type's folder from the table above.

```text
docs/videos/<folder>/<slug>/
  scenario.md              # type, goal, personas, environments, beats (the plan)
  script.md                # what the person does in the screen take
  transcript.md            # every narration line, numbered, read in the narration take
  runs/<date>-<env>.md     # one recording: how it was run, checks or frictions
```

- Slugs are kebab-case and name the journey: `invite-teammate`,
  `thread-handoff-to-agent`.
- Start from `templates/` in this skill. If `docs/videos/README.md` does not
  exist, create it from `templates/README.md`.
- Before writing a new scenario, read `docs/videos/README.md`. If the journey
  exists under any type, reuse it: re-run it, re-cut it as another type, or
  update it.
- Add a row to the README index for each new scenario.
- No secrets, passwords or tokens in any of these files. Name the env var or
  vault item that holds them.

## Choose the mode

| The person wants | Do |
|---|---|
| A new video | Steps 0 to 8 |
| The script and transcript only | Steps 0, 1 and 3 |
| To re-run a saved scenario | Read its files, then steps 2 to 8 |
| The same journey as another type | Copy the scenario to the new type's folder, then steps 1 (adjust) to 8 |
| To re-record only the narration | Step 5, then 6 to 8 |
| To re-cut footage already recorded | Steps 6 to 8 |
| To see what exists | Read `docs/videos/README.md` |

## 1. Scenario

Write `docs/videos/<folder>/<slug>/scenario.md` from the template. Settle
these with the person:

1. **Type.** From step 0.
2. **Goal.** One sentence naming what the user gets done (demo, tutorial,
   friction log) or what changed (release clip).
3. **Personas.** Each has a name, a role, an accent colour and its own browser
   window. Two or more personas means the handoff rules in step 3 and step 7
   apply.
4. **Environment.** Local, staging, or both. See "Environments" below.
5. **Beats.** Each beat has one persona, one user action, what done looks
   like, and a length in seconds. A tutorial's beats are its numbered steps.

Time budget:

| Part | Demo | Friction log | Tutorial | Release clip |
|---|---|---|---|---|
| Intro pre-roll | 4 to 6 | 4 to 6 | 3 to 5 | 0 to 2 |
| Hook | 10 to 15: who I am, what I want | 10 to 15: who I am, what I'm trying to do | 8 to 12: what you'll be able to do | 3 to 6: the problem |
| Journey beats | the rest | 200 to 230 | the rest | the rest |
| Persona cards | about 2 each | about 2 each | about 2 each | none |
| Ending | close, 10 to 15 | verdict, 20 to 30 | recap, 10 to 15 | none |
| End card | 3 to 4 | 3 to 4 | 3 to 4 | 3 to 4 |

- Add the beat lengths up in the scenario file. Over the type's cap means cut
  a beat or split the journey into two slugs. Do not plan to speed-talk.
- Walk the journey yourself first when you can (agent-browser against the same
  environment). You learn how long pages take, what data must exist, and
  where it breaks. If the project already has a written walkthrough of this
  journey, reuse its steps.

### Environments

The scenario lists both environments so the same script runs on either. The
script uses `$APP_URL`; the run picks the value.

#### Research how to run it

Do this before writing beats, for every environment the scenario lists. A
scenario nobody can start is not reusable.

1. Read what is already known: the "Environments" section of
   `docs/videos/README.md` and the "How this was run" section of the latest
   run file for this scenario or a neighbouring one.
2. Fill the gaps from the project, in this order: README, AGENTS.md and
   CLAUDE.md, the project's own skills, service and task-runner config,
   test and synthetic-check config (it usually names the staging URLs), and
   the sign-in route's source.
3. Find, for each environment:
   - the base URL, and for local, how the port is found;
   - the command that starts the stack and how long it takes to be ready;
   - a check that the app answers (health URL or page);
   - how a persona signs in and how its role is set;
   - how the data the journey needs is created;
   - how to reset or clean up afterwards.
4. Try what you can without changing anything: resolve the port, call the
   health check, open the sign-in page. Mark each fact as **checked** (you ran
   it and it worked) or **from docs** (read, not run).
5. Ask the person only for what the project cannot tell you, such as where
   staging test accounts are kept.
6. Write the result in two places:
   - facts that hold for every video go in the "Environments" section of
     `docs/videos/README.md`;
   - facts for this journey (data to create, starting pages, cleanup) go in
     the scenario's Environment section.

Do not guess a URL, a port or a sign-in route. If something could not be
found, write "unknown" with what you tried, and resolve it with the person
before recording.

**Local**

1. The person starts the stack. Do not start it for them.
2. Resolve the URL and ports the way the project documents, and check the
   app answers before recording.
3. Sign each persona in, one browser window per persona. Use the project's
   development sign-in if it has one, and set each persona's role explicitly.
4. Local shows the code in this checkout. Write the commit (`git rev-parse
   --short HEAD`) in the run file.

**Staging**

1. Each persona signs in for real, with a test account kept for this purpose.
   The scenario names where the credentials are kept, not the credentials.
2. Sign in before recording starts, so no password or magic link is on screen.
3. Data made on staging stays there. Name everything the run creates with a
   tag (`vid-<date>`), and list the cleanup in the scenario.
4. Do not change staging infrastructure for a recording.
5. Staging can show other people's data. Note what must be hidden; step 7
   redacts it.
6. Write the date and time (UTC) of the recording in the run file, since
   staging moves.

## 2. Storyboard it in Splice

1. Check Splice (`splice ctl status`). If it is not running, ask the person to
   open it.
2. Make the project: `splice ~/Movies/Splice/videos/<folder>/<slug>-<date>-<env>.splice`
   opens a new, empty project with that name (ask first if the person did not
   ask you to set it up).
3. Confirm `status` names that project and its `duration` is 0. If any other
   project is open, pass `--project <name>` on every command. Never edit a
   project the person did not make or ask for.
4. Set the canvas: `splice ctl canvas --aspect 16:9 --fps 30` (9:16 for a
   vertical release clip).
5. Write the transcript (step 3) first, so the board can carry it. Then add
   one beat per row of the scenario, in order, with its planned length,
   intro and end card included:
   - `--story`: the beat's transcript lines, with their numbers, exactly as in
     `transcript.md`;
   - `--capture`: what the screen take shows, and how the face appears.

   ```sh
   splice ctl story add --title "Hook" --duration 12 \
     --story "L1 I'm Dana, an admin at Acme. I want to invite Sam ..." \
     --capture "Narration camera full frame"
   splice ctl story add --title "Dana · Open members" --duration 30 \
     --story "L2 First, the members page. L3 [after take] ..." \
     --capture "Screen: Settings > Members. Face bubble"
   ```

   Put the persona's name first in every beat title. Lines marked
   `[after take]` are filled in step 5; update the beat's `--story` with
   `story set` then.
6. Add a cue at each persona change: `splice ctl cue add --at 96 --label
   "HANDOFF Dana -> Sam"`.
7. `splice ctl story read`: the beats must end within the type's length. Fix
   the plan in `scenario.md` first, then the board, so the two stay the same.
8. `splice ctl view story` and ask the person to approve the board.

## 3. Script and transcript

Two files. The script is for the screen take; the transcript is everything
the finished video says.

### `script.md`: the screen take

Write it from `templates/script.md`. The person reads it while driving the
product, so it must work at a glance.

- One block per beat: persona, **ANCHOR**, **DO**, then **CHECK** or
  **NOTICE** by type.
- **ANCHOR** is a short line the person says out loud to open the beat, and it
  appears nowhere else in the script ("Next, the members page."). The mic
  records a scratch track; you find beats by these lines in its captions.
- **DO** is the clicks, one per line, with the exact labels on screen.
- **CHECK** (demo, tutorial, release clip): what must be on screen before the
  next beat. If it is not, the person says "fail" and what they see. The take
  doubles as an end-to-end test; the run file records each check.
- **NOTICE** (friction log): a prompt, "Say what you expected here, then what
  you got." The person answers in their own words to the scratch track. These
  reactions are the evidence for the run file and the source for the
  transcript's friction lines. They are not used in the video.

Rules the person follows, printed at the top of the script:

1. Record the journey in one take. Do not stop the recording.
2. Pause for a full second between beats.
3. After a mistake, pause, say "again", and repeat the beat from its anchor
   line. The last attempt is the one kept.
4. While a page loads, keep quiet or say what you are waiting for.
5. At a handoff, say the handoff line, then switch windows.

Handoffs in the script:

- A full-width banner between the beats: `HANDOFF  Dana (admin, window 1) ->
  Sam (member, window 2)`.
- One browser window per persona, each visibly different (profile colour or
  theme), so the footage itself shows who is acting.

### `transcript.md`: the narration

Write it from `templates/transcript.md`. It is every word of the finished
video's voice, in order, as numbered lines.

- Number every line `L1`, `L2`, ... across the whole video; never reuse a
  number. One line is one to three sentences about one thing on screen.
- Group the lines under the beat they play over, with the beat's length and a
  word budget: about 2.2 words per second of the beat, less where the screen
  needs a moment to read (a tutorial: about 1.8). Add the words up per beat;
  over budget means cut words, not speed up the voice.
- Write it the way the person talks: short sentences, first person, no
  marketing words. Read it aloud once; anything that trips gets rewritten.
- Tone by type:
  - **Demo:** what the user does and what it gets them. Name a feature only
    while it is on screen. No claims the footage does not show.
  - **Friction log:** what I expected, what I got, what it cost me.
  - **Tutorial:** instructions in the order they happen, with the exact
    labels on screen ("Click **Members**, then **Invite**.").
  - **Release clip:** one problem, the change, the result. Usually three to
    five lines in all.
- The hook, every handoff, and the ending are lines like any other. A handoff
  line names both people: "That's Dana's side done. Now I'm Sam, a new member,
  opening the invite."
- Where a line depends on what happens in the screen take (how long a wait
  took, a count, what broke, which option the agent offered), write the
  expected line and mark it `[after take]`. A friction log's verdict is
  always `[after take]`.
- Leave room for one extra line per beat for something nobody predicted.

## 4. Screen take

1. Preflight with the person:
   - personas signed in, each in its own window, at the starting page;
   - notifications off, bookmarks bar hidden, unrelated tabs closed;
   - browser zoom at 110 to 125 percent so text reads at 1080p;
   - the script on a second display, a phone or paper, not on the recorded
     display.
2. Set up the take. Read `splice ctl record sources` first and check that
   screen and microphone access are granted. No camera: the face comes from
   the narration take.

   ```sh
   # one persona: record the browser window
   splice ctl record setup --screen window:Chrome --camera none --microphone default \
     --no-system --layout screen --clicks --cursor
   # two or more personas, or a terminal too: record the display
   splice ctl record setup --screen display:1 --camera none --microphone default \
     --no-system --layout screen --clicks --cursor
   ```

3. Ask before starting. Then `splice ctl record start --at 0`.
4. The person runs the script once, start to finish.
5. `splice ctl record stop --wait`. Keep the reply: it lists the screen and
   microphone clips and the take's folder.
6. Mute the scratch track: `splice ctl volume --clip <mic clip> --value 0`.
   Keep it on the timeline; it lines up with the screen and is cut with it.
7. `splice ctl save --label "screen take"`.
8. For a demo, tutorial or release clip: if any CHECK failed, stop here. Tell
   the person what failed with a frame (`splice ctl frame`), and retake once
   it is fixed.

## 5. Narration take

### Fill the transcript from the screen take

1. Transcribe the scratch track: `splice ctl captions --clip <mic clip>
   --wait`, then `splice ctl read`. Find each beat by its anchor line.
2. Look at frames for each beat (`splice ctl frame`). For a friction log, read
   the person's NOTICE reactions and look at the frames where they named a
   problem.
3. Replace every `[after take]` line with what actually happened: real wait
   times, counts, names, and for a friction log what broke and the three
   frictions. Drop lines about things that did not happen; add lines for
   things that did.
4. Check each beat's word budget again, then delete the scratch caption
   clips.
5. Update the board: `story set --beat <id> --story "<lines>"` for each beat
   whose lines changed. Show the person the final transcript and get their
   OK before they read it.

### Record it

1. Set up for camera and voice only:

   ```sh
   splice ctl record setup --screen none --camera default --microphone default \
     --no-system --layout camera --mirror --clean
   ```

   Ask the person to turn on Voice Isolation (`splice ctl record mic-mode`).
   They look at the camera; the transcript sits just under or beside the
   lens. For a type with no face (a release clip without one), use
   `--camera none`.
2. `splice ctl record start --into media`, so the take does not land on the
   timeline yet.
3. Rules for the reading, printed at the top of the transcript:
   1. Say the line's number ("L3"), pause, read the line, pause about two
      seconds.
   2. After a flub, say the number again and reread the whole line. The last
      reading of each number is the one kept.
   3. Read at a relaxed pace. Do not rush to fit a beat; the picture is fitted
      to the voice.
4. `splice ctl record stop --wait`. The take has a camera clip and a
   microphone clip that start together.
5. `splice ctl save --label "narration take"`.

## 6. Cut

### The screen take

1. From the scratch captions (or by scanning `frame`s; every beat starts with
   a click), mark each beat's range in the screen take.
2. Drop the person's own mistakes ("again"), dead air, and the head and tail.
3. Apply the drops from the end of the timeline to the start, so earlier times
   stay valid. Split the screen clip and the scratch mic at the same times and
   delete both pieces with `--ripple`:

   ```sh
   splice ctl split --at 212.4
   splice ctl split --at 219.8
   splice ctl delete --clip 31,32 --ripple
   ```

4. Waits, by type:
   - **Friction log:** waiting is friction. Do not cut a slow load, a spinner
     or an error. Speed it up (`splice ctl speed --clip <piece> --rate 6` on
     the screen piece and the scratch piece; for waits of many minutes, a rate
     that lands it at about 3 s) and label it with the real time ("waited
     14 s").
   - **Demo, tutorial:** keep a second of the working state on each side and
     cut the middle. Put a label on the cut ("4 min later").
   - **Release clip:** cut waits outright.

### The narration

1. Add the narration's camera and mic clips to the timeline after everything
   else (`splice ctl add --media <id>`), on their own tracks.
2. Transcribe the mic clip (`captions --wait`, then `read`). Find every spoken
   line number; keep the last reading of each.
3. Split camera and mic together at each kept line's start and end, keeping
   about 0.2 s of room on each side. Delete the spoken numbers, the retakes
   and the pauses. Delete the caption clips.
4. Each line is now a camera piece and a mic piece of the same length. Move
   both to the line's beat with `splice ctl move --clip <id> --to <t>`, the
   same `--to` for both, starting about 0.3 s after the action the line talks
   about. Never move one without the other.

### Fit the picture to the voice

1. A beat runs as long as its lines plus about a second. If the lines run
   longer than the beat's screen footage, slow a sped-up wait or keep more of
   a pause. If they are much shorter, trim the beat so there is no idle
   screen under silence.
2. `read` after each beat: lines must not overlap each other, and each line
   must sit over the screen it describes. Check with `frame` at each line's
   start.

## 7. Finish

Work in this order. Check each with `splice ctl frame` before the next.

1. **Intro pre-roll.** Use the `Video intro` symbol; make it once from the
   recipe if `splice ctl symbol list` does not have it. Fill its labels: the
   journey, then product · environment · date, then the type's kicker (DEMO,
   FRICTION LOG, HOW-TO, NEW). Make room first by moving the cut to start
   after it. A release clip may skip it and open on the hook.
2. **Face in frame.** The face is the narration's camera pieces, so it shows
   only while a line is spoken. Where the type table says full frame, keep the
   camera piece full frame and hide the screen under it (`look --opacity 0` on
   that screen piece). Elsewhere set each camera piece to a round bubble in a
   corner (`look --scale 0.26 --x 0.36 --y 0.3 --mask ellipse`), or hide it
   where the type has no bubble. Where a bubble covers the control in use,
   move it to another corner.
3. **Click zooms.** `splice ctl zoom --clip <screen piece> --to 1.8` on each
   screen piece (a tutorial: every click; a demo: where text is small).
   Remove the zoom (`--none`) where it hides what the narration is talking
   about, and add a keyframed push-in where it points at something without a
   click. `--none` clears every zoom on that piece; to drop one zoom, split the
   piece around it first.
4. **Callouts.** A see-through scene over the screen: a ring or box on the
   spot, an arrow, and a label of six words at most. Show each for 3.5 s,
   starting as the narration names the thing, where the zoom is steady. Check
   frames at its start, middle and end.
   - **Demo:** a few, neutral or green, naming the feature on screen.
   - **Friction log:** one per friction. Red for friction, green for a good
     moment, amber for a wait.
   - **Tutorial:** a numbered step title at the start of each beat ("2 · Open
     Members"), and a ring on each control as it is clicked.
   - **Release clip:** one, on the change.
5. **Persona handoffs.** At each handoff cue:
   - a full-frame persona card for about 2 s, in the persona's colour, with
     name and role ("Sam · new member");
   - the card on the screen's track, touching the clips before and after it,
     with a `push-left` transition into it and a `dissolve` out of it;
   - a persona badge (name, role, colour) in the top-left corner for the whole
     of every beat, so any paused frame shows who is acting. One-persona
     demos and release clips may leave the badge out;
   - the same colour on that persona's callouts' label background.
6. **Fades.** A `dissolve` from the intro into the hook, `dip-black` between
   major sections, plain cuts inside a beat, a `dissolve` where footage from
   another take joins, and `look --exit fade` on the end card. Sound cannot be
   faded: `volume` is one value per clip. Each line already starts and ends in
   a pause.
7. **Redact.** Blur anything private or not the team's to show: emails of real
   people, tokens, other customers' names (`look --redact blur` on that piece).
8. **Sound.** Narration at 1; the scratch track stays at 0. Music, if any,
   under 0.4 and out of the way of the first line.
9. **Captions**, on for tutorials and release clips, optional otherwise:
   `captions --clip <narration mic pieces>` on the finished cut, then fix
   misheard product names against `transcript.md`.
10. **End card, 3 to 4 s.**
    - Demo: the closing promise in a few words and where to try it.
    - Friction log: the three frictions and where the run file is.
    - Tutorial: the steps as a short list.
    - Release clip: what changed and the changelog link.

Before export:

0. Make the board match the cut. `story remove` the beats from last to first
   (removing an earlier beat pulls later footage left), then `story add` them
   again in order, intro and cards included, with the real lengths and the
   final transcript lines as each beat's `--story`. `read` after the first
   removal: if any clip moved, `undo` and leave the board.
1. `splice ctl status`: `duration` is within the type's length. If it is over,
   shorten waits and pauses first, then drop the weakest beat. Do not speed
   up speech.
2. Export a draft and ask the person to watch it:
   `splice ctl export ~/Movies/Splice/videos/<folder>/<slug>-<date>-<env>-draft.mp4 --draft --wait`.
3. Apply their notes, then export the final with `--high --wait`.
4. You cannot hear the result. Say so, and ask the person to check the voice
   level and the music.

Do not upload or share the video unless the person asks.

## 8. Run file

Write `docs/videos/<folder>/<slug>/runs/<date>-<env>.md` from
`templates/run.md`:

1. Type, environment, commit or recording time, personas, the path of the
   video, and the take number.
2. **How this was run**: the commands and steps actually used, in order, so
   the next person can repeat it without research.
   - starting the stack, or the staging URL;
   - the readiness check;
   - each persona's sign-in, with its role;
   - the data created before recording;
   - the cleanup done afterwards;
   - anything that differed from the README or the scenario, and what failed
     before the working way was found.
   Then correct the README's "Environments" section and the scenario where
   they were wrong.
3. By type:
   - **Demo, tutorial, release clip: checks.** One row per CHECK: beat,
     check, pass or fail, evidence (a link, a time, a frame). A failed check
     names what showed instead.
   - **Friction log: frictions.** Timestamp in the final video, persona, what
     happened, what the person expected, severity (blocker, slows, cosmetic).
     The frictions come from the scratch track's reactions, timed by the line
     that names each one.
4. What worked well, in two or three lines.
5. Anything in the scenario, script or transcript to change for the next run.

Update the scenario's row in `docs/videos/README.md` with the date and
environment of this run.

## Checks before calling it done

1. The video is within the type's length and opens with the intro (or the
   hook, for a release clip).
2. Every transcript line is in the video once, on its beat, with its camera
   and voice together. The face appears as the type table says.
3. No `[after take]` marker is left in `transcript.md`.
4. Every handoff has a card, a spoken line and a badge.
5. Callouts match the type: every friction has one (friction log); every step
   has a title (tutorial).
6. Every cut wait has a label with the real time. A friction log removed no
   waits.
7. No screen in the video comes from anything but a real run; footage from a
   second take is marked.
8. Nothing private is readable in any frame you sampled.
9. `scenario.md`, `script.md`, `transcript.md` and the run file are in
   `docs/videos/<folder>/<slug>/`, and the README index lists the scenario.
10. The run file has "How this was run" with the commands used, and the
    README's "Environments" section agrees with it.
