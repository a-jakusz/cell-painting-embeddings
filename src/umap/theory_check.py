import umap
import polars as pl
import numpy as np
import plotly.express as px
from src.umap.utils import average_among_well, normalize_by_dmso

def build_umap():
    # reducer = umap.UMAP(metric='cosine', random_state=1)
    reducer = umap.UMAP(metric='euclidean', random_state=1)

    df = pl.read_parquet("data/embeddings/embs.parquet")
    df = average_among_well(df)
    df = normalize_by_dmso(df)

    emb = np.array(df["embedding"].to_list())

    emb_umap = reducer.fit_transform(emb)

    # well names look like 'A02': row = letter, column = number
    df = df.with_columns(
        row=pl.col('well').str.slice(0, 1),
        col=pl.col('well').str.slice(1).cast(pl.Int32).cast(pl.Utf8),
        well_no=pl.col('well').rank('dense').over('compound', 'plate').cast(pl.Utf8),  # 1-3 inside compound
    )

    keep = (df['compound'] != 'dmso').to_numpy()   # compounds only, no dmso
    for color in ['row', 'col', 'well_no']:
        fig = px.scatter(
            x=emb_umap[keep, 0], y=emb_umap[keep, 1],
            color=df[color].to_numpy()[keep], title=f"colored by {color}",
        )
        fig.show()

build_umap()
