# CSV GRAPHING

Maintained By: Saurabh Jain
# Description
#### CSV Graphing is a simple dashboard build to visualize the *.csv files or any delimited file. It provide uni visualization or comparative visualization

## Features 
- Load csv file with any delimiter (, or ; or # etc.) 
- Plots **interactive graphs** (single metrics or comparable scatters) with few clicks.
- Filter graph data as per requirement
- Show graph data in tabular format
- Plot **isolated** or **comparative** graphs

![CSV Graphing Pictorial](https://github.com/saurabhbakshi/csv_graphing/blob/master/csvgraphingpictorial.png)

## Running Container
- Syntax: docker run --rm -d --name -p :5500 sjain/csv-graphing:1
- Example: docker run --rm -d --name demo-board -p 5500:5500 sjain/csv-graphing:1

## Execution Consideration
- The initial load will be of first 100 rows from file
- With initial load tool will build the pagination based on number of rows in file

## Limitation
- Only work with single file
- No data level filters are available
- Auto refresh is not there, with change in data range need to click *Load Data* again to load data in memory
