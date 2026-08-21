# QML untrusted content

Plugins in Omarchy share `omarchy-shell`. There is no renderer sandbox.

## Text.AutoText (seen in marketplace review)

`Text.textFormat` defaults to `Text.AutoText`, which uses `Qt::mightBeRichText()`.
If the string looks like HTML, Qt parses the [supported HTML subset](https://doc.qt.io/qt-6/richtext-html-subset.html).
From [Text QML](https://doc.qt.io/qt-6/qml-qtquick-text.html):

> When displaying user-controlled, untrusted content, the textFormat should
> either be explicitly set to Text.PlainText, or the contents should be stripped
> of unwanted tags. … inline images. This functionality includes loading images
> remotely over the network.

A vault title or username such as `<img src="https://attacker.example/x.png">`
makes Quickshell request that URL when the row renders. Effect: IP/timing
beacon, proof the item exists, not JS XSS and not Dashlane cookie theft.

Fix at the binding:

```qml
textFormat: Text.PlainText
```

Apply to every `Text` / `TextEdit` / `Label` that shows API, CLI, file, or
clipboard data — not only fields named "html". `elide` does not disable rich text.

## Other QML sinks

- **`Image { source: url }`** — HTTP(S) or `file://`. Qt has had crashes on
  invalid image sources ([advisory, 2023](https://www.qt.io/blog/security-advisory-loading-invalid-qml-image-source-impacts-qt)).
  Allowlist schemes and hosts, or do not bind untrusted URLs.
- **`Loader { source: url }`** and **`Qt.createQmlObject(qmlString, …)`** —
  [dynamic QML instantiation](https://doc.qt.io/qt-6/qtqml-javascript-dynamicobjectcreation.html)
  is code execution. Never pass untrusted strings.
- **`WebEngineView`** — Chromium. Do not point at untrusted URLs from a
  privileged shell process.
- **`XMLHttpRequest` / `WebSocket`** — user-controlled URLs become SSRF from
  the desktop session.

## Process and IPC

Quickshell `Process.command` is an argv list. Values in that list appear in
`ps` and `/proc/<pid>/cmdline`. Pass secrets on stdin (Omarchy
`omarchy.network` EAP: `stdinEnabled: true`, `write(secret)`, then close stdin).

Do not `bash -c` with interpolated names, SSIDs, or ids. `id=` filters belong
in their own argv slot.

Bar widgets instantiate per monitor. Duplicate `IpcHandler` targets warn at
runtime. `Process.onExited` that mutates UI during `omarchy-shell shell rescanPlugins`
or `omarchy restart shell` has hit Quickshell
`IpcHandler::updateRegistration` SIGSEGV. Guard with an `alive` flag; stop
processes in `Component.onDestruction`; avoid background secret-bearing polls.

## Cache and clipboard

If you index untrusted metadata, allowlist keys in the helper before JSON
leaves the process. Never persist password/otp/token fields. `os.makedirs` +
`chmod 0o700` on the directory; open cache files with `0o600`. Default umask
`022` otherwise yields world-readable `~/.cache/.../index.json`.

Clipboard: copy via `wl-copy` (or the platform CLI), then after a delay clear
**only if** `wl-paste` still equals the secret.
