# Security Policy

## Supported versions

Blended is pre-1.0. Only the latest build from `main` and the latest tagged release get
security fixes.

## Reporting a vulnerability

Please do not open a public issue for a security problem.

Report it privately through GitHub: on the repository's **Security** tab, choose
**Report a vulnerability**. If that option isn't available, open a public issue that asks for a
private contact, without any details of the problem.

Please include:

- the Blended build or version (CI build number, or the version in the window title);
- what an attacker can do, and how (for example a crafted `.blend` or `.blended` file, a
  script, or an add-on);
- steps or a file that reproduce it, if you have them.

You'll get an acknowledgement, and the fix will be credited in `CHANGELOG.md` unless you ask
otherwise.

## What is not a vulnerability

As in Blender, a `.blend` or `.blended` file can contain Python scripts, and Auto Run (off by
default) lets them run when the file opens. Opening a file is like running a script: only open
files from sources you trust. A report that a file runs its own scripts with Auto Run enabled is
expected behavior, not a vulnerability.

## Upstream Blender

Blended is a fork of Blender. If the problem is also in upstream Blender, please report it to
the Blender project as well, following
[Blender's security policy](https://developer.blender.org/docs/handbook/bug_reports/vulnerability_reports/).

## Verifying a build

Every Windows build records SHA-256 checksums in its CI run summary, and releases publish a
`.sha256` file next to the zip. Builds also carry a signed build-provenance attestation that ties
`Blended.exe` and the zip to the commit and workflow run that built them:

```
gh attestation verify Blended.exe --repo EvangAI-777/Blended
```
