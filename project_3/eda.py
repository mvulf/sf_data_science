import pandas as pd

# Visualization Libs
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

def box_hist_plot(data: pd.DataFrame, x: str, title: str, hist_kde=False, hist_yscale='linear', box_showmeans=True, height_ratios=(.15, .85)) -> matplotlib.figure.Figure:
    """Plot Seaborn boxplot and histplot one above the other

    Args:
        data (pd.DataFrame): Data for plotting
        x (str): Columns name for plotting
        title (str): Figure (plot) name
        hist_kde (bool): If True, compute a Kernel Density Estimate. Defaults to False.
        hist_yscale (str): Hist count axis Scale. Defaults to 'linear'.
        box_showmeans (bool): Show mean-value point with the marker. Defaults to True.
        height_ratios (tuple): Height ratios of the boxplot and histplot. Defaults to (.15, .85).

    Returns:
        matplotlib.figure.Figure: Figure with seaborn boxplot and hitstplot
    """
    # Create a figure composed of two axes objects
    f, (ax_box, ax_hist) = plt.subplots(2, sharex=True, 
        gridspec_kw={
            'height_ratios': height_ratios
    })
    # Set up figure
    f.suptitle(title);
    f.tight_layout()

    # Plot boxplot
    sns.boxplot(data=data, x=x, showmeans=box_showmeans, 
                meanprops={"marker":"1",
                        "markeredgecolor":"white",
                        "markersize":"10"}, 
                ax=ax_box)
    ax_box.set(xlabel=None)

    # Plot histplot
    sns.histplot(data=data, x=x, kde=hist_kde, ax=ax_hist)
    ax_hist.set_yscale(hist_yscale)
    plt.close(f)    
    # Return figure
    return f