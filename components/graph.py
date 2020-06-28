import dash_html_components as html
import dash
import pandas as pd
import dash_core_components as dcc
from app import app
from dash.dependencies import Input, Output, State
import dash_table
import plotly.express as px
import plotly.graph_objects as go


def getGraph():
    return html.Div(children=[
        html.H2('Graph will be shown below',
                className='secondary-heading'),
        dcc.Loading(
            id="graph-loading",
            children=[html.Div(id='graph-container', style={'height': '90vh', 'margin': 'auto'}, children=[dcc.Graph(id="show-graph", className="show-graph"), ])], type='default')])


@app.callback(
    Output('graph-container', 'style'),
    [Input('show-data-table', 'value')]

)
def updateGrpahHeight(show_table):
    if len(show_table) == 0:
        return {'height': '90vh', 'margin': 'auto'}
    else:
        return {'height': '60vh', 'margin': 'auto'}


@app.callback(
    Output('show-graph', 'figure'),
    [Input('x-value', 'data'),
     Input('y-value', 'data')],
    [State('memory', 'data')]
)
def plotGraph(x_value, y_value, data):
    if data == None:
        raise dash.exceptions.PreventUpdate
    fig = None
    plot_data = pd.DataFrame(data)
    x_series = plot_data[x_value]

    if type(y_value).__name__ == 'list':
        fig = go.Figure()
        for y_val in y_value:
            y_series = plot_data[y_val]
            fig.add_trace(go.Scatter(x=x_series, y=y_series,
                                     mode='lines+markers', name=y_val))
    else:
        fig = px.bar(plot_data, x=x_value, y=y_value)
    fig.update_layout(autosize=True)
    #                   margin=dict(l=50, r=50, b=100, t=100, pad=4))
    return fig
# @app.callback(
#     dash.dependencies.Output('nac_perf-cpu', 'figure'),
#     [dash.dependencies.Input('date-filter', 'start_date'),
#      dash.dependencies.Input('date-filter', 'end_date'),
#      #  dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
#      #  dash.dependencies.Input('crossfilter-yaxis-type', 'value'),
#      #  dash.dependencies.Input('crossfilter-year--slider', 'value')
#      ])
# def updateCPUGraph(start_date, end_date):
#     global data
#     fig = None
#     if start_date is not None and end_date is not None:
#         data = data[(data['N_DATE'] >= start_date)
#                     & (data['N_DATE'] <= end_date)]
#         fig = px.bar(data, x='DATE', y='OVERALL_CPU_LOAD_VAL',
#                      labels={'OVERALL_CPU_LOAD_VAL': "CPU Usage"},
#                      color='OVERALL_CPU_LOAD_VAL')
#     return fig
