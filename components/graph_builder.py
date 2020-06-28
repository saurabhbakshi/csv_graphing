import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash

from app import app


def graphBuilder():
    return dcc.Loading(
        id="loading",
        children=[
            html.Div(id='hidden-div', hidden=True, children=[
                html.Div(id='graph-builder', hidden=True, className="container-div", children=[
                        html.H3('Graph Configuration',
                                className="form-heading"),
                        dcc.Dropdown(
                            className="dropdown-input",
                            id='graph-x',
                            options=[
                            ],
                            value='',
                            placeholder="Select the X value"
                        ),
                    dcc.Dropdown(
                            className="dropdown-input",
                            id='graph-y',
                            options=[
                            ],
                            value='',
                            multi=True,
                            placeholder="Select the Y values"
                            ),

                    html.Button('Build Graph', id='build-graph',
                                n_clicks=0, className="btn-primary"),
                    dcc.Checklist(id='show-data-table',
                                  options=[
                                      {'label': 'Show graph data', 'value': 'True'}
                                  ],
                                  value=[]
                                  ),
                    html.Div(className="hr"),
                    dcc.Store(id='x-value'),
                    dcc.Store(id='y-value'),
                    dcc.Store(id='construct-graph')
                ])]), ],
        type="circle",
    )


@app.callback(
    [Output('graph-x', 'options'),
     Output('graph-x', 'value'),
     Output('graph-y', 'options'),
     Output('graph-y', 'value'),
     ],
    [Input('data_columns', 'data')]
)
def updateGraphBuilder(columns):
    options = []
    if columns == None:
        raise dash.exceptions.PreventUpdate
    for col in columns:
        options.append({'label': col, 'value': col})
    return options, options[0]['value'], options, options[1]['value']


@app.callback(
    [Output('x-value', 'data'),
     Output('y-value', 'data')],
    [Input('build-graph', 'n_clicks')],
    [
        State('graph-x', 'value'),
        State('graph-y', 'value')
    ]
)
def buildGraph(n_clicks, x_value, y_values):
    if n_clicks == 0:
        raise dash.exceptions.PreventUpdate
    # print(x_value, y_values)
    return x_value, y_values
