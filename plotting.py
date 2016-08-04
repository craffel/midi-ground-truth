""" Functions for simply pretty plotting. """

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('white')
import numpy as np
import matplotlib

FC = '#28ABE3'


def plot_hist(data, bins, xlabel=None, ylabel=None, divisor=1000):
    fig = plt.figure()
    # Make it so that all points beyond the bin range get put in the last bin
    data = np.array(data)
    data[data > bins[-1]] = bins[-1] - 1e-10
    # Get histogram bin heights
    heights, _ = np.histogram(data, bins)
    # If the largest difference in heights is more than 20x the median
    # distance in heights, use a split histogram
    height_diffs = np.abs(np.diff(heights))
    if np.median(height_diffs) * 20 < height_diffs.max():
        # Find all bin indices which are > .5*highest bin
        highest = max(heights)
        high_bin_indices = [n for n in range(len(heights))
                            if heights[n] > highest / 2.]
        split_hist(heights, bins, high_bin_indices)
    else:
        pretty_hist(heights, bins)
        divide_yticklabels(divisor=divisor)
    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        # When a split histogram is created, ylabel draws in the middle of the
        # bottom histogram - this standardizes the location regardless
        fig.text(0.05, 0.5, ylabel, ha='center', va='center',
                 rotation='vertical')


def uniform_hist(heights, bins, ax, **kwargs):
    ax.bar(left=np.arange(len(bins) - 1) - .5, height=heights,
           width=1, bottom=0, **kwargs)


def pretty_hist(heights, bins, ax=None, title=None):
    """ Utility method for plotting a nice histogram """
    # If no axis was provided, get current axis
    if ax is None:
        ax = plt.gca()
    # Plot histogram, with specific coloring and axis-alignment
    uniform_hist(heights, bins, ax, fc=FC, alpha=.7)
    # Remove spines from plot
    sns.despine()
    # Add grid to y axis
    ax.yaxis.grid()
    # Set the plotting range to fit the histogram exactly
    bin_spacing = 1.
    ax.set_xlim(-bin_spacing / 2., len(bins) - 1 - bin_spacing / 2.)
    if title is not None:
        plt.suptitle(title, verticalalignment='top', y=.95, size='large')


def divide_yticklabels(ax=None, divisor=1000):
    """ Utility method to scale down all y tick labels """
    # If no axis was provided, get current axis
    if ax is None:
        ax = plt.gca()
    ax.set_yticklabels([int(float(t) / divisor)
                        if (float(t) / divisor).is_integer()
                        else float(t) / divisor
                        for t in ax.get_yticks()])


def split_hist(heights, bin_edges, high_bin_indices, divisor=1000):
    """ Plot a histogram where one or more bins have very large values """
    # Make high_bin_indices a list if an int was passed
    if isinstance(high_bin_indices, int):
        high_bin_indices = [high_bin_indices]
    # Create 2-row, 1-col subplot where the upper sublot is 1/4 the height
    # The upper subplot will be the tops of the very large bins; lower will be
    # the rest
    gs = matplotlib.gridspec.GridSpec(
        2, 1, width_ratios=[1], height_ratios=[1, 4])
    # Set the spacing between subplots to .1
    gs.update(hspace=0.1)
    # Grab axes handles
    ax = plt.subplot(gs[0])
    ax2 = plt.subplot(gs[1])
    # Plot pretty histograms both for the "upper" and "lower" parts of split
    pretty_hist(heights, bin_edges, ax)
    pretty_hist(heights, bin_edges, ax2)
    low_min = 0
    # Compute the height of the largest bin _not_ in high_bin_indices
    low_max = 1.1 * max(heights[n] for n in range(len(bin_edges) - 1)
                        if n not in high_bin_indices)
    # Compute the height of the smallest bin in high_bin_indices
    high_min = .9 * min(heights[n] for n in high_bin_indices)
    # Compute the height of the highest bin in high_bin_indices
    high_max = 1.1 * max(heights[n] for n in high_bin_indices)
    # Set the Y plotting range according to the above.  This will crop things.
    ax.set_ylim(high_min, high_max)
    ax2.set_ylim(low_min, low_max)
    # Hide the spines between ax and ax2
    ax.spines['bottom'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax.xaxis.tick_top()
    ax.tick_params(labeltop='off')
    ax2.xaxis.tick_bottom()

    # Compute the spacing between y-ticks on the lower plot
    lowtick_spacing = np.diff(ax2.get_yticks())[0]
    # Create a single tick on the upper plot, rounded to the same spacing as
    # lower plot
    ax.set_yticks([int(lowtick_spacing) *
                   int((high_min + high_max) /
                   (2 * lowtick_spacing))])
    # X-axis start of clip lines (relative to [0, 1])
    start = -.015
    # Compute proportion of x-axis covered by last high_bin_indices (+ .015)
    end = (high_bin_indices[-1] + 1) / float(len(bin_edges) - 1) + .015
    # Plot the lines, allowing for it to expand outside of the axis
    ax.plot([start, end], [0., 0.],
            transform=ax.transAxes, color='k', clip_on=False)
    ax2.plot([start, end], [1., 1.],
             transform=ax2.transAxes, color='k', clip_on=False)

    # Convert count to thousands
    divide_yticklabels(ax, divisor)
    divide_yticklabels(ax2, divisor)
