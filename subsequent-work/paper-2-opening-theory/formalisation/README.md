# M3A Paper II formalisation

This is the source-only Lean project for Paper II stages M0-M8.

- Lean toolchain: `leanprover/lean4:v4.32.1`
- Mathlib revision: `v4.32.1`
- Root import: `M3A.AnalyticBridge`
- Build: `lake build`
- Direct root check: `lake env lean M3AFormalisation.lean`

The `M3A/` modules are ordered by the dependency spine documented in
`reports/M3A_THEOREM_TO_LEAN_DEPENDENCY_MAP.md`. The `reports/` directory also
contains the M1-M8 build and axiom reports produced during the completed local
development.

Compiled `.lake` content is intentionally excluded. Lake reconstructs it from
`lakefile.toml`, `lake-manifest.json`, and `lean-toolchain`.

