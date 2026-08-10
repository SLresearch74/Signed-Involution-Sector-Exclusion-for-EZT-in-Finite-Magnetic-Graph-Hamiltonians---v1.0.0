# Lean / Mathlib M3A workstation setup report

## Final status

READY FOR M3A FORMALISATION

## 1. Windows version

- Edition: Microsoft Windows 11 Pro
- Version: 10.0.26200.8875 (25H2, build 26200)
- System type: x64-based PC
- Shell used: PowerShell

## 2. Git version

- Git for Windows 2.54.0.windows.1
- Executable: `C:\Program Files\Git\cmd\git.exe`
- Installer SHA-256:
  `2b96e7854f0520f0f6b709c21041d9801b1be44d5e1a0d9fa621b2fbc40f1983`
- Installer Authenticode signature: valid; signer Johannes Schindelin

The initial diagnostic found Git 2.53.0.windows.3 only inside Codex's bundled
runtime. A refreshed normal Windows PATH had no Git, so the official Git for
Windows distribution was installed after approval.

## 3. VS Code version

- Version: 1.131.0
- Commit: `e4c7e7b1d6d060162f4aa7f8225271b67ce1df75`
- Architecture: x64
- Installation: signed Microsoft per-user installer

## 4. Lean extension identifier

- `leanprover.lean4@0.0.239`
- Publisher: `leanprover`
- VS Code reported the project folder as trusted and all enabled extensions as
  active.

## 5. elan version

- `elan 4.2.3 (b6cec7e10 2026-06-08)`
- Installed under `%USERPROFILE%\.elan`
- No global Lean default was required; the project toolchain is authoritative.

## 6. Project Lean toolchain

`leanprover/lean4:v4.32.1`

This is recorded in `lean-toolchain`; no dependency-driven substitution was
needed.

## 7. Lean version

`Lean (version 4.32.1, x86_64-w64-windows-gnu, commit f054605aea4b840552cca2e725580bffd1e1b704, Release)`

## 8. Lake version

`Lake version 5.0.0-src+f054605 (Lean version 4.32.1)`

## 9. Mathlib revision

- Requested/input revision: `v4.32.1`
- Resolved commit from `lake-manifest.json`:
  `520045ab14e26149ee970e2e617ca04b09bde5d6`
- Repository: `https://github.com/leanprover-community/mathlib4`

## 10. Project path

`C:\Users\skilo\Documents\M3AFormalisation`

Username-independent form: `%USERPROFILE%\Documents\M3AFormalisation`.

The target did not exist before creation, so no existing project was
overwritten and no deduplicated name was needed.

## 11. Commands run

The complete chronological terminal-command log is in
`lean_setup_log/commands.txt`. Principal commands were:

```powershell
elan toolchain install leanprover/lean4:v4.32.1
lean +leanprover/lean4:v4.32.1 --version
lake +leanprover/lean4:v4.32.1 --version
lake +leanprover/lean4:v4.32.1 new M3AFormalisation math
lake update
lake exe cache get
lake env lean M3A\Basic.lean
lake env lean M3A\CoefficientAlgebra.lean
lake build
code --install-extension leanprover.lean4
code --reuse-window . M3A\CoefficientAlgebra.lean
```

Installer signature, checksum, PATH and version checks are also recorded in the
log directory.

## 12. Files created

- `lean-toolchain`
- `lakefile.toml`
- `lake-manifest.json`
- `M3AFormalisation.lean`
- `M3A/Basic.lean`
- `M3A/CoefficientAlgebra.lean`
- `M3A/Model.lean`
- `LEAN_M3A_SETUP_REPORT.md`
- `lean_setup_log/environment.txt`
- `lean_setup_log/commands.txt`
- `lean_setup_log/stdout.txt`
- `lean_setup_log/stderr.txt`
- `lean_setup_log/final_status.md`

Lake-generated `.git`, `.github`, `.gitignore`, `README.md` and the original
template module were preserved. Generated caches/build outputs remain in
`.lake` locally but are excluded from the bootstrap ZIP.

## 13. `lake build` result

Success:

```text
Built M3A.Basic
Built M3A.CoefficientAlgebra
Built M3A.Model
Built M3AFormalisation
Build completed successfully (8659 jobs).
lake build verification exit code: 0
```

## 14. First M3A theorem result

`M3A.coefficient_syzygy` compiled successfully from the exact requested
definitions and proof:

```lean
by
  simp [cubicCoeff, quad, ell]
  ring
```

The source contains no `sorry`, `admit`, user-declared `axiom`, `unsafe`
escape, or unverified external theorem.

## 15. Axiom report

Lean printed:

```text
'M3A.coefficient_syzygy' depends on axioms: [propext, Quot.sound]
```

These are Lean's ordinary logical/extensionality and quotient foundations; no
project-specific axioms are present.

## 16. Errors encountered and resolution

1. WMI/CIM OS query was denied. `systeminfo`, `ver` and the registry supplied
   the required OS facts.
2. The VS Code installer wrapper timed out after installation started. The
   installed CLI, version and signed publisher were verified directly before
   the installer was deleted.
3. The first elan script invocation passed a Boolean as text. The same official
   script was rerun with a real PowerShell Boolean and completed successfully.
4. No default Lean toolchain was configured immediately after elan by design.
   The requested named toolchain was installed and selected by the project.
5. `lake new`/`lake update` wrapper timeouts occurred during the first large
   dependency checkout. Task-owned child processes were monitored; the manifest
   was generated and the official Mathlib cache later exited 0.
6. The first Mathlib load outlived a short wrapper. A bounded rerun of
   `Basic.lean` exited 0.
7. The initial full build could not discover the requested `M3A.*` modules.
   The generated library globs were extended to include `M3A.+`; dependency and
   toolchain revisions were unchanged. The rebuild succeeded.
8. VS Code status access was initially blocked by the workspace sandbox. The
   status was rerun with user-profile permission. The normal VS Code profile was
   visually verified with the project root open, the official Lean InfoView
   active, no red errors, and `No goals / Goals accomplished!` after `ring`.
9. Git was absent from the refreshed normal user PATH. Signed Git for Windows
   2.54.0 was installed and verified.

Full captured details are in `lean_setup_log/stderr.txt`.

## 17. Exact unresolved issues

None.

The stop condition has been reached. No attempt was made to formalise the rest
of the paper. The next phase should begin with a theorem-to-Lean dependency map
covering signed involutions and baseline darkness, the exact selected numerator,
the dark-plane decomposition, endpoint word support, the fixed-ray trichotomy,
and the fixed-fibre Newton theorem.
