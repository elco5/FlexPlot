import io
import os
import base64
import logging

import dash
from dash import dcc, html, Input, Output

from data_ingestion.data_loader import DataLoader  # Replace with your actual import
from utilities.logging import setup_logger

logger = logging.getLogger("my_logger")

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(
    [
        dcc.Dropdown(
            id="log-level",
            options=[
                {"label": "DEBUG", "value": "DEBUG"},
                {"label": "INFO", "value": "INFO"},
                {"label": "WARNING", "value": "WARNING"},
                {"label": "ERROR", "value": "ERROR"},
                {"label": "CRITICAL", "value": "CRITICAL"},
            ],
            value="INFO",
        ),
        dcc.Upload(
            id="upload-data",
            children=html.Div(["Drag and Drop or ", html.Button("Select File")]),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
            },
            multiple=False,  # Allow single file upload
        ),
        html.Div(id="output-data-upload"),
    ]
)


# Callback to change log level
@app.callback(Output("log-level", "value"), [Input("log-level", "value")])
def change_log_level(value):
    logger.setLevel(value)
    logger.info(f"Log level set to {value}")
    return value


# Callback to handle file upload
@app.callback(
    Output("output-data-upload", "children"),
    [Input("upload-data", "contents")],
    [dash.State("upload-data", "filename")],
)
def upload_file(contents, filename):
    if contents is not None:
        logger.info(f"Received file: {filename}")
        content_type, content_string = contents.split(",")
        decoded = base64.b64decode(content_string)
        logger.info(f"Decoded file: {filename}")

        # Create a temporary file to save the decoded content
        temp_file_path = f"temp_{filename}"
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(decoded)
            logger.info(f"Created temporary file: {filename}")

        try:
            # Use DataLoader to process the file
            data_loader = DataLoader(temp_file_path)
            logger.info(f"Created DataLoader for file: {filename}")
            data_loader.auto_load(file_path=temp_file_path)
            logger.info(f"Auto Loaded file: {filename}")
            
            # set df to the data_loader's dataframe
            df = data_loader.data['data_frame']
            logger.info(f"Set df to data_loader.data['data_frame']: {filename}")
            
            # Clean up the temporary file
            os.remove(temp_file_path)
            logger.info(f"Removed temporary file: {filename}")
            
            logger.info(f"Successfully processed file: {filename}")
            return html.Div(
                [
                    f"Successfully uploaded: {filename}",
                    html.Hr(),
                    html.Div("Preview:"),
                    html.Pre(df.head().to_string()),
                ]
            )
        except Exception as e:
            # Clean up the temporary file in case of an error
            os.remove(temp_file_path)

            logger.error(f"Failed to process file: {filename}. Error: {e}")
            return html.Div([f"Failed to process {filename}. Error: {e}"])


if __name__ == "__main__":
    app.run_server(debug=True)
