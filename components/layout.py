from components.data_table import getDataTable
import dash_html_components as html

# Components import
from components import file_uploader
from components import data_load
from components import graph
from components import graph_builder
from components import data_table


def left_pane_layout():
    return html.Div(className="container", children=[
        html.Div(className="title", children=[
                 html.H1('CSV Graphing Dashboard')]),
        html.Div(className="content-container", children=[
            html.Div(id="left-panel", className="left-panel", children=[
                file_uploader.file_uploader(),
                data_load.data_load(),
                graph_builder.graphBuilder()
            ]),
            html.Div(id="main-content", className="main-content", children=[
                graph.getGraph(),
                data_table.getDataTable()
            ]),
        ]), ])


def right_pane_layout():
    pass


def grid_layout():
    pass
