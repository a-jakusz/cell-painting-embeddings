# Сell Painting Embeddings (GMUM - Interpretable Drug Discovery)

Comparing learned (CLOOME) and hand-crafted (CellProfiler) representations of
cell images from the [JUMP Cell Painting](https://broadinstitute.github.io/jump_hub/) dataset.

## Goal

Cells treated with a chemical compound change their appearance. This project
asks how well two different representations of that change capture it:

- **CLOOME**: image embeddings from a pretrained contrastive model
  ([paper](https://www.nature.com/articles/s41467-023-42328-w),
  [code](https://github.com/ml-jku/cloome))
- **CellProfiler**: classical morphological profiles supplied with JUMP

## Data

- 20 compounds from JUMP (U2OS cells), chosen to cover strong, weak and no
  expected phenotype, plus DMSO negative controls
- Both representations aggregated to one vector per well, matched by
  source, plate and well

## Pipeline

1. **Select and download**: find the compounds in JUMP, download 5-channel images
2. **Embed**: compute CLOOME image embeddings
3. **Visualise**: UMAP, one colour per compound, KDE for DMSO
4. **Compare**: same plots for CellProfiler profiles, matched per well
5. **Cluster**: cluster CellProfiler profiles and show example images per cluster

## Stack

Python, managed with [uv](https://docs.astral.sh/uv/) (`uv sync`).
Data: polars · Images: jump-portrait, tifffile · Embeddings: CLOOME (PyTorch)
Analysis: umap-learn, scikit-learn, scipy · Plots: plotly

## Status

Work in progress.