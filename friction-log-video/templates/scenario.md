# <Journey title>

| | |
|---|---|
| Slug | `<slug>` |
| Product | <which app> |
| Runs on | local, staging |
| Planned length | <sum> s of 300 |
| Last recorded | never |

## Goal

<One sentence: what the user is trying to get done.>

## Personas

| Name | Role | Colour | Window | Local sign-in | Staging account |
|---|---|---|---|---|---|
| Dana | Admin at Acme | `#2f6fed` | 1 | `dana@example.test`, admin | vault item `<name>` |
| Sam | New member | `#8e4ec6` | 2 | `sam@example.test`, member | vault item `<name>` |

## Environment

Each line is marked **checked** (run and it worked) or **from docs** (read,
not run). Shared facts are in `../README.md` under "Environments".

### Local

- Start: <the command the person runs>.
- `APP_URL`: <local URL, and how the port is found>.
- Sign-in: <the development sign-in for a persona, with its role>.
- Data to create before recording: <list, with the command or page for each>.

### Staging

- `APP_URL`: <staging URL>
- Sign-in: real sign-in, before recording starts.
- Tag for anything created: `fl-<date>`.
- Hide in the edit: <emails, other customers' names, tokens>.
- Cleanup after recording: <what to delete, and where>.

## Preconditions

1. <What must be true before beat 1: accounts exist, the inbox is empty, ...>

## Beats

| # | Persona | Beat | The user does | Done when | Seconds |
|---|---|---|---|---|---|
| 0 | | Intro | (pre-roll) | | 5 |
| 1 | Dana | Hook | Says who they are and what they want | | 12 |
| 2 | Dana | <title> | <one action> | <what is on screen> | 35 |
| 3 | Dana | <title> | <one action> | <what is on screen> | 40 |
| | | Handoff card: Sam | | | 2 |
| 4 | Sam | <title> | <one action> | <what is on screen> | 45 |
| 5 | Sam | <title> | <one action> | <what is on screen> | 40 |
| | | Handoff card: Dana | | | 2 |
| 6 | Dana | Verdict | Names the top three frictions | | 25 |
| 7 | | End card | | | 4 |
| | | **Total** | | | **210** |

## Friction expected

<What the dry run found, so the person knows where to slow down and react.
Leave empty if nobody has walked it yet.>

## Out of scope

<What this video does not cover.>
