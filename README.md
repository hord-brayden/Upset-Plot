# Upset-Plot
Simple Script to demo the Upset plot graphing visualization - 

> [!TIP]
> Head over to the project page for this, because their stuff is better than this stuff
> 
> [Python UpSet Plot Project Original](https://pypi.org/project/UpSetPlot/)

## Example Output
This is what you can expect from this plotting script, it should be fairly self-evident what the purpose is, but if you need a more in-depth understanding of how the data is intended to be read, refer to this website (UofU Upset Plot Home)[https://upset.app/]

![Upset Plot Demo](https://github.com/hord-brayden/Upset-Plot/blob/main/Final-Plot.png?raw=true)

## Usage
Really just head on down into the .py file, and on lines 155-166 edit these to be what you need them to be:
```python
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
```
Run the script, then you'll have to fight with matplotlib a bit and fiddling with the sizing, and hopefully profit?

## Reqs
You'll need to install some python libs to get this working, here are those reqs:
```bash
pip install pandas matplotlib upsetplot
```
