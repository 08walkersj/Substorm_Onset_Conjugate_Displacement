import numpy as np

def add_boxkey(axis, size=8, x_center=.175, scale=False, ypos=9.5, xshift=0, width=.8, boxplotkwargs={}, y_offset=0.1, sample_data=False, **text_kwargs):
    """
    Adds a box plot key to a given axis and labels key components such as the median, quartiles, and outliers.

    Parameters:
    -----------
    axis : matplotlib axis
        The axis object to draw the box plot on.
    size : int, optional
        Font size for the text labels (default is 8).
    x_center : float, optional
        Controls the centering of the box plot data (default is 0.175).
    scale : bool or float, optional
        Determines the spread of the sample data, either a float or calculated automatically (default is False).
    ypos : float, optional
        Position on the y-axis where the box plot will be placed (default is 9.5).
    xshift : float, optional
        Shifts the sample data along the x-axis (default is 0).
    width : float, optional
        Width of the box plot (default is 0.8).
    boxplotkwargs : dict, optional
        Additional keyword arguments passed to the `axis.boxplot` function (default is {}).
    y_offset : float, optional
        Vertical offset for text labels (default is 0.1).
    sample_data : array or bool, optional
        Custom sample data to be used in the box plot. If False, synthetic data is generated (default is False).
    **text_kwargs : dict
        Additional keyword arguments passed to the `axis.text` function for text styling.
    
    Returns:
    --------
    sample_boxplot : dict
        A dictionary containing the artists of the box plot components (e.g., medians, boxes, whiskers, etc.).
    text : list
        A list of `matplotlib.text.Text` objects representing the text annotations added to the box plot.
    """

    # If no sample_data is provided, create synthetic data
    if not sample_data:
        np.random.seed(342314)  # Set a random seed for reproducibility
        if not scale:
            # If no scale is provided, calculate it based on x_center
            scale = .03 * (x_center / .175)
        # Generate synthetic data based on two normal distributions
        sample_data = (np.random.normal(.2, scale=scale, size=(100,)) + 
                       np.random.normal(.15, scale=scale, size=(100,))) * (x_center / .175)
        # Adjust the first data point downward
        sample_data[0] -= .15 * (x_center / .175)
        # Apply x-axis shift to the data
        sample_data += xshift

    # Define default boxplot settings with horizontal orientation and mean line
    boxkwargs = dict(vert=False, showmeans=True, meanline=True, 
                     positions=[ypos], widths=width)
    # Update boxplot settings with any additional user-provided keyword arguments
    boxkwargs.update(boxplotkwargs)

    # Default text settings, including font size
    txt_kwargs = {'size': size}
    # Update text settings with any additional user-provided keyword arguments
    txt_kwargs.update(text_kwargs)

    # Create the box plot on the provided axis with the sample data
    sample_boxplot = axis.boxplot(sample_data, **boxkwargs)

    # Add text labels to annotate key components of the box plot
    text = [
        axis.text(sample_boxplot['medians'][0].get_xdata()[0], sample_boxplot['medians'][0].get_ydata()[0],
                  s='Median', ha='center', va='top', color=sample_boxplot['medians'][0].get_color(), **txt_kwargs),
        axis.text(sample_boxplot['boxes'][0].get_xdata()[0], sample_boxplot['boxes'][0].get_ydata()[0] - y_offset * 3,
                  s='Lower\nQuartile', ha='center', va='top', color=sample_boxplot['boxes'][0].get_color(), **txt_kwargs),
        axis.text(sample_boxplot['boxes'][0].get_xdata()[-2], sample_boxplot['boxes'][0].get_ydata()[-2] - y_offset * 3,
                  s='Upper\nQuartile', ha='center', va='top', color=sample_boxplot['boxes'][0].get_color(), **txt_kwargs),
        axis.text(sample_boxplot['means'][0].get_xdata()[0], sample_boxplot['means'][0].get_ydata()[-1],
                  s='Mean', ha='center', va='bottom', color=sample_boxplot['means'][0].get_color(), **txt_kwargs),
        axis.text(sample_boxplot['caps'][0].get_xdata()[0], sample_boxplot['caps'][0].get_ydata()[-1],
                  s='Minimum', ha='center', va='bottom', color=sample_boxplot['caps'][0].get_color(), **txt_kwargs),
        axis.text(sample_boxplot['caps'][1].get_xdata()[0], sample_boxplot['caps'][1].get_ydata()[-1],
                  s='Maximum', ha='center', va='bottom', color=sample_boxplot['caps'][1].get_color(), **txt_kwargs),
        axis.text(sample_boxplot['fliers'][0].get_xdata()[0], sample_boxplot['fliers'][0].get_ydata()[-1] + y_offset,
                  s='Outliers', ha='center', va='bottom', color=sample_boxplot['fliers'][0].get_color(), **txt_kwargs)
    ]

    # Return both the box plot object and the text annotations
    return sample_boxplot, text
