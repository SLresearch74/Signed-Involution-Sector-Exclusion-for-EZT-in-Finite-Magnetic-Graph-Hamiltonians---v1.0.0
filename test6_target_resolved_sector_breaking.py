#!/usr/bin/env python3
"""
Test 6: target-resolved sector-breaking.

Purpose:
  Separate total canonical sector-breaking from target-effective first-order leakage.

  beta0(B) = ||P0 B Q0 + Q0 B P0||
      P0 = P_s^{H0}, the unperturbed source-generated Krylov projector.

  alpha_T(B) = max_{t in [0,T]} |A1(t)|

  A1(t) = -i int_0^t <ell| exp[-i(t-tau)H0] B_perp exp[-i tau H0] |s> d tau.

  beta0 > 0 means the canonical old source sector is broken.
  alpha_T measures whether that breaking is target-effective at first order.

Outputs:
  /mnt/data/test6_target_resolved_sector_breaking.py
  /mnt/data/test6_target_resolved_summary.csv
  /mnt/data/test6_first_order_timeseries.csv
  /mnt/data/test6_efficiency_comparison.csv
  /mnt/data/test6_moment_audit.csv
  /mnt/data/test6_first_order_vs_actual.png
  /mnt/data/test6_beta_vs_alpha.png
  /mnt/data/test6_target_efficiency.png
  /mnt/data/test6_README.md
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


def normalize_op_norm(A: np.ndarray, target: float = 1.0) -> np.ndarray:
    norm = op_norm(A)
    if norm == 0:
        raise ValueError("Cannot normalize zero operator.")
    return (target / norm) * A


def krylov_projector(H: np.ndarray, s: int, tol: float = 1e-10) -> tuple[np.ndarray, int, np.ndarray]:
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


def sector_breaking_block(B: np.ndarray, P: np.ndarray) -> np.ndarray:
    I = np.eye(B.shape[0], dtype=complex)
    Q = I - P
    return P @ B @ Q + Q @ B @ P


def amplitude_timeseries(H: np.ndarray, times: np.ndarray, s: int, ell: int) -> np.ndarray:
    vals, vecs = np.linalg.eigh(H)
    coeffs = vecs[ell, :] * np.conjugate(vecs[s, :])
    phases = np.exp(-1j * np.outer(times, vals))
    return phases @ coeffs


def first_order_A1_timeseries_spectral(
    H0: np.ndarray,
    Bperp: np.ndarray,
    times: np.ndarray,
    s: int,
    ell: int,
    degeneracy_tol: float = 1e-12,
) -> np.ndarray:
    """
    Fast spectral formula for

      A1(t) = -i int_0^t <ell|U0(t-tau) Bperp U0(tau)|s> d tau.

    If H0 |a> = lambda_a |a>, then:

      A1(t) = -i sum_ab c_ab exp(-i t lambda_a)
               int_0^t exp[-i tau(lambda_b-lambda_a)] d tau

    where:
      c_ab = <ell|a><a|Bperp|b><b|s>.
    """
    vals, vecs = np.linalg.eigh(H0)

    # C[a,b] = <ell|a><a|Bperp|b><b|s>
    C = (
        vecs[ell, :, None]
        * (vecs.conjugate().T @ Bperp @ vecs)
        * np.conjugate(vecs[s, :])[None, :]
    )

    A1 = np.zeros(len(times), dtype=complex)
    delta = vals[None, :] - vals[:, None]  # lambda_b - lambda_a

    for idx, t in enumerate(times):
        phase_a = np.exp(-1j * t * vals)[:, None]
        integral = np.empty_like(delta, dtype=complex)

        mask = np.abs(delta) < degeneracy_tol
        integral[mask] = t
        integral[~mask] = (1.0 - np.exp(-1j * delta[~mask] * t)) / (1j * delta[~mask])

        A1[idx] = -1j * np.sum(C * phase_a * integral)

    return A1


def moment_sequence(H: np.ndarray, s: int, ell: int, max_k: int) -> list[complex]:
    n = H.shape[0]
    e_s = np.eye(n, dtype=complex)[:, s]
    bra = np.eye(n, dtype=complex)[ell, :].conjugate()
    v = e_s.copy()
    moments = []
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
        "family": "structured",
        "H0": H0,
        "B": B,
        "P_cert": P_cert,
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

    P_cert = np.zeros((n, n), dtype=complex)
    P_cert[:N_cycle, :N_cycle] = P_cycle

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
        "family": "structured",
        "H0": H0,
        "B": B,
        "P_cert": P_cert,
        "s": s,
        "ell": ell,
        "aux": aux,
        "description": B_type,
    }


def make_random_cross_scenarios(count: int = 5, N: int = 8, seed: int = 606) -> list[dict]:
    rng = np.random.default_rng(seed)
    H0 = scalar_pi_flux_cycle(N)
    R = signed_reflection_R_pi(N)
    P_cert = (np.eye(N, dtype=complex) + R) / 2.0
    P0, _, _ = krylov_projector(H0, 0)
    I = np.eye(N, dtype=complex)
    Q0 = I - P0

    scenarios = []
    for j in range(count):
        X = rng.normal(size=(N, N)) + 1j * rng.normal(size=(N, N))
        A = (X + X.conjugate().T) / 2.0
        B_cross = P0 @ A @ Q0 + Q0 @ A @ P0
        B_cross = normalize_op_norm(B_cross, 1.0)
        scenarios.append({
            "scenario": f"original_C8_random_cross_beta1_{j+1}",
            "family": "random_beta1",
            "H0": H0,
            "B": B_cross,
            "P_cert": P_cert,
            "s": 0,
            "ell": N // 2,
            "description": "random pure cross-block perturbation normalized to beta0=1",
        })
    return scenarios


def safe_ratio(num: float, den: float) -> float:
    if den == 0:
        return float("nan")
    return float(num / den)


def run_test(out_dir: Path) -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)

    scenarios = [
        make_original_scenario("sector_preserving_mirror_diag"),
        make_original_scenario("reflection_breaking_diag"),
        make_original_scenario("direct_target"),
        make_extended_scenario("aux_channel"),
        make_extended_scenario("direct_target"),
    ] + make_random_cross_scenarios(count=5)

    T = 20.0
    n_times = 1201
    times = np.linspace(0.0, T, n_times)

    eps_small = 1e-4
    eps_report = 0.10

    summary_rows = []
    timeseries_rows = []
    efficiency_rows = []
    moment_rows = []

    for scen in scenarios:
        scenario = scen["scenario"]
        family = scen["family"]
        H0 = scen["H0"]
        B = scen["B"]
        s = scen["s"]
        ell = scen["ell"]
        n = H0.shape[0]

        P0, rank_P0, _ = krylov_projector(H0, s)
        I = np.eye(n, dtype=complex)
        Bperp0 = sector_breaking_block(B, P0)
        beta0 = op_norm(Bperp0)

        e_s = I[:, s]
        e_ell = I[:, ell]
        source_error = float(np.linalg.norm(P0 @ e_s - e_s))
        target_error = float(np.linalg.norm(P0 @ e_ell))
        comm_H0_P0 = fro_norm(H0 @ P0 - P0 @ H0)

        A1 = first_order_A1_timeseries_spectral(H0, Bperp0, times, s, ell)
        A1_abs = np.abs(A1)
        alpha_T = float(np.max(A1_abs))
        t_alpha = float(times[int(np.argmax(A1_abs))])
        eta_T = safe_ratio(alpha_T, T * beta0)

        A1_bound = times * beta0
        positive_t = times > 0
        if beta0 > 1e-14:
            A1_bound_ratio_max = float(np.max(A1_abs[positive_t] / A1_bound[positive_t]))
        else:
            A1_bound_ratio_max = float("nan")

        H_small = H0 + eps_small * B
        amp_small = amplitude_timeseries(H_small, times, s, ell)
        pred_small = eps_small * A1
        first_order_error = amp_small - pred_small

        H_report = H0 + eps_report * B
        amp_report = amplitude_timeseries(H_report, times, s, ell)
        prob_report = np.abs(amp_report) ** 2

        moments = moment_sequence(H_report, s, ell, max_k=n - 1)
        max_moment_abs = float(max(abs(m) for m in moments))
        for k, m in enumerate(moments):
            moment_rows.append({
                "test": "Test 6 target-resolved sector-breaking",
                "scenario": scenario,
                "epsilon": eps_report,
                "k": k,
                "moment_real": float(np.real(m)),
                "moment_imag": float(np.imag(m)),
                "moment_abs": float(abs(m)),
                "n": n,
                "source_s": s,
                "target_ell": ell,
            })

        max_amp_small = float(np.max(np.abs(amp_small)))
        max_pred_small = float(np.max(np.abs(pred_small)))
        max_first_order_abs_error = float(np.max(np.abs(first_order_error)))
        relative_first_order_error = safe_ratio(max_first_order_abs_error, max_pred_small)

        max_amp_report = float(np.max(np.abs(amp_report)))
        max_prob_report = float(np.max(prob_report))
        avg_prob_report = float(np.trapz(prob_report, times) / T)

        Ebreak_small_dimless = float(abs(eps_small) * beta0)
        Ebreak_report_dimless = float(abs(eps_report) * beta0)
        mbreak_small_kg_if_rad_per_s = float(HBAR * Ebreak_small_dimless / (C_LIGHT ** 2))
        mbreak_report_kg_if_rad_per_s = float(HBAR * Ebreak_report_dimless / (C_LIGHT ** 2))

        eps_alpha_small = float(abs(eps_small) * alpha_T)
        eps_alpha_report = float(abs(eps_report) * alpha_T)

        if beta0 < 1e-12 and alpha_T < 1e-10 and max_amp_report < 1e-10:
            classification = "sector_preserving_zero"
        elif beta0 > 1e-12 and alpha_T < 1e-10 and max_amp_report < 1e-10:
            classification = "sector_broken_target_dark"
        elif beta0 > 1e-12 and alpha_T > 1e-10 and max_amp_report > 1e-5:
            classification = "sector_broken_target_effective"
        else:
            classification = "mixed_or_check"

        status = (
            "PASS"
            if (
                source_error < 1e-10
                and target_error < 1e-10
                and comm_H0_P0 < 1e-10
                and (np.isnan(A1_bound_ratio_max) or A1_bound_ratio_max <= 1.0 + 1e-9)
                and max_first_order_abs_error <= 5e-6
            )
            else "CHECK"
        )

        summary_rows.append({
            "test": "Test 6 target-resolved sector-breaking",
            "scenario": scenario,
            "family": family,
            "description": scen["description"],
            "n": n,
            "source_s": s,
            "target_ell": ell,
            "T": T,
            "rank_P0_krylov_H0": rank_P0,
            "comm_H0_P0_fro": comm_H0_P0,
            "source_containment_error": source_error,
            "target_exclusion_error": target_error,
            "beta0_Bperp_operator_norm": beta0,
            "alpha_T_max_abs_A1": alpha_T,
            "t_at_alpha_T": t_alpha,
            "eta_T_alpha_over_T_beta": eta_T,
            "A1_bound_ratio_max": A1_bound_ratio_max,
            "eps_small": eps_small,
            "Ebreak_small_dimensionless": Ebreak_small_dimless,
            "mbreak_small_kg_if_B_units_rad_per_s": mbreak_small_kg_if_rad_per_s,
            "eps_alpha_small": eps_alpha_small,
            "max_actual_amp_small": max_amp_small,
            "max_first_order_prediction_small": max_pred_small,
            "max_first_order_abs_error_small": max_first_order_abs_error,
            "relative_first_order_error_small": relative_first_order_error,
            "eps_report": eps_report,
            "Ebreak_report_dimensionless": Ebreak_report_dimless,
            "mbreak_report_kg_if_B_units_rad_per_s": mbreak_report_kg_if_rad_per_s,
            "eps_alpha_report": eps_alpha_report,
            "max_actual_amp_report": max_amp_report,
            "max_actual_probability_report": max_prob_report,
            "avg_actual_probability_report": avg_prob_report,
            "max_moment_abs_k0_to_nminus1_at_report_epsilon": max_moment_abs,
            "classification": classification,
            "status": status,
        })

        if family == "random_beta1" or scenario in (
            "original_C8_reflection_breaking_diag",
            "original_C8_direct_target_coupling",
            "extended_C8_aux_channel",
        ):
            efficiency_rows.append({
                "test": "Test 6 target-resolved sector-breaking",
                "scenario": scenario,
                "family": family,
                "beta0_Bperp_operator_norm": beta0,
                "alpha_T_max_abs_A1": alpha_T,
                "eta_T_alpha_over_T_beta": eta_T,
                "t_at_alpha_T": t_alpha,
                "eps_report": eps_report,
                "Ebreak_report_dimensionless": Ebreak_report_dimless,
                "eps_alpha_report": eps_alpha_report,
                "max_actual_probability_report": max_prob_report,
                "avg_actual_probability_report": avg_prob_report,
                "classification": classification,
            })

        keep_timeseries = (
            family == "structured"
            or scenario in ("original_C8_random_cross_beta1_1", "original_C8_random_cross_beta1_2")
        )
        if keep_timeseries:
            for t, a1, asmall, pred, err, areport, preport in zip(
                times, A1, amp_small, pred_small, first_order_error, amp_report, prob_report
            ):
                timeseries_rows.append({
                    "test": "Test 6 target-resolved sector-breaking",
                    "scenario": scenario,
                    "family": family,
                    "t": float(t),
                    "beta0_Bperp_operator_norm": beta0,
                    "A1_real": float(np.real(a1)),
                    "A1_imag": float(np.imag(a1)),
                    "A1_abs": float(abs(a1)),
                    "A1_bound_t_beta0": float(t * beta0),
                    "eps_small": eps_small,
                    "actual_small_amp_real": float(np.real(asmall)),
                    "actual_small_amp_imag": float(np.imag(asmall)),
                    "actual_small_amp_abs": float(abs(asmall)),
                    "first_order_pred_small_real": float(np.real(pred)),
                    "first_order_pred_small_imag": float(np.imag(pred)),
                    "first_order_pred_small_abs": float(abs(pred)),
                    "first_order_error_real": float(np.real(err)),
                    "first_order_error_imag": float(np.imag(err)),
                    "first_order_error_abs": float(abs(err)),
                    "eps_report": eps_report,
                    "actual_report_amp_real": float(np.real(areport)),
                    "actual_report_amp_imag": float(np.imag(areport)),
                    "actual_report_amp_abs": float(abs(areport)),
                    "actual_report_probability": float(preport),
                })

    summary_path = out_dir / "test6_target_resolved_summary.csv"
    timeseries_path = out_dir / "test6_first_order_timeseries.csv"
    efficiency_path = out_dir / "test6_efficiency_comparison.csv"
    moment_path = out_dir / "test6_moment_audit.csv"

    with summary_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary_rows[0].keys()))
        writer.writeheader()
        writer.writerows(summary_rows)

    with timeseries_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(timeseries_rows[0].keys()))
        writer.writeheader()
        writer.writerows(timeseries_rows)

    with efficiency_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(efficiency_rows[0].keys()))
        writer.writeheader()
        writer.writerows(efficiency_rows)

    with moment_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(moment_rows[0].keys()))
        writer.writeheader()
        writer.writerows(moment_rows)

    readme_path = out_dir / "test6_README.md"
    readme_path.write_text("""# Test 6: target-resolved sector-breaking

