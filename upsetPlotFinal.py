import pandas as pd
import matplotlib.pyplot as plt
from upsetplot import UpSet, from_memberships
import warnings

def generate_upset_plot(
    data_file,
    file_type='csv',
    sort_by='cardinality',
    show_counts='%d',
    max_intersections=15,
    min_values=None,
    figsize=(12, 8),
    element_size=40,
    intersection_plot_elements=6,
    font_size=12,
    label_rotation=45,
    **kwargs
):
    """
    Generates an UpSet plot from the given data file with improved readability.

    Parameters:
    - data_file: str
        Path to the data file (CSV or XLSX).
    - file_type: str, default 'csv'
        Type of the data file: 'csv' or 'xlsx'.
    - sort_by: str, default 'cardinality'
        Criteria to sort the intersections: 'cardinality' or 'degree'.
    - show_counts: str, default '%d'
        Format string for displaying counts on the plot.
    - max_intersections: int, default 15
        Maximum number of intersections to display.
    - min_values: float or int, optional
        Minimum figure for 'Values', that's not very intuititively named, which is the value to include an intersection.
    - figsize: tuple, default (12, 8)
        Size of the figure (width, height).
    - element_size: int, default 40
        Size of each element in the plot.
    - intersection_plot_elements: int, default 6
        Number of elements in the intersection plot (bars).
    - font_size: int, default 12
        Font size for the plot text.
    - label_rotation: int, default 45
        Rotation angle for the x-axis labels.
    - **kwargs:
        Additional keyword arguments passed to the UpSet plot.

    Returns:
    - None
        Displays the UpSet plot.
    """

    # Suppress FutureWarnings from pandas
    warnings.simplefilter(action='ignore', category=FutureWarning)

    # Check versions of libraries
    import matplotlib
    import upsetplot

    print(f"Using pandas version: {pd.__version__}")
    print(f"Using matplotlib version: {matplotlib.__version__}")
    print(f"Using upsetplot version: {upsetplot.__version__}")

    # Read the data file based on the specified file type
    if file_type == 'csv':
        data = pd.read_csv(data_file)
    elif file_type == 'xlsx':
        data = pd.read_excel(data_file)
    else:
        raise ValueError("file_type must be 'csv' or 'xlsx'")

    # Ensure the required columns are present in the data
    if 'Overlap Intersections' not in data.columns or 'Values' not in data.columns:
        raise ValueError("Data must contain 'Overlap Intersections' and 'Values' columns.")

    # Split the 'Overlap Combinations' into a list of individual sets
    data['Sets'] = data['Overlap Intersections'].apply(lambda x: [s.strip() for s in x.split(',')])

    # Prepare the data for the UpSet plot using from_memberships
    upset_data = from_memberships(data['Sets'], data=data['Values'])

    # Filter the data based on 'min_values' if provided
    if min_values is not None:
        upset_data = upset_data[upset_data >= min_values]

    # Sort the data and limit the number of intersections displayed
    upset_data = upset_data.sort_values(ascending=False)
    if max_intersections is not None:
        upset_data = upset_data.iloc[:max_intersections]

    # Set the font size
    plt.rcParams.update({'font.size': font_size})

    # Create the UpSet plot with the specified options
    upset = UpSet(
        upset_data,
        sort_categories_by='cardinality',
        sort_by=sort_by,
        show_counts=show_counts,
        intersection_plot_elements=intersection_plot_elements,
        element_size=element_size,
        **kwargs
    )

    # Plot the UpSet chart
    fig = plt.figure(figsize=figsize)
    upset.plot(fig=fig)

    # Try to rotate x-axis labels for better readability
    try:
        # Try accessing axes via the public get_axes method
        axes = upset.get_axes()
        matrix_axis = axes['matrix']
        plt.setp(
            matrix_axis.get_xticklabels(),
            rotation=label_rotation,
            ha='right'
        )
    except AttributeError as e:
        print("Error accessing axes to rotate labels:", e)
        print("Available attributes of upset object:", dir(upset))
        print("Attempting alternative methods to access axes...")
        try:
            # Try accessing the private _axes attribute
            matrix_axis = upset._axes['matrix']
            plt.setp(
                matrix_axis.get_xticklabels(),
                rotation=label_rotation,
                ha='right'
            )
        except AttributeError as e:
            print("Alternative method failed:", e)
            print("Attempting to access axes via matplotlib's current figure...")
            # Alternative method using plt.gcf()
            fig = plt.gcf()
            axes = fig.get_axes()
            if len(axes) > 0:
                # You may need to adjust the index based on your plot's structure
                matrix_axis = axes[0]
                plt.setp(
                    matrix_axis.get_xticklabels(),
                    rotation=label_rotation,
                    ha='right'
                )
            else:
                print("Could not access axes to rotate labels.")

    # Adjust labels and layout for better readability
    plt.tight_layout()

    # Display the plot
    plt.show()

generate_upset_plot(
    data_file='demo-data.csv',       # Replace with data file path
    file_type='csv',                 # Change to 'csv' if using a CSV file, xlsx if using an inferior filetype
    sort_by='cardinality',           # Options: 'cardinality' or 'degree'
    show_counts='%d',                # Format for displaying counts
    max_intersections=20,            # Show only top 20 intersections/interactions
    min_values=1000,                  # Exclude intersections with 'Values' less than 1000, to limit nonsense and tightly packed visuals
    figsize=(14, 10),                # Increase figure size for better readability
    element_size=40,                 # Adjust element size as needed
    font_size=10,                    # Set the font size
    label_rotation=45                # Rotate x-axis labels by 45 degrees
)