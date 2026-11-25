"""Small helpers shared by the notebooks."""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

DATA = "data/"

NAVY = "#0b2545"
BLUE = "#2a78d6"
SKY = "#9cc0ec"
ORANGE = "#eb6834"
GREEN = "#1baf7a"
RED = "#d03b3b"
GREY = "#c9c8c1"

plt.rcParams.update({
    "figure.figsize": (9, 4),
    "figure.dpi": 110,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "axes.grid.axis": "y",
    "axes.axisbelow": True,
    "grid.color": "#e6e4dd",
    "axes.titlelocation": "left",
    "axes.titleweight": "bold",
    "legend.frameon": False,
    "savefig.dpi": 150,
    "savefig.bbox": "tight",
})


def fiscal_year(dates):
    # Cottonil's year runs Oct -> Sep. Oct 2025 is FY2026.
    return np.where(dates.dt.month >= 10, dates.dt.year + 1, dates.dt.year)


def read(name, dates=None):
    return pd.read_csv(DATA + name, parse_dates=dates or [], low_memory=False)


def load_lines():
    """Sales lines with category, channel and fiscal year attached."""
    lines = read("sales_order_items.csv", dates=["order_date"])
    products = read("products_catalog.csv")[["product_id", "category_en"]]
    orders = read("sales_orders.csv")[["sales_order_id", "sales_channel", "customer_id"]]
    lines = lines.merge(products, on="product_id", how="left").merge(orders, on="sales_order_id", how="left")
    lines["FY"] = fiscal_year(lines["order_date"])
    return lines


def load_orders():
    orders = read("sales_orders.csv", dates=["order_date"])
    orders["FY"] = fiscal_year(orders["order_date"])
    return orders


def millions(x):
    return f"{x / 1e6:,.1f}M"


def save(name):
    plt.savefig(f"images/{name}.png")
