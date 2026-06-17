#!/usr/bin/env python3
"""
Test 5: projector dependence of sector-breaking mass-equivalent.

Purpose:
  Compare m_break(P) across different protecting/candidate projectors.

  The previous tests established:

      m_break(P) = |epsilon| ||P B Q + Q B P|| / c^2

  or, for angular-frequency Hamiltonians,

      m_break(P) = hbar |epsilon| ||P B Q + Q B P|| / c^2.

  Test 4 showed that P must remain in the notation. Test 5 asks:

      How do certificate projectors compare with Krylov projectors?

Projectors examined:
  1. P_cert:
       the signed-involution certificate projector from the unperturbed construction.

  2. P_krylov_H0:
       the canonical source-generated Krylov projector for the unperturbed Hamiltonian H0.

  3. P_krylov_Heps:
       the source-generated Krylov projector for the perturbed Hamiltonian H_epsilon.
       This is not used as the perturbative sector in the original theorem unless it
       also commutes with H0, but it diagnoses the actual reachable subspace after perturbation.

  4. P_enlarged:
       only for the auxiliary-channel construction; a deliberately larger valid projector.

Scenarios:
  A. original_C8_sector_preserving_mirror_diag
  B. original_C8_reflection_breaking_diag
  C. original_C8_direct_target_coupling
  D. extended_C8_aux_channel
  E. extended_C8_direct_target_control

Outputs:
  /mnt/data/test5_projector_dependence.py
  /mnt/data/test5_projector_summary.csv
  /mnt/data/test5_projector_metrics.csv
  /mnt/data/test5_moment_audit.csv
  /mnt/data/test5_timeseries.csv
  /mnt/data/test5_projector_bperp_comparison.png
  /mnt/data/test5_target_probability_by_scenario.png
  /mnt/data/test5_projector_rank_comparison.png
  /mnt/data/test5_README.md
"""

from __future__ import annotations

import csv
from pathlib import Path
import numpy as np

C_LIGHT = 299_792_458.0
HBAR = 1.054_571_817e-34


def scalar_pi_flux_cycle(N: int, g: float = 1.0) -> np.ndarray:
    if N < 4 or N % 2 != 0:
        raise ValueError("N must be even and >= 4.")
    H = np.zeros((N, N), dtype=complex)
    for n in range(N - 1):
        H[n + 1, n] = g
        H[n, n + 1] = g
    H[0, N - 1] = -g
    H[N - 1, 0] = -g
    return H


def signed_reflection_R_pi(N: int) -> np.ndarray:
    R = np.zeros((N, N), dtype=complex)
    for n in range(N):
        if n == 0:
            R[0, 0] = 1.0
        else:
            R[(-n) % N, n] = -1.0
    return R


def op_norm(A: np.ndarray) -> float:
    return float(np.linalg.norm(A, ord=2))


def fro_norm(A: np.ndarray) -> float:
    return float(np.linalg.norm(A, ord="fro"))


def projector_rank(P: np.ndarray) -> float:
    # For an exact orthogonal projector, trace is rank. Return real trace.
    return float(np.real_if_close(np.trace(P)))


def sector_breaking_block(B: np.ndarray, P: np.ndarray) -> np.ndarray:
    I = np.eye(B.shape[0], dtype=complex)
    Q = I - P
    return P @ B @ Q + Q @ B @ P


def krylov_projector(H: np.ndarray, s: int, tol: float = 1e-10) -> tuple[np.ndarray, int, np.ndarray]:
    """
    Orthogonal projector onto span{s, Hs, ..., H^(n-1)s}.
    Uses SVD for numerical rank and basis.
    """
    n = H.shape[0]
    e_s = np.eye(n, dtype=complex)[:, s]
    K = np.zeros((n, n), dtype=complex)
    v = e_s.copy()
    for k in range(n):
        K[:, k] = v
        v = H @ v

    U, singular_values, _ = np.linalg.svd(K, full_matrices=False)
    if singular_values[0] == 0:
        rank = 0
    else:
        rank = int(np.sum(singular_values > tol * singular_values[0]))
    basis = U[:, :rank]
    P = basis @ basis.conjugate().T
    return P, rank, singular_values


def amplitude_timeseries(H: np.ndarray, times: np.ndarray, s: int, ell: int) -> np.ndarray:
    vals, vecs = np.linalg.eigh(H)
    coeffs = vecs[ell, :] * np.conjugate(vecs[s, :])
    phases = np.exp(-1j * np.outer(times, vals))
    return phases @ coeffs


