
from components import layout
# import dash_html_components as html
# import dash_core_components as dcc
# import plotly.express as px
# import plotly.graph_objects as go
# import pandas as pd
# from dash.dependencies import Input, Output
from datetime import datetime as dt
from app import app

app.layout = layout.left_pane_layout()


if __name__ == '__main__':
    app.run_server(debug=True)
