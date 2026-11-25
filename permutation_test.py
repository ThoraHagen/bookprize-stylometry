import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

# ---------------------------------------------------------------------------
# DataFrames with one column per text metric
# ---------------------------------------------------------------------------
# controls_df

# nominees_df


def percentile(x, ref):
    return 100 * (np.searchsorted(ref, x, "left") + np.searchsorted(ref, x, "right")) / (2 * len(ref))


def stats(p):
    return np.median(p), np.mean(np.abs(p - 50)), np.subtract(*np.percentile(p, [75, 25]))


def run_feature_test(nominee_vals, control_vals, rng, n_perm=10_000):
    """Permutation test for one feature.
    """
    nominee_vals = np.asarray(nominee_vals, dtype=float)
    control_vals = np.asarray(control_vals, dtype=float)
    nominee_vals = nominee_vals[~np.isnan(nominee_vals)]
    control_vals = control_vals[~np.isnan(control_vals)]

    ref = np.sort(control_vals)
    obs = stats(percentile(nominee_vals, ref))

    null = np.array([
        stats(percentile(rng.choice(control_vals, len(nominee_vals), replace=False), ref))
        for _ in range(n_perm)
    ])

    p_L = np.mean(np.abs(null[:, 0] - null[:, 0].mean()) >= abs(obs[0] - null[:, 0].mean()))
    p_T = np.mean(null[:, 1] <= obs[1])
    p_H = np.mean(null[:, 2] <= obs[2])

    return {
        "location": obs[0], "typicality": obs[1], "homogeneity": obs[2],
        "p_L": p_L, "p_T": p_T, "p_H": p_H,
        "n_nominees": len(nominee_vals), "n_controls": len(control_vals),
    }


def fdr_bh(pvals):
    """Benjamini-Hochberg correction"""
    pvals = np.asarray(pvals, dtype=float)
    n = len(pvals)
    order = np.argsort(pvals)
    ranked = pvals[order]

    q = ranked * n / (np.arange(1, n + 1))
    q = np.minimum.accumulate(q[::-1])[::-1]  # monoton erzwingen
    q = np.clip(q, 0, 1)

    q_final = np.empty(n)
    q_final[order] = q
    return q_final


FEATURES_KEEP = [
    "wienersachtextformel1", "n_tokens", "yulek", "ttr", "rttr", "maas",                   
    "mtld", "yulei",
    "relativeadjfrequency", "relativeadvfrequency", "relativeintjfrequency",
    "relativenounfrequency", "relativepropnfrequency", "relativeverbfrequency",
    "relativeadpfrequency", "relativeauxfrequency", "relativecconjfrequency",
    "relativedetfrequency", "relativenumfrequency", "relativepartfrequency",
    "relativepronfrequency", "relativesconjfrequency", "relativepunctfrequency",
    "relativexfrequency", "nominalstyleindex", "proportionfunctional", "lexicaldensity",
]

FEATURES = [f for f in FEATURES_KEEP if f in nominees_df.columns]

N_PERM = 10000

rows = []
for feat in FEATURES:
    res = run_feature_test(nominees_df[feat].to_numpy(), controls_df[feat].to_numpy(), rng, n_perm=N_PERM)
    res["feature"] = feat
    rows.append(res)

results = pd.DataFrame(rows).set_index("feature")

for col in ["p_L", "p_T", "p_H"]:
    results[f"{col}_fdr"] = fdr_bh(results[col].to_numpy())


pd.set_option("display.width", 200)
pd.set_option("display.max_columns", None)
pd.set_option("display.float_format", lambda v: f"{v:.3f}")
print(results[["location", "typicality", "homogeneity", "p_L", "p_L_fdr", "p_T", "p_T_fdr", "p_H", "p_H_fdr", "n_nominees", "n_controls"]])
