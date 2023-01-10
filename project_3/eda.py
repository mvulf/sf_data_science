import pandas as pd
import math
import numpy as np

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


def get_bins_categories(series: pd.Series, bins_num: int, 
    method: str='')->pd.Series:
    """Retrieve categorical series from numerical with ordered int labels

    Args:
        series (pd.Series): Source series
        bins_num (int): Number of bins
        method (str): Method of cutting: 
            default '' - linear bins
            quantiles - by quantiles

    Returns:
        pd.Series: The result of source series cutting - 
        ordered categorical Series
    """
    # Get bins
    if method=='quantiles':
        bins = [series.min()]
        bins.extend([series\
            .quantile(q=x/10) for x in list(range(1,bins_num))])
        bins.append(series.max())
    else:
        bins = list(np.linspace(series.min(), series.max(), bins_num+1))
        
    # Get labels
    labels=list(range(0,bins_num))
    
    # Cut Series
    return pd.cut(series, bins=bins, labels=labels)


# GET EARTH DISTANCE
# Earh radius in km
r = 6371.0 # km

def hav(theta:float)->float:
    """haversin function

    Args:
        theta (float): delta between two angles

    Returns:
        float: haversin
    """
    return math.sin(theta/2)**2

def to_rad(theta_deg:float)->float:
    """Convert degrees to radians

    Args:
        theta_deg (float): angle in degrees

    Returns:
        float: _description_
    """
    return theta_deg/180 * math.pi
to_rad_np = np.vectorize(to_rad)

def hav_distance(lat_1:float, lng_1:float, lat_2:float, lng_2:float)->float:
    """Calculate distance in km between two point on the Earth 
    by the haversin formula

    Args:
        lat_1 (float): First point lattitude
        lng_1 (float): First point longitute
        lat_2 (float): Second point lattitude
        lng_2 (float): Second point longitute

    Returns:
        float: Earth distance in km
    """
    coordinates = to_rad_np(np.array([
        [lat_1, lng_1],
        [lat_2, lng_2]
    ]))
    
    if np.isnan(coordinates).any():
        return np.nan
    
    return 2*r*math.asin(math.sqrt(hav(coordinates[1,0] - coordinates[0,0]) +\
    math.cos(coordinates[0,0])*math.cos(coordinates[1,0])*\
        hav(coordinates[1,1] - coordinates[0,1])))