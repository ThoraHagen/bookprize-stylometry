import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

rng = np.random.default_rng(42)

# ---------------------------------------------------------------------------
# controls_df
# nominees_df
# ---------------------------------------------------------------------------

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

controls_complete = controls_df[FEATURES].dropna().copy()
nominees_complete = nominees_df[FEATURES].dropna().copy()
print(f"Kontrollen: {len(controls_complete)}/{len(controls_df)} vollstaendig, "
      f"Nominierte: {len(nominees_complete)}/{len(nominees_df)} vollstaendig")

if "n_tokens" in FEATURES:
    controls_complete["n_tokens"] = np.log1p(controls_complete["n_tokens"])
    nominees_complete["n_tokens"] = np.log1p(nominees_complete["n_tokens"])

scaler = StandardScaler().fit(controls_complete)
pca = PCA(n_components=2, random_state=42).fit(scaler.transform(controls_complete))

controls_pc = pca.transform(scaler.transform(controls_complete))
nominees_pc = pca.transform(scaler.transform(nominees_complete))

gray_cmap = LinearSegmentedColormap.from_list("gray_density", ["#fcfcfb", "#c9c8c1", "#8a8880"])

fig, ax = plt.subplots(figsize=(9, 7))
fig.patch.set_facecolor("#fcfcfb")
ax.set_facecolor("#fcfcfb")

sns.kdeplot(
    x=controls_pc[:, 0], y=controls_pc[:, 1],
    fill=True, cmap=gray_cmap, levels=10, thresh=0.03,
    ax=ax, zorder=1,
)
ax.scatter(
    nominees_pc[:, 0], nominees_pc[:, 1],
    s=26, c="#2a78d6", alpha=0.8, linewidths=0, zorder=3,
    label=f"Nominees (n={len(nominees_pc)})",
)

ctrl_centroid = controls_pc.mean(axis=0)
nom_centroid = nominees_pc.mean(axis=0)
ax.annotate(
    "", xy=nom_centroid, xytext=ctrl_centroid, zorder=4,
    arrowprops=dict(arrowstyle="-|>", color="#0b0b0b", lw=1.5),
)
ax.scatter(*ctrl_centroid, marker="D", s=130, facecolor="#fcfcfb", edgecolor="#52514e",
           linewidth=1.8, zorder=5, label="Controls - mean")
ax.scatter(*nom_centroid, marker="D", s=130, facecolor="#2a78d6", edgecolor="#0b3d73",
           linewidth=1.8, zorder=5, label="Nominees - mean")

all_x = np.concatenate([controls_pc[:, 0], nominees_pc[:, 0]])
all_y = np.concatenate([controls_pc[:, 1], nominees_pc[:, 1]])
xlo, xhi = np.percentile(all_x, [0.5, 99.5])
ylo, yhi = np.percentile(all_y, [0.5, 99.5])
xpad, ypad = (xhi - xlo) * 0.08, (yhi - ylo) * 0.08
ax.set_xlim(xlo - xpad, xhi + xpad)
ax.set_ylim(ylo - ypad, yhi + ypad)

var1, var2 = pca.explained_variance_ratio_[:2] * 100
ax.set_xlabel(f"PC1 ({var1:.1f}% explained variance)", color="#0b0b0b")
ax.set_ylabel(f"PC2 ({var2:.1f}% explained variance)", color="#0b0b0b")
ax.set_title("PCA: Nominees vs. Control Group (Density)", color="#0b0b0b", fontsize=13)
ax.tick_params(colors="#52514e")
for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)
for spine in ["left", "bottom"]:
    ax.spines[spine].set_color("#c3c2b7")

ax.legend(frameon=False, loc="best")
plt.tight_layout()
plt.savefig("pca_nominierte_vs_kontrollen.png", dpi=300, facecolor="#fcfcfb", bbox_inches="tight")
plt.show()
