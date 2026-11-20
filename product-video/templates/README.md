# Product videos

Recorded videos of product journeys: demos, friction logs, tutorials and
release clips. Each is recorded in two takes, the screen journey and then the
narration read on camera from a written transcript. Each journey keeps its
scenario, script and transcript here so it can be recorded again on another
environment, after a fix, or as another type.

The `product-video` skill writes and uses these files.

## Layout

```text
docs/videos/<type>/<slug>/     # demos, friction-logs, tutorials, release-clips
  scenario.md              # goal, personas, local and staging setup, beats
  script.md                # what the person does in the screen take
  transcript.md            # every narration line, numbered
  runs/<date>-<env>.md     # one recording: checks or frictions
```

- Videos and Splice projects are not committed. They are in
  `~/Movies/Splice/videos/<type>/` on the machine that recorded them; each
  run file gives the path or link.
- No passwords, tokens or magic links in these files. Name the env var or
  vault item.

## Environments

| Product | Local | Staging |
|---|---|---|
| <app> | <URL, and how the port is found> | <URL> |

- Start the local stack: <command>.
- Local sign-in for a persona: <route or steps, with how the role is set>.
- Staging sign-in: <where test accounts are kept>.

## Videos

| Type | Slug | Journey | Product | Personas | Last recorded |
|---|---|---|---|---|---|
| | | | | | |
