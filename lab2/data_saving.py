import csv
import os
import numpy as np
import pandas as pd
from IPython.display import display
import matplotlib.pyplot as plt
def save_result_csv(result, filename="results.csv"):
    # Ensure numpy numbers are converted
    result = {
        k: float(v) if isinstance(v, (np.floating, np.integer)) else v
        for k, v in result.items()
    }

    # Determine if we need to write the header
    write_header = not os.path.isfile(filename) or os.path.getsize(filename) == 0

    with open(filename, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=result.keys())
        if write_header:
            writer.writeheader()
        writer.writerow(result)


def load_result_csv(filename="results.csv"):
    return pd.read_csv(filename)

def visualize_csv_table(df, max_rows=10):
    """
    Visualize CSV data as a clean table (head of the DataFrame).
    """
    display(df.head(max_rows))

def plot_multiple_csv(
    dfs,
    labels,
    x_col,
    y_col,
    title="CSV Comparison Plot"
):
    """
    Plot multiple CSV datasets on the same graph.
    
    Assumes all DataFrames contain x_col and y_col.
    """
    plt.figure(figsize=(10, 6))

    for df, label in zip(dfs, labels):
        plt.plot(
            df[x_col],
            df[y_col],
            linewidth=2,
            label=label
        )

    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()

