import dash_html_components as html
import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import os
from components import utilities
from app import app


def data_load():

    return html.Div(className="container-div", children=[
        html.H3('ETL Configuration', className="form-heading"),
        dcc.Input(className="text-input", id='delimiter-input', type="text", maxLength=1,
                  placeholder="Delimiter, eg. ; or /."),
        dcc.Checklist(id='column-splitter',
                      options=[
                          {'label': 'Use Column Splitter', 'value': 'True'}
                      ],
                      value=[]
                      ),
        dcc.Input(className="text-input", id='split-source', type="text",
                  placeholder="--optional: Column to split, eg. DATE"),
        dcc.Input(className="text-input", id='split-on', type="text", maxLength=1,
                  placeholder="--optional: Splitter for column eg. ;/ "),
        dcc.Input(className="text-input", id='split-target', type="text",
                  placeholder="--optional: Target columns after split, eg. DATE,TIME"),
        html.P(id='form-error', className='form-error'),
        html.Div(className="range-slider", children=[
            html.Label('Select Data Range'),
            dcc.RangeSlider(
                className="range-slider-slide",
                id='range-slider',
                min=0,
                max=200,
                step=1,
                value=[0, 100],
                marks={
                    0: '0',
                    100: '100'
                }
            )
        ]),
        html.Button('Load Data', id='load-data',
                    n_clicks=0, className="btn-primary"),
        # dcc.Loading(
        #     id="loading-2",
        #     children=[html.Div([html.Div(id="data-loader")])],
        #     type="circle",
        # ),
        html.Div(className="hr"),
        dcc.Store(id='memory'),
        dcc.Store(id='data_columns')
    ])


def eTLOperation(output_dir, column_splitter, delimiter, split_s, splitter, split_t, data_range):
    file = os.listdir(output_dir)[0]
    if file == None:
        return "No file found to load!"
    file_abs_path = os.path.join(output_dir, file)
    data, max_range, error = utilities.loadDataFrame(
        file_abs_path, delimiter, data_from=data_range[0], data_to=data_range[1])
    if error != None:
        return None, None, error
    else:
        if column_splitter == 'True':
            data = utilities.split_dataFrame_column(
                data, split_s, splitter, split_t)
        return data, max_range, None


def formValiator(column_splitter, delimiter, split_s, splitter, split_t):
    validation_out = None
    if delimiter == None or len(delimiter) == 0:
        validation_out = "Delimiter should be of length 1"
        return validation_out
    if column_splitter == 'True':
        if split_s == None or len(split_s) == 0 or splitter == None or len(splitter) == 0 or split_t == None or len(split_t) == 0:
            validation_out = "All three are required split-source,splitter and split-target"
            return validation_out
        if splitter != None:
            if len(split_t.split(",")) != 2*len(split_s.split(",")):
                validation_out = "Split source is splitted into 2 target columns. Split source and target not in sync"
                return validation_out
    return validation_out

# @app.callback(

# )
# def updateSlider()


@app.callback(
    # Output("loading-output-2", "children"),
    [Output('form-error', 'children'), Output('memory', 'data'), Output('data_columns',
                                                                        'data'), Output('hidden-div', 'hidden'), Output('range-slider', 'max'), Output('range-slider', 'marks')],
    [Input('load-data', 'n_clicks'), Input('output_dir', 'data')],
    [
        State('column-splitter', 'value'), State('delimiter-input', 'value'), State('split-source', 'value'), State('split-on',
                                                                                                                    'value'), State('split-target', 'value'), State('memory', 'data'), State('range-slider', 'value'), State('range-slider', 'marks')
    ]
)
def loadData(n_clicks, output_dir, column_splitter, delimiter, split_source, splitter, split_target, data, data_range, range_marks):
    if n_clicks is None or n_clicks == 0:
        raise dash.exceptions.PreventUpdate
    validation_out = None
    if n_clicks is not None:
        split_enabled = None
        if delimiter == None or len(delimiter) == 0:
            validation_out = "Delimiter can't be empty!"
            return validation_out, None, None, True, 200, range_marks
        if len(column_splitter) > 0:
            split_enabled = column_splitter[0]

        # print(n_clicks, output_dir, split_enabled,
        #       delimiter, split_target, split_source, splitter)
        validation_out = formValiator(split_enabled,
                                      delimiter, split_source, splitter, split_target)
        if validation_out != None:
            return validation_out, None, None, True, 200, range_marks
        data, max_range, error = eTLOperation(
            output_dir, split_enabled, delimiter, split_source, splitter, split_target, data_range)
        if error != None:
            return error, None, None, True, 200, range_marks
    # Setting default value of data dict
    # eTLOperation(output_dir,delimiter,split_source,splitter,split_target)
    # df = pd.DataFrame({'A': [1, 2, 3, 4], 'B': [5, 6, 7, 8]})
    # data = df.to_dict('records')
    step_size = 100
    new_range_marks = {}
    for i in range(0, int(max_range/step_size)):
        new_range_marks[int(i*100)] = str(i*100)
    new_range_marks[int(max_range)] = str(max_range)
    data_columns = list(data.columns)
    return validation_out, data.to_dict('records'), data_columns, False, max_range, new_range_marks
    # ctx = dash.callback_context
    # upload_dir_absolute = ctx.states['UPLOAD_DIRECTORY_ABSOLUTE']
    # files = os.listdir(upload_dir_absolute)
    # for file in files:
    #     df = pd.read_csv(os.path.join(
    #         upload_dir_absolute, file), delimiter=';')