## Purpose

This test separates two quantities:

```text
beta0(B) = ||P0 B Q0 + Q0 B P0||
```

where `P0 = P_s^{H0}` is the unperturbed source-generated Krylov projector, from:

```text
alpha_T(B) = max_{t in [0,T]} |A1(t)|
```

where:

```text
A1(t) = -i int_0^t <ell| exp[-i(t-tau)H0] B_perp exp[-i tau H0] |s> d tau
```

`beta0(B)` measures total canonical sector-breaking.  
`alpha_T(B)` measures target-resolved first-order leakage.

## Interpretation

The mass-equivalent remains tied only to the sector-breaking energy scale:

```text
E_break^can = |epsilon| beta0(B)
m_break^can = E_break^can / c^2
```

or, for angular-frequency Hamiltonians:

```text
m_break^can = hbar |epsilon| beta0(B) / c^2
```

`alpha_T(B)` is not a mass. It tells whether the sector-breaking channel is target-effective over the finite time window.

## Key diagnostic

```text
eta_T(B) = alpha_T(B) / (T beta0(B))
```

Since the bound gives:

```text
alpha_T(B) <= T beta0(B)
```

we expect:

```text
0 <= eta_T(B) <= 1
```

for nonzero beta0.

## Expected lessons

- Sector-preserving perturbation: beta0 = 0 and alpha_T = 0.
- Reachable perturbation: beta0 > 0 and alpha_T > 0.
- Auxiliary-channel perturbation: beta0 > 0 but alpha_T approximately 0.
- Random perturbations normalized to beta0 = 1 can have different alpha_T and eta_T.

