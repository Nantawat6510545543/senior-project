import io
import matplotlib.pyplot as plt
from PIL import Image

def merge_figures_vertical(figs):
    if not figs:
        return None

    images = []

    # Convert each matplotlib fig → PIL image
    for fig in figs:
        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight")
        plt.close(fig)
        buf.seek(0)
        images.append(Image.open(buf).convert("RGB"))

    # Determine final canvas size
    width = max(img.width for img in images)
    height = sum(img.height for img in images)

    # Create blank canvas
    merged = Image.new("RGB", (width, height), "white")

    # Paste images vertically
    y_offset = 0
    for img in images:
        merged.paste(img, (0, y_offset))
        y_offset += img.height

    # Convert back → matplotlib figure
    dpi = 100
    fig = plt.figure(figsize=(width / dpi, height / dpi), dpi=dpi)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.imshow(merged)
    ax.axis("off")

    return fig
