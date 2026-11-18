import umap
import polars as pl
import numpy as np
import plotly.express as px
from src.umap.utils import kde_dmso, average_among_well, normalize_by_dmso

def build_umap():
    # reducer = umap.UMAP(metric='cosine', random_state=1)
    reducer = umap.UMAP(metric='euclidean', random_state=1)

    df = pl.read_parquet("data/embeddings/embs.parquet")
    df = average_among_well(df)
    df = normalize_by_dmso(df)

    emb = np.array(df["embedding"].to_list())

    emb_umap = reducer.fit_transform(emb)

    compounds = df['compound'].to_numpy()
    plates = df['plate'].to_numpy()
    wells = df['well'].to_numpy()
    # sites = df['site'].to_numpy()

    is_dmso = compounds == 'dmso'
    fig = px.scatter(
        x=emb_umap[~is_dmso, 0], y=emb_umap[~is_dmso, 1], 
        color=compounds[~is_dmso], 
        color_discrete_sequence=px.colors.qualitative.Alphabet
    )
    # fig = px.scatter(x=emb_umap[~is_dmso, 0], y=emb_umap[~is_dmso, 1], color=plates[~is_dmso], color_discrete_sequence=px.colors.qualitative.Alphabet)

    # kde
    fig = kde_dmso(emb_umap, compounds, fig)

    fig.show()

build_umap()