## Files

- `test6_target_resolved_sector_breaking.py`: self-contained script.
- `test6_target_resolved_summary.csv`: summary by scenario.
- `test6_first_order_timeseries.csv`: A1, actual small-epsilon amplitude, first-order prediction, and errors.
- `test6_efficiency_comparison.csv`: beta0-normalized target-efficiency comparison.
- `test6_moment_audit.csv`: finite moment audit at report epsilon.
- `test6_first_order_vs_actual.png`: first-order prediction against actual small-epsilon amplitude.
- `test6_beta_vs_alpha.png`: beta0 versus alpha_T.
- `test6_target_efficiency.png`: eta_T comparison.
""")

    first_order_plot_path = out_dir / "test6_first_order_vs_actual.png"
    beta_alpha_plot_path = out_dir / "test6_beta_vs_alpha.png"
    efficiency_plot_path = out_dir / "test6_target_efficiency.png"

    try:
        import matplotlib.pyplot as plt

        selected = [
            "original_C8_reflection_breaking_diag",
            "original_C8_direct_target_coupling",
            "extended_C8_aux_channel",
        ]
        plt.figure(figsize=(9, 5))
        for scenario in selected:
            rows = [r for r in timeseries_rows if r["scenario"] == scenario]
            xs = [r["t"] for r in rows]
            actual = [r["actual_small_amp_abs"] for r in rows]
            pred = [r["first_order_pred_small_abs"] for r in rows]
            plt.plot(xs, actual, label=f"{scenario} actual")
            plt.plot(xs, pred, linestyle="--", label=f"{scenario} first-order")
        plt.xlabel("time")
        plt.ylabel("amplitude magnitude, epsilon=1e-4")
        plt.title("Test 6: first-order target leakage prediction")
        plt.legend(fontsize=7)
        plt.tight_layout()
        plt.savefig(first_order_plot_path, dpi=200)
        plt.close()

        plt.figure(figsize=(8, 5))
        for row in summary_rows:
            plt.scatter(row["beta0_Bperp_operator_norm"], row["alpha_T_max_abs_A1"])
            label = row["scenario"].replace("original_C8_", "").replace("extended_C8_", "")
            plt.text(row["beta0_Bperp_operator_norm"], row["alpha_T_max_abs_A1"], label, fontsize=6)
        plt.xlabel("beta0 = ||B_perp(P0)||")
        plt.ylabel("alpha_T = max |A1(t)|")
        plt.title("Test 6: total sector-breaking versus target-resolved leakage")
        plt.tight_layout()
        plt.savefig(beta_alpha_plot_path, dpi=200)
        plt.close()

        plt.figure(figsize=(10, 5))
        labels = [r["scenario"] for r in efficiency_rows]
        values = [r["eta_T_alpha_over_T_beta"] for r in efficiency_rows]
        plt.bar(range(len(values)), values)
        plt.xticks(range(len(labels)), labels, rotation=60, ha="right", fontsize=7)
        plt.ylabel("eta_T = alpha_T / (T beta0)")
        plt.title("Test 6: target efficiency of sector-breaking channel")
        plt.tight_layout()
        plt.savefig(efficiency_plot_path, dpi=200)
        plt.close()

    except Exception as exc:
        first_order_plot_path.write_text(f"Plot generation failed: {exc}\n")
        beta_alpha_plot_path.write_text(f"Plot generation failed: {exc}\n")
        efficiency_plot_path.write_text(f"Plot generation failed: {exc}\n")

    return {
        "script": out_dir / "test6_target_resolved_sector_breaking.py",
        "summary": summary_path,
        "timeseries": timeseries_path,
        "efficiency": efficiency_path,
        "moment_audit": moment_path,
        "readme": readme_path,
        "first_order_plot": first_order_plot_path,
        "beta_alpha_plot": beta_alpha_plot_path,
        "efficiency_plot": efficiency_plot_path,
    }


if __name__ == "__main__":
    outputs = run_test(Path("/mnt/data"))
    for key, path in outputs.items():
        print(f"{key}: {path}")