def moment_sequence(H: np.ndarray, s: int, ell: int, max_k: int) -> list[complex]:
    n = H.shape[0]
    e_s = np.eye(n, dtype=complex)[:, s]
    bra = np.eye(n, dtype=complex)[ell, :].conjugate()
    moments = []
    v = e_s.copy()
    for k in range(max_k + 1):
        moments.append(complex(bra @ v))
        v = H @ v
    return moments


def make_original_scenario(B_type: str, N: int = 8) -> dict:
    H0 = scalar_pi_flux_cycle(N)
    R = signed_reflection_R_pi(N)
    P_cert = (np.eye(N, dtype=complex) + R) / 2.0
    s = 0
    ell = N // 2

    if B_type == "sector_preserving_mirror_diag":
        f = np.zeros(N)
        f[0] = 0.25
        f[N // 2] = 0.90
        vals = {1: -0.10, 2: 0.60, 3: -0.35}
        for n, value in vals.items():
            f[n] = value
            f[(-n) % N] = value
        B = np.diag(f).astype(complex)
        scenario_name = "original_C8_sector_preserving_mirror_diag"

    elif B_type == "reflection_breaking_diag":
        n = np.arange(N)
        B = np.diag(np.sin(2.0 * np.pi * n / N)).astype(complex)
        scenario_name = "original_C8_reflection_breaking_diag"

    elif B_type == "direct_target":
        B = np.zeros((N, N), dtype=complex)
        B[s, ell] = 1.0
        B[ell, s] = 1.0
        scenario_name = "original_C8_direct_target_coupling"

    else:
        raise ValueError(f"Unknown original B_type: {B_type}")

    return {
        "scenario": scenario_name,
        "H0": H0,
        "B": B,
        "P_cert": P_cert,
        "P_enlarged": None,
        "s": s,
        "ell": ell,
        "description": B_type,
    }


def make_extended_scenario(B_type: str, N_cycle: int = 8) -> dict:
    H_cycle = scalar_pi_flux_cycle(N_cycle)
    R_cycle = signed_reflection_R_pi(N_cycle)
    P_cycle = (np.eye(N_cycle, dtype=complex) + R_cycle) / 2.0

    n = N_cycle + 1
    aux = N_cycle
    s = 0
    ell = N_cycle // 2

    H0 = np.zeros((n, n), dtype=complex)
    H0[:N_cycle, :N_cycle] = H_cycle

    P_old = np.zeros((n, n), dtype=complex)
    P_old[:N_cycle, :N_cycle] = P_cycle

    P_enlarged = P_old.copy()
    P_enlarged[aux, aux] = 1.0

    if B_type == "aux_channel":
        B = np.zeros((n, n), dtype=complex)
        B[s, aux] = 1.0
        B[aux, s] = 1.0
        scenario_name = "extended_C8_aux_channel"
    elif B_type == "direct_target":
        B = np.zeros((n, n), dtype=complex)
        B[s, ell] = 1.0
        B[ell, s] = 1.0
        scenario_name = "extended_C8_direct_target_control"
    else:
        raise ValueError(f"Unknown extended B_type: {B_type}")

    return {
        "scenario": scenario_name,
        "H0": H0,
        "B": B,
        "P_cert": P_old,
        "P_enlarged": P_enlarged,
        "s": s,
        "ell": ell,
        "aux": aux,
        "description": B_type,
    }


def classify_exact_zero(max_prob: float, max_moment_abs: float, tol: float = 1e-10) -> bool:
    return bool(max_prob < tol and max_moment_abs < tol)


def run_test(out_dir: Path) -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)

    scenarios = [
        make_original_scenario("sector_preserving_mirror_diag"),
        make_original_scenario("reflection_breaking_diag"),
        make_original_scenario("direct_target"),
        make_extended_scenario("aux_channel"),
        make_extended_scenario("direct_target"),
    ]

    eps_values = [0.10, 0.50]
    T = 20.0
    n_times = 2001
    times = np.linspace(0.0, T, n_times)

    summary_rows = []
    metrics_rows = []
    moment_rows = []
    timeseries_rows = []

    for scen in scenarios:
        scenario = scen["scenario"]
        H0 = scen["H0"]
        B = scen["B"]
        P_cert = scen["P_cert"]
        P_enlarged = scen["P_enlarged"]
        s = scen["s"]
        ell = scen["ell"]
        n = H0.shape[0]

        P_k0, rank_k0, sv_k0 = krylov_projector(H0, s)
        P_cert_minus_k0_fro = fro_norm(P_cert - P_k0)
        P_cert_minus_k0_op = op_norm(P_cert - P_k0)

        for eps in eps_values:
            H_eps = H0 + eps * B

            amps = amplitude_timeseries(H_eps, times, s, ell)
            amp_abs = np.abs(amps)
            probs = amp_abs ** 2

            moments = moment_sequence(H_eps, s, ell, max_k=n - 1)
            max_moment_abs = float(max(abs(m) for m in moments))
            exact_zero_by_audit = classify_exact_zero(float(np.max(probs)), max_moment_abs)

            P_keps, rank_keps, sv_keps = krylov_projector(H_eps, s)
            P_keps_target_error = float(np.linalg.norm(P_keps @ np.eye(n, dtype=complex)[:, ell]))
            P_k0_minus_keps_fro = fro_norm(P_k0 - P_keps)
            P_k0_minus_keps_op = op_norm(P_k0 - P_keps)

            # Moment audit rows.
            for k, m in enumerate(moments):
                moment_rows.append({
                    "test": "Test 5 projector dependence",
                    "scenario": scenario,
                    "epsilon": eps,
                    "k": k,
                    "moment_real": float(np.real(m)),
                    "moment_imag": float(np.imag(m)),
                    "moment_abs": float(abs(m)),
                    "n": n,
                    "source_s": s,
                    "target_ell": ell,
                })

            # Summary.
            summary_rows.append({
                "test": "Test 5 projector dependence",
                "scenario": scenario,
                "description": scen["description"],
                "epsilon": eps,
                "n": n,
                "source_s": s,
                "target_ell": ell,
                "rank_P_cert": projector_rank(P_cert),
                "rank_P_krylov_H0": projector_rank(P_k0),
                "rank_P_krylov_Heps": projector_rank(P_keps),
                "rank_P_enlarged": projector_rank(P_enlarged) if P_enlarged is not None else "",
                "P_cert_minus_P_krylov_H0_fro": P_cert_minus_k0_fro,
                "P_cert_minus_P_krylov_H0_op": P_cert_minus_k0_op,
                "P_krylov_H0_minus_P_krylov_Heps_fro": P_k0_minus_keps_fro,
                "P_krylov_H0_minus_P_krylov_Heps_op": P_k0_minus_keps_op,
                "P_krylov_Heps_target_error": P_keps_target_error,
                "max_target_amplitude": float(np.max(amp_abs)),
                "max_target_probability": float(np.max(probs)),
                "avg_target_probability": float(np.trapz(probs, times) / T),
                "max_moment_abs_k0_to_nminus1": max_moment_abs,
                "exact_zero_by_moment_and_time_audit": exact_zero_by_audit,
                "time_of_max_probability": float(times[int(np.argmax(probs))]),
            })

            # Projector metrics.
            projectors = [
                ("P_cert", P_cert, "signed/inherited certificate projector for H0"),
                ("P_krylov_H0", P_k0, "canonical Krylov projector for unperturbed H0"),
                ("P_krylov_Heps", P_keps, "canonical Krylov projector for perturbed H_epsilon"),
            ]
            if P_enlarged is not None:
                projectors.append(("P_enlarged", P_enlarged, "deliberately enlarged valid projector for aux case"))

            E = np.eye(n, dtype=complex)
            e_s = E[:, s]
            e_ell = E[:, ell]

            for pname, P, pdesc in projectors:
                Bperp = sector_breaking_block(B, P)
                Bperp_norm = op_norm(Bperp)

                comm_H0_P = fro_norm(H0 @ P - P @ H0)
                comm_Heps_P = fro_norm(H_eps @ P - P @ H_eps)
                comm_B_P = fro_norm(B @ P - P @ B)

                source_error = float(np.linalg.norm(P @ e_s - e_s))
                target_error = float(np.linalg.norm(P @ e_ell))

                protects_H0 = bool(comm_H0_P < 1e-10 and source_error < 1e-10 and target_error < 1e-10)
                protects_Heps = bool(comm_Heps_P < 1e-10 and source_error < 1e-10 and target_error < 1e-10)

                Ebreak_dimless = float(abs(eps) * Bperp_norm)
                mbreak_kg_if_rad_per_s = float(HBAR * Ebreak_dimless / (C_LIGHT ** 2))

                metrics_rows.append({
                    "test": "Test 5 projector dependence",
                    "scenario": scenario,
                    "epsilon": eps,
                    "projector": pname,
                    "projector_description": pdesc,
                    "rank": projector_rank(P),
                    "comm_H0_P_fro": comm_H0_P,
                    "comm_Heps_P_fro": comm_Heps_P,
                    "comm_B_P_fro": comm_B_P,
                    "source_containment_error": source_error,
                    "target_exclusion_error": target_error,
                    "protects_H0": protects_H0,
                    "protects_Heps": protects_Heps,
                    "Bperp_operator_norm": Bperp_norm,
                    "Ebreak_dimensionless": Ebreak_dimless,
                    "mbreak_kg_if_B_units_rad_per_s": mbreak_kg_if_rad_per_s,
                    "diff_to_P_cert_fro": fro_norm(P - P_cert),
                    "diff_to_P_krylov_H0_fro": fro_norm(P - P_k0),
                    "diff_to_P_krylov_Heps_fro": fro_norm(P - P_keps),
                    "actual_max_target_probability": float(np.max(probs)),
                    "actual_exact_zero_by_audit": exact_zero_by_audit,
                })

            # Time series for all scenarios at eps=0.10; enough for plots.
            if abs(eps - 0.10) < 1e-12:
                for t, amp, aa, pp in zip(times, amps, amp_abs, probs):
                    timeseries_rows.append({
                        "test": "Test 5 projector dependence",
                        "scenario": scenario,
                        "epsilon": eps,
                        "t": float(t),
                        "amp_real": float(np.real(amp)),
                        "amp_imag": float(np.imag(amp)),
                        "amp_abs": float(aa),
                        "probability": float(pp),
                        "n": n,
                        "source_s": s,
                        "target_ell": ell,
                    })

    # Write CSVs.
    summary_path = out_dir / "test5_projector_summary.csv"
    metrics_path = out_dir / "test5_projector_metrics.csv"
    moment_path = out_dir / "test5_moment_audit.csv"
    timeseries_path = out_dir / "test5_timeseries.csv"

    with summary_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary_rows[0].keys()))
        writer.writeheader()
        writer.writerows(summary_rows)

    with metrics_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(metrics_rows[0].keys()))
        writer.writeheader()
        writer.writerows(metrics_rows)

    with moment_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(moment_rows[0].keys()))
        writer.writeheader()
        writer.writerows(moment_rows)

    with timeseries_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(timeseries_rows[0].keys()))
        writer.writeheader()
        writer.writerows(timeseries_rows)

    # README.
    readme_path = out_dir / "test5_README.md"
    readme_path.write_text("""# Test 5: projector dependence

## Purpose

This test compares the sector-breaking mass-equivalent across different projectors:

```text
m_break(P) = |epsilon| ||P B Q + Q B P|| / c^2
```

or, for angular-frequency Hamiltonians,

```text
m_break(P) = hbar |epsilon| ||P B Q + Q B P|| / c^2
```

The goal is to test the refinement from Test 4:

```text
P must stay in the notation.
```

## Projectors

The script compares:

1. `P_cert`  
   The signed/inherited certificate projector for the unperturbed system.

2. `P_krylov_H0`  
   The canonical source-generated Krylov projector for the unperturbed Hamiltonian.

3. `P_krylov_Heps`  
   The canonical source-generated Krylov projector for the perturbed Hamiltonian.
   This diagnoses the actual reachable subspace after the perturbation.

4. `P_enlarged`  
   Only in the auxiliary-channel scenario: a deliberately larger sector that still excludes the target.

## Scenarios

- `original_C8_sector_preserving_mirror_diag`
- `original_C8_reflection_breaking_diag`
- `original_C8_direct_target_coupling`
- `extended_C8_aux_channel`
- `extended_C8_direct_target_control`

## Main expected lessons

- In the basic scalar pi-flux cycle, `P_cert` and `P_krylov_H0` should coincide numerically.
- If a perturbation preserves the original sector, all relevant projectors remain stable and target leakage remains zero.
- If a perturbation breaks the original sector and reaches the target, `P_krylov_Heps` should expand to include the target.
- If a perturbation breaks the old sector but only opens an auxiliary channel, `P_krylov_Heps` can expand without including the target.
- Therefore `m_break(P)` is projector-dependent, while the Krylov projector diagnoses actual reachability for a given Hamiltonian.

## Files

- `test5_projector_dependence.py`: self-contained script.
- `test5_projector_summary.csv`: one row per scenario and epsilon.
- `test5_projector_metrics.csv`: one row per scenario, epsilon, and projector.
- `test5_moment_audit.csv`: finite moments through `k = 0,...,n-1`.
- `test5_timeseries.csv`: target probability curves at `epsilon = 0.10`.
- `test5_projector_bperp_comparison.png`: B_perp comparison across projectors.
- `test5_target_probability_by_scenario.png`: target probability curves by scenario.
- `test5_projector_rank_comparison.png`: rank comparison across projectors.
""")

    # Plots.
    bperp_plot_path = out_dir / "test5_projector_bperp_comparison.png"
    target_plot_path = out_dir / "test5_target_probability_by_scenario.png"
    rank_plot_path = out_dir / "test5_projector_rank_comparison.png"

    try:
        import matplotlib.pyplot as plt

        # Bperp comparison for eps=0.10.
        eps_plot = 0.10
        eps_metrics = [r for r in metrics_rows if abs(r["epsilon"] - eps_plot) < 1e-12]
        scenarios_unique = [s["scenario"] for s in scenarios]
        projector_order = ["P_cert", "P_krylov_H0", "P_krylov_Heps", "P_enlarged"]

        labels = []
        values = []
        for scenario in scenarios_unique:
            for projector in projector_order:
                rows = [r for r in eps_metrics if r["scenario"] == scenario and r["projector"] == projector]
                if rows:
                    labels.append(f"{scenario}\n{projector}")
                    values.append(rows[0]["Bperp_operator_norm"])

        plt.figure(figsize=(12, 6))
        plt.bar(range(len(values)), values)
        plt.xticks(range(len(labels)), labels, rotation=75, ha="right", fontsize=7)
        plt.ylabel("||B_perp(P)||")
        plt.title("Test 5: projector-dependent sector-breaking norm at epsilon=0.10")
        plt.tight_layout()
        plt.savefig(bperp_plot_path, dpi=200)
        plt.close()

        # Target probability curves.
        plt.figure(figsize=(9, 5))
        for scenario in scenarios_unique:
            rows = [r for r in timeseries_rows if r["scenario"] == scenario]
            xs = [r["t"] for r in rows]
            ys = [r["probability"] for r in rows]
            plt.plot(xs, ys, label=scenario)
        plt.xlabel("time")
        plt.ylabel("target probability")
        plt.title("Test 5: target probability by scenario at epsilon=0.10")
        plt.legend(fontsize=7)
        plt.tight_layout()
        plt.savefig(target_plot_path, dpi=200)
        plt.close()

        # Rank comparison for eps=0.10.
        eps_summary = [r for r in summary_rows if abs(r["epsilon"] - eps_plot) < 1e-12]
        x = np.arange(len(eps_summary))
        width = 0.25
        cert_ranks = [r["rank_P_cert"] for r in eps_summary]
        k0_ranks = [r["rank_P_krylov_H0"] for r in eps_summary]
        keps_ranks = [r["rank_P_krylov_Heps"] for r in eps_summary]
        scenario_labels = [r["scenario"] for r in eps_summary]

        plt.figure(figsize=(10, 5))
        plt.bar(x - width, cert_ranks, width, label="P_cert")
        plt.bar(x, k0_ranks, width, label="P_krylov_H0")
        plt.bar(x + width, keps_ranks, width, label="P_krylov_Heps")
        plt.xticks(x, scenario_labels, rotation=45, ha="right", fontsize=8)
        plt.ylabel("projector rank")
        plt.title("Test 5: projector rank comparison at epsilon=0.10")
        plt.legend()
        plt.tight_layout()
        plt.savefig(rank_plot_path, dpi=200)
        plt.close()

    except Exception as exc:
        bperp_plot_path.write_text(f"Plot generation failed: {exc}\n")
        target_plot_path.write_text(f"Plot generation failed: {exc}\n")
        rank_plot_path.write_text(f"Plot generation failed: {exc}\n")

    return {
        "script": out_dir / "test5_projector_dependence.py",
        "summary": summary_path,
        "metrics": metrics_path,
        "moment_audit": moment_path,
        "timeseries": timeseries_path,
        "readme": readme_path,
        "bperp_plot": bperp_plot_path,
        "target_plot": target_plot_path,
        "rank_plot": rank_plot_path,
    }


if __name__ == "__main__":
    outputs = run_test(Path("/mnt/data"))
    for key, path in outputs.items():
        print(f"{key}: {path}")
