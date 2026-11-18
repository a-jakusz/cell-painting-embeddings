import umap
import polars as pl
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import gaussian_kde


reducer = umap.UMAP(metric='cosine', random_state=1)
# reducer = umap.UMAP(metric='euclidean', random_state=1)

df = pl.read_parquet("data/embeddings/embs.parquet")
emb = np.array(df["embedding"].to_list())
print(df)
print(emb)

emb_umap = reducer.fit_transform(emb)
print(emb_umap)

compounds = df['compound'].to_numpy()
plates = df['plate'].to_numpy()
wells = df['well'].to_numpy()
sites = df['site'].to_numpy()
print(np.unique(compounds))
cmap = plt.get_cmap("tab20") # 20 distinct colours
for i, c in enumerate(np.unique(compounds)):
    m = compounds == c
    plt.scatter(emb_umap[m, 0], emb_umap[m, 1], s=15, color=cmap(i % 20), label=c)

is_dmso = compounds == 'dmso'
fig = px.scatter(x=emb_umap[~is_dmso, 0], y=emb_umap[~is_dmso, 1], color=compounds[~is_dmso], color_discrete_sequence=px.colors.qualitative.Alphabet)
# fig = px.scatter(x=emb_umap[~is_dmso, 0], y=emb_umap[~is_dmso, 1], color=plates[~is_dmso], color_discrete_sequence=px.colors.qualitative.Alphabet)

# kde
x, y = emb_umap[is_dmso, 0], emb_umap[is_dmso, 1]
kde = gaussian_kde(np.vstack([x, y]))

n = 3
xi = np.linspace(x.min()-n, x.max()+n, 200)
yi = np.linspace(y.min()-n, y.max()+n, 200)
X, Y = np.meshgrid(xi, yi)
Z = kde(np.vstack([X.ravel(), Y.ravel()])).reshape(X.shape)

fig.add_trace(go.Contour(
    x=xi, y=yi, z=Z,
    colorscale="Blues", ncontours=40,
    contours=dict(coloring="heatmap"),
    opacity=0.5, showscale=False, 
    name="dmso", hoverinfo='skip',
    )
)

plt.title('test')
plt.show()
fig.show()