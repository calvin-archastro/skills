---
name: omarchy-plugin
description: >
  Author, review, or publish an Omarchy Quickshell plugin (bar widget, panel,
  overlay, service, marketplace listing). Use when building or reviewing
  ~/.config/omarchy/plugins code, writing manifest.json, talking to
  omarchyplugins.com, or handling QML untrusted-content / Process secrets.
  Triggers: omarchy plugin, bar widget, Quickshell plugin, QML security,
  Text.AutoText, PlainText, marketplace, /omarchy-plugin.
---

# Omarchy plugin

Plugins run **unsandboxed inside `omarchy-shell`**. Same user, same process as
the bar. Treat every helper, QML binding, and cache file as if a hostile string
from disk or a shared vault will land in it.

Official runtime contract: `$OMARCHY_PATH/shell/README.md` and
`$OMARCHY_PATH/shell/plugins/README.md`. Marketplace packaging:
https://omarchyplugins.com/develop.html and
https://omarchyplugins.com/publish.html. QML untrusted-content details:
[references/qml-untrusted-content.md](references/qml-untrusted-content.md).

## Build

1. **Clone a built-in of the same kind.** `omarchy plugin clone omarchy.clock --edit`
   (or dropbox/bluetooth/weather for a popup bar widget). Edit
   `~/.config/omarchy/plugins/<id>/`, never `/usr/share/omarchy/`.
2. **Keep `moduleName` / `ipcTarget` equal to `manifest.json` `id`.** Nested
   panels stay one `bar-widget`; do not invent a second `kinds` entry for a
   Loader'd `Panel.qml`.
3. **Use `qs.Ui` / `qs.Commons`.** `BarWidget`, `Panel`, `KeyboardPanel`,
   `PanelHero`, `TextField`, `ButtonGroup`/`TabBar`. Do not skin Fusion
   controls unless you replace `background` and `contentItem`.
4. **Saved QML hot-reloads.** Force discovery with
   `omarchy-shell shell rescanPlugins`. Do **not** `omarchy restart shell` to
   pick up plugin edits — Process `onExited` during IpcHandler reregistration
   has segfaulted Quickshell (reload + live `Process`).
5. **Validate before share:**
   `omarchy plugin validate "$PLUGIN_DIR"` and
   `qmllint -I "$OMARCHY_PATH/shell" "$PLUGIN_DIR"/*.qml`.

Permanent IDs are namespaced and **not** `omarchy.*` (`cgrunewald.dashlane`,
`io.github.you.plugin`). Changing an ID after listing is a new plugin.

## Untrusted data (mandatory)

Anything not a string you authored in the QML file is untrusted: API JSON,
CLI output, files, clipboard, other apps' titles, vault fields, URLs.

**Render as labels, never as markup or code.**

```qml
Text {
  text: item.title
  textFormat: Text.PlainText   // default is AutoText — will fetch <img src="https://…">
}
```

Same rule for `TextEdit`, `TextArea`, and Qt Quick Controls `Label` that show
untrusted strings. Qt documents this: AutoText/RichText/MarkdownText will load
remote images from HTML. Marketplace review has already rejected a plugin for
this (Dashlane titles/usernames).

Do not bind untrusted strings to:

| Sink | Why |
|---|---|
| `Text` without `PlainText` | Remote image / markup |
| `Image.source` / `AnimatedImage.source` | Network or `file://` fetch |
| `Loader.source` / `Loader.sourceComponent` from a string | Loads QML (code exec) |
| `Qt.createQmlObject` / `Qt.createComponent` on untrusted input | Code exec |
| `WebEngineView.url` | Full browser |
| `Process.command` with a secret in the array | Visible in `/proc/…/cmdline` and `ps` |

Secrets go **stdin**, never argv. Pattern used by Omarchy network EAP:

```qml
Process {
  stdinEnabled: true
  onStarted: { write(secret); secret = ""; stdinEnabled = false }
}
```

Do not dump a secrets API (`password -o json`, etc.) into QML. Strip to an
allowlist in a helper, then parse. Do not write secrets to `~/.cache`. Cache
dirs `0700`, files `0600`. Clipboard copies of secrets should expire (overwrite
only if still the same value).

`Process` helpers: argv arrays (no `bash -c` with interpolated user data);
`alive` flag and skip `onExited` after `Component.onDestruction`; do not poll
secret-bearing commands on a timer while the panel is closed.

## Publish (omarchyplugins.com)

That catalog is the community marketplace, not first-party Omarchy (`omarchy.*`
stays in basecamp/omarchy). Listing is **not** a security audit.

Repo root must have `manifest.json`, README with **install and remove**, and a
license. Then file
https://github.com/HANCORE-linux/omarchy-plugin-marketplace/issues/new?template=submit-plugin.yml
(or the [CLI body in SUBMISSION.md](https://github.com/HANCORE-linux/omarchy-plugin-marketplace/blob/main/SUBMISSION.md)).
Show the user the issue title+body and get an explicit go-ahead before `gh issue create`.

Automated baseline only catches a short static list (`curl\|sh`, sudoers, …).
It will not catch AutoText image fetches. Still fix those.

## Review checklist

- [ ] `textFormat: Text.PlainText` on every `Text` bound to external data
- [ ] No untrusted `Image.source` / `Loader.source`
- [ ] No secrets in `Process.command`
- [ ] Cache permissions 700/600; no secret fields on disk
- [ ] README install **and** remove; license; unique id
- [ ] `omarchy plugin validate` clean
- [ ] Did not restart the shell just to reload QML
