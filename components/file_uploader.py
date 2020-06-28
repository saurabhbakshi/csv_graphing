import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash
import os
import base64

from urllib.parse import quote as urlquote
from components import utilities

from app import app

UPLOAD_DIRECTORY = "..\\upload_files"
dirname = os.path.dirname(__file__)
UPLOAD_DIRECTORY_ABSOLUTE = os.path.join(dirname, UPLOAD_DIRECTORY)

# print(dirname)
# print(UPLOAD_DIRECTORY_ABSOLUTE)


def file_uploader():
    return html.Div(id="file-upload", className="container-div", children=[
        dcc.Upload(
            className="file-uploader",
            id='upload-data',
            children=html.Div([
                'Drop file to upload'
            ]),

            multiple=True
        ),
        html.Ul(id='file-list', className='file-list'),
        html.Button('Remove Upload Data', id='remove-upload',
                    n_clicks=0, className="btn-primary"),
        html.Div(className="hr"),
        dcc.Store(id='output_dir')

    ])


def save_file(name, content):
    data = content.encode("utf8").split(b";base64,")[1]
    try:
        if 'csv' in name or 'xls' in name:
            with open(os.path.join(UPLOAD_DIRECTORY_ABSOLUTE, name), "wb") as fp:
                fp.write(base64.decodebytes(data))
        else:
            return html.Div([
                'Upload of only csv/xls files allowed'
            ])
    except Exception as e:
        # print(e)
        return html.Div([
            'There was an error processing this file.'
        ])


def file_download_link(filename):
    """Create a Plotly Dash 'A' element that downloads a file from the app."""
    location = "/download/{}".format(urlquote(filename))
    return html.Div(children=[
        html.A(filename, id=filename, href="")
    ], style={
        'padding': '5px',
        'margin-left': '5px',
        'display': 'flex',
        'justify-content': 'space-between',
        'align-items': 'center',
        'width': '100%',
        'border-bottom': '1px dotted rgba(247 ,245, 244,.4)'
    })


@app.callback(
    [Output('file-list', 'children'),
     Output('output_dir', 'data')],
    [Input('upload-data', 'contents'), Input('remove-upload', 'n_clicks')
     ],
    [State('upload-data', 'filename'),
     State('upload-data', 'last_modified'),

     ]


)
def upload_file(list_of_contents, id, list_of_names, list_of_dates):
    ctx = dash.callback_context
    children = []
    if ctx.triggered[0]['prop_id'].split('.')[0] != 'remove-upload':
        if list_of_contents is not None and list_of_names is not None:
            for name, data in zip(list_of_names, list_of_contents):
                children.append(save_file(name, data))

        files = utilities.listFiles(UPLOAD_DIRECTORY_ABSOLUTE)
        if len(files) == 0:
            children.append(html.Li('No Files yet!'))
        else:
            [children.append(html.Li(file_download_link(filename)))
             for filename in files]
    else:

        files = utilities.listFiles(UPLOAD_DIRECTORY_ABSOLUTE)
        # [remove_files(filename) for filename in files]
        [utilities.remove_file(UPLOAD_DIRECTORY_ABSOLUTE, filename)
         for filename in files]
        children.append(html.Li('Files Removed!'))
    return children, UPLOAD_DIRECTORY_ABSOLUTE
