import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import base64
import io
import datetime

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUMEN])

app.layout = html.Div(
    [
        html.H1("SmartDAQ Temperature Data Plotter"),
        html.H2("Upload SmartDAQ Excel File (.xlsx)"),
        dcc.Upload(
            id="upload-data",
            children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
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
            # Allow multiple files to be uploaded
            multiple=False,
        ),
        dcc.Graph(
            id="output-data-upload",
            style={
                "height": "800px",
            },
        ),
    ]
)


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(",")

    decoded = base64.b64decode(content_string)
    try:
        if "xlsx" in filename:
            # Load the entire Excel file into a DataFrame
            excel_io = io.BytesIO(decoded)
            full_data = pd.read_excel(excel_io)

            # Find the row index for the 'Date' and 'Tag Comment'
            date_row_index = (
                full_data.index[full_data.iloc[:, 0] == "Date"].tolist()[0] + 1
            )
            tag_comment_row_index = full_data.index[
                full_data.iloc[:, 2] == "Tag Comment"
            ].tolist()[0]

            # Define column names starting from the 'Tag Comment' row
            column_names = full_data.iloc[tag_comment_row_index, 2:].dropna().tolist()
            data_temperature = full_data.iloc[date_row_index:, : len(column_names) + 2]
            data_temperature.columns = ["Date", "Time"] + column_names

            # Convert 'Date' and 'Time' to datetime
            data_temperature["datetime"] = pd.to_datetime(
                data_temperature["Date"].astype(str)
                + " "
                + data_temperature["Time"].astype(str)
            )
            data_temperature.drop(["Date", "Time","Tag Comment"], axis=1, inplace=True)

            # Melt the DataFrame for plotting
            temperature_long_df = data_temperature.melt(
                id_vars="datetime", var_name="Measurement", value_name="Temperature"
            )

            # Create the figure
            fig = px.line(
                temperature_long_df, x="datetime", y="Temperature", color="Measurement"
            )
            return fig

    except Exception as e:
        # Create a figure with an error message
        fig = px.line()
        fig.update_layout(
            title=f"An error occurred: {e}",
            xaxis={'visible': False},
            yaxis={'visible': False},
            annotations=[
                {
                    'text': "No data to display due to an error:<br>" + str(e),
                    'xref': 'paper',
                    'yref': 'paper',
                    'showarrow': False,
                    'font': {
                        'size': 16
                    }
                }
            ]
        )
        return fig



@app.callback(
    Output("output-data-upload", "figure"),
    [Input("upload-data", "contents")],
    [State("upload-data", "filename"), State("upload-data", "last_modified")],
)
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        return parse_contents(list_of_contents, list_of_names, list_of_dates)
    else:
        # Return an empty figure or your default figure if no file is uploaded
        return go.Figure()


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
