import dash
from dash import dcc, html, Input, Output
import base64
import io
import pandas as pd

from utilities.logging import setup_logger

logger = setup_logger()

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    dcc.Dropdown(
        id='log-level',
        options=[
            {'label': 'DEBUG', 'value': 'DEBUG'},
            {'label': 'INFO', 'value': 'INFO'},
            {'label': 'WARNING', 'value': 'WARNING'},
            {'label': 'ERROR', 'value': 'ERROR'},
            {'label': 'CRITICAL', 'value': 'CRITICAL'},
        ],
        value='INFO'
    ),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.Button('Select File')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False  # Allow single file upload
    ),
    html.Div(id='output-data-upload')
])

# Callback to change log level
@app.callback(
    Output('log-level', 'value'),
    [Input('log-level', 'value')]
)
def change_log_level(value):
    logger.setLevel(value)
    logger.info(f"Log level set to {value}")
    return value

# Callback to handle file upload
@app.callback(
    Output('output-data-upload', 'children'),
    [Input('upload-data', 'contents')],
    [dash.State('upload-data', 'filename')]
)
def upload_file(contents, filename):
    if contents is not None:
        logger.info(f"Received file: {filename}")
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        try:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            logger.info(f"Successfully processed file: {filename}")
            return html.Div([
                f'Successfully uploaded: {filename}',
                html.Hr(),
                html.Div('Preview:'),
                html.Pre(df.head().to_string())
            ])
        except Exception as e:
            logger.error(f"Failed to process file: {filename}. Error: {e}")
            return html.Div([
                f'Failed to process {filename}. Error: {e}'
            ])

if __name__ == '__main__':
    app.run_server(debug=True)
