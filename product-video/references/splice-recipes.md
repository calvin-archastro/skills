# Splice recipes for product videos

Each recipe names the `splice ctl` commands to run. Clip and media ids come
from the replies; read them, do not guess. The scene files are in
`<skill dir>/assets/`, where `<skill dir>` is the directory this skill is
installed in (the parent of this file's directory),
and pass `splice ctl scene check`. Preview one without a project:

```sh
splice --still <skill dir>/assets/persona-card.json /tmp/card.png --size 1920x1080 --at 1.5
```

## Intro symbol (make once, reuse in every video)

`splice ctl symbol list` shows whether `Video intro` exists. (An older
`Friction log intro` has a fixed red kicker; make `Video intro` anyway.) To make it,
ask the person for a new empty scratch project and work only there (these
clips go at 0 and would land on top of a take):

```sh
splice ctl color --color "#101216" --at 0 --duration 5 --track 1
splice ctl text --text "Invite a teammate" --at 0.3 --duration 4.7 --track 2 \
  --size 96 --bold --y -0.04 --animate rise --by word --over 0.6 --exit fade
splice ctl text --text "Acme app · staging · 2026-11-20" --at 0.9 --duration 4.1 --track 3 \
  --size 38 --color "#ffffffb3" --y 0.09 --enter fade --exit fade
splice ctl text --text "DEMO" --at 0.1 --duration 4.9 --track 4 \
  --size 28 --bold --color "#ffffffcc" --y -0.16 --enter fade --exit fade
splice ctl symbol make --clip <colour>,<title>,<subtitle>,<kicker> --name "Video intro" --wait
```

The titles become placeholders named `Title`, `Title 2`, `Title 3`, `Title
4`. Run `splice ctl symbol read --name "Video intro"` to see which label holds
which line before filling them. The kicker takes the type: DEMO, FRICTION LOG,
HOW-TO or NEW.

Use it:

```sh
splice ctl symbol add --name "Video intro" --at 0 --wait
splice ctl symbol fill --clip <use> --label Title --text "Invite a teammate" --wait
splice ctl symbol fill --clip <use> --label "Title 2" --text "Acme app · local · 2026-11-20" --wait
splice ctl symbol fill --clip <use> --label <kicker's label> --text "FRICTION LOG" --wait
```

Make room for it first: every clip of the cut moves right by the intro's
length. Move the clips from last to first so none collides.

## Persona card (one scene per persona)

```sh
splice ctl scene new --file <skill dir>/assets/persona-card.json --duration 2 --opaque \
  --name "Card Sam" --at <handoff time> --track <screen track> --wait
splice ctl scene patch --media <card> --layer name --json '{"text": "Sam"}' --wait
splice ctl scene patch --media <card> --layer role --json '{"text": "New member at Acme"}' --wait
splice ctl scene patch --media <card> --layer band --json '{"fill": "#2f6fed"}' --wait
splice ctl transition --clip <card clip> --kind push-left --for 0.4
splice ctl transition --clip <first clip after the card> --kind dissolve --for 0.4
```

- The card takes 2 s of its own: open a 2 s gap at the handoff on every
  layer, then place the card in the gap on the screen's track. It must touch
  the screen clips on both sides; a transition with nothing just before it on
  the same track comes in from black instead.
- A patch changes every clip of that scene, so each persona needs its own
  scene. To show the same persona again later, `add --media <card>` again.

Persona colours. Keep one colour per persona for the whole video:

| Order | Colour |
|---|---|
| First persona | `#2f6fed` blue |
| Second | `#8e4ec6` purple |
| Third | `#12a594` teal |

Red, green and amber are for callouts; do not give them to a persona.

## Persona badge (on screen for every beat)

```sh
splice ctl scene new --file <skill dir>/assets/persona-badge.json --duration <beat length> \
  --name "Badge Sam" --at <beat start> --wait
splice ctl scene patch --media <badge> --layer who --json '{"text": "Sam · member"}' --wait
splice ctl scene patch --media <badge> --layer chip --json '{"fill": "#2f6fed"}' --wait
```

Put badges on a track above the screen and camera. If the badge covers the
product's own header, move the chip's `x` and `y`, the same way for every
persona.

## Callout

```sh
splice ctl scene new --file <skill dir>/assets/annotation-callout.json --duration 3.5 \
  --name "Note 02 no feedback" --at <time> --wait
splice ctl scene patch --media <note> --layer words --json '{"text": "No feedback after click"}' --wait
splice ctl scene patch --media <note> --layer ring --json '{"x": "71%", "y": "33%", "width": 260, "height": 90}' --wait
splice ctl scene patch --media <note> --layer arrow --json '{"x": "71%", "y": "33%"}' --wait
splice ctl scene sheet --media <note> /tmp/note.png
splice ctl frame <time + 1.5> /tmp/note-over.png
```

- Find the spot from a frame: take `splice ctl frame <time>`, measure the
  control's centre as a fraction of the picture, and use those percentages.
- The arrow's `from` and `to` are offsets from the ring's centre. Keep the
  label clear of the camera bubble and the persona badge.
- Colours: friction `#e5484d`, good moment `#30a46c`, wait `#f5a524`. Change
  `stroke` on `ring`, `arrow` and `label` together.
- A wait label needs no ring: remove `ring` and `arrow` and set the text to
  the real time, for example "waited 14 s".
- If the screen clip has zoom keyframes during the annotation, the spot moves.
  Start the annotation after the zoom settles, or remove that zoom.

## Camera: bubble and full frame

The narration's camera pieces come in full frame (the `camera` layout). Each
one has a mic piece of the same length at the same time; change the camera
piece's `look` freely, but move both together.

```sh
# a journey line: round bubble, bottom right
splice ctl look --clip <camera piece> --scale 0.26 --x 0.36 --y 0.3 --mask ellipse --feather 0.02
# the bubble covers the control in use: top right for this line
splice ctl look --clip <camera piece> --x 0.36 --y -0.32
# hook and verdict: keep it full frame and hide the screen under it
splice ctl look --clip <screen piece> --opacity 0
```

Hiding a whole track hides it for the whole movie. For one section, split the
screen clip there and set that piece's opacity to 0.

## Push in on a detail (no click there)

```sh
splice ctl keyframe --clip <screen piece> --at 48.0 --scale 1 --x 0 --y 0
splice ctl keyframe --clip <screen piece> --at 48.8 --scale 1.6 --x -0.18 --y 0.12 --ease in-out
splice ctl keyframe --clip <screen piece> --at 53.0 --scale 1.6 --x -0.18 --y 0.12
splice ctl keyframe --clip <screen piece> --at 53.8 --scale 1 --x 0 --y 0
```

To centre a spot at fraction (fx, fy) of the picture at scale s, set
`--x (0.5 - fx) * s` and `--y (0.5 - fy) * s`. Check with `frame`.

## A shortened wait

```sh
splice ctl split --at <wait start>
splice ctl split --at <wait end>
splice ctl speed --clip <screen piece> --rate 6
splice ctl speed --clip <scratch mic piece> --rate 6   # it stays muted
```

Do this before laying the narration in. `speed` moves later clips on its own
track only, so the screen and scratch pieces need the same rate. After it, `read` and check that every section still lines up,
then add the wait label over the shortened piece.
