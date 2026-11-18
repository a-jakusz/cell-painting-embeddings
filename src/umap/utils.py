import numpy as np
from scipy.stats import gaussian_kde
import plotly.graph_objects as go
import polars as pl

def average_among_well(df):
    # 3 sites -> one embedding
    keys = ['source', 'batch', 'compound', 'plate', 'well']
    cols = [f"e{i}" for i in range(len(df['embedding'][0]))]
    return (
        # divide embedding on single elements -> mean -> construct embedding back
        df.with_columns(pl.col('embedding').list.to_struct(fields=cols))
        .unnest('embedding')
        .group_by(keys, maintain_order=True)
        .agg(pl.col(cols).mean())
        .select(*keys, pl.concat_list(cols).alias('embedding'))
    )

def normalize_by_dmso(df):
    # DMSO -- common starting point
    cols = [f"e{i}" for i in range(len(df['embedding'][0]))]
    dmso_mean = lambda c: pl.col(c).filter(pl.col('compound') == 'dmso').mean().over('plate')
    return (
        df.with_columns(pl.col('embedding').list.to_struct(fields=cols))
        .unnest('embedding')
        .with_columns([pl.col(c) - dmso_mean(c) for c in cols])
        .with_columns(pl.concat_list(cols).alias('embedding'))
        .drop(cols)
    )

def kde_dmso(emb_umap, compounds, fig):
    is_dmso = compounds == 'dmso'
    x, y = emb_umap[is_dmso, 0], emb_umap[is_dmso, 1]
    kde = gaussian_kde(np.vstack([x, y]))

    n = 3
    xi = np.linspace(x.min()-n, x.max()+n, 200)
    yi = np.linspace(y.min()-n, y.max()+n, 200)
    X, Y = np.meshgrid(xi, yi)
    Z = kde(np.vstack([X.ravel(), Y.ravel()])).reshape(X.shape)

    fig.add_trace(go.Contour(
        x=xi, y=yi, z=Z,
        colorscale="Blues", ncontours=20,
        contours=dict(coloring="heatmap"),
        opacity=0.5, showscale=False, 
        name="dmso", hoverinfo='skip',
        )
    )
    return fig