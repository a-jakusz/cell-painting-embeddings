import umap
import polars as pl
import numpy as np
import matplotlib.pyplot as plt

reducer = umap.UMAP()

df = pl.read_parquet("data/embeddings/embs.parquet")
emb = np.array(df["embedding"].to_list())
print(emb)

emb_umap = reducer.fit_transform(emb)

compounds = df["compound"].to_numpy()
print(compounds)
cmap = plt.get_cmap("tab20")                      # 20 distinct colours
for i, c in enumerate(np.unique(compounds)):
    m = compounds == c
    plt.scatter(emb_umap[m, 0], emb_umap[m, 1], s=15, color=cmap(i % 20), label=c)

plt.title('test')
plt.show()