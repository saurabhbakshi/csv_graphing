from components.data_load import data_load
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table
from dash.dependencies import Input, Output, State
from components import utilities

from app import app


@app.callback(
    [Output('memory-out', 'data'),
     Output('memory-out', 'columns'),
     Output('table-container', 'hidden')],
    [Input('show-data-table', 'value')],
    [State('memory', 'data'),
     State('data_columns', 'data'),
     State('x-value', 'data'),
     State('y-value', 'data')
     ]

)
def graphData(show_table, dataFrame, data_columns, x_val, y_val):
    if dataFrame is None:
        raise dash.exceptions.PreventUpdate
    selected_columns = []
    selected_columns.append(x_val)
    if type(y_val).__name__ == 'list':
        selected_columns.extend(y_val)
    else:
        selected_columns.append(y_val)

    filtered_columns = list(
        set(selected_columns).intersection(set(data_columns)))
    filtered_columns.pop(filtered_columns.index(x_val))
    filtered_columns.insert(0, x_val)
    table_columns = []
    if len(show_table) == 0:
        return None, None, True
        # raise dash.exceptions.PreventUpdate
    else:
        # tableData = utilities.listToDataFrame(dataFrame)
        for col in filtered_columns:
            table_columns.append({"name": col, "id": col})
        return dataFrame, table_columns, False


def getDataTable():
    return html.Div(id="table-container", className='table-container', hidden=True, children=[

        html.H2('Data will be shown below', className='secondary-heading'),
        dash_table.DataTable(
            id='memory-out',
            columns=[],
            page_size=20,
            fixed_rows={'headers': True},
            style_table={'height': '300px', 'overflowY': 'auto'},
            style_cell={'whiteSpace': 'normal', 'height': 'auto'}
        )
    ])
