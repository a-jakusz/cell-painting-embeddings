import matplotlib.colors as mpl  # noqa: CPY001
import numpy as np
from jump_portrait.fetch import get_item_location_metadata, get_jump_image
from matplotlib import pyplot as plt

def display_site(
    source: str,
    batch: str,
    plate: str,
    well: str,
    site: int,
    label: str,
    int_percentile: float,
) -> None:
    """Plot all channels from one image.

    Parameters
    ----------
    source : String
        Source ID for image of interest.
    batch : String
        Batch ID for image of interest.
    plate : String
        Plate ID for image of interest.
    well : String
        Well ID for image of interest.
    site : String
        Site ID for image of interest.
    label : String
        Label to display in lower left corner.
    int_percentile: float
        Rescale the image from 0 - this percentile of intensity values.

    """
    n_rows = 2
    n_cols = 3

    # Make images
    axes = plt.subplots(n_rows, n_cols, figsize=(2.6 * n_cols, 2.6 * n_rows))[1]
    axes = axes.ravel()

    channel_rgb = {
        "AGP": "#FF7F00",  # Orange
        "DNA": "#0000FF",  # Blue
        "ER": "#00FF00",  # Green
        "Mito": "#FF0000",  # Red
        "RNA": "#FFFF00",  # Yellow
    }

    for ax, (channel, rgb) in zip(axes, channel_rgb.items()):
        cmap = mpl.LinearSegmentedColormap.from_list(channel, ("#000", rgb))

        img = get_jump_image(source, batch, plate, well, channel, site)

        ax.imshow(img, vmin=0, vmax=np.percentile(img, int_percentile), cmap=cmap)
        ax.axis("off")

        # Add channel name label in the top left corner
        ax.text(
            0.05,
            0.95,
            channel,
            horizontalalignment="left",
            verticalalignment="top",
            fontsize=18,
            color="black",
            bbox=dict(
                facecolor="white", alpha=0.8, edgecolor="none", boxstyle="round,pad=0.3"
            ),
            transform=ax.transAxes,
        )

    # put label in last subplot
    ax = axes[-1]
    ax.text(
        0.5,
        0.5,
        label,
        horizontalalignment="center",
        verticalalignment="center",
        fontsize=20,
        color="black",
        transform=ax.transAxes,
    )
    ax.axis("off")

    # show plot
    plt.tight_layout()