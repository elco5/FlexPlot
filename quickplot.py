import pandas as pd
import plotly.express as px

# Load the column names
path_to_your_file = r"\\teslamotors.com\US\Engineering\Stationary_Storage\Compliance\Products\Energy Gateway 3\Raw Data & Photos\Temperature\RAW\6-14\000064_230614_112648.GEV.xlsx"
column_names = pd.read_excel(path_to_your_file, skiprows=30, nrows=1)
column_names = column_names.iloc[:, 2:].values.flatten().tolist()  # Assuming temperature data starts at the 3rd column

# Load the data, skipping the metadata rows
data_temperature = pd.read_excel(path_to_your_file, skiprows=34, header=None)
data_temperature.columns = ['Date', 'Time'] + column_names

# Combine the date and time into a single datetime column
data_temperature['datetime'] = pd.to_datetime(data_temperature['Date'].astype(str) + ' ' + data_temperature['Time'].astype(str))

# Drop the separate Date and Time columns as we now have datetime
data_temperature.drop(['Date', 'Time'], axis=1, inplace=True)

# Melt the dataframe to long format for use with Plotly Express
temperature_long_df = data_temperature.melt(id_vars='datetime', var_name='Measurement', value_name='Temperature')

# Create the interactive plot with Plotly Express
fig = px.line(temperature_long_df, x='datetime', y='Temperature', color='Measurement')

# Add interactive functionality with checkboxes for each temperature measurement
# This will allow users to select which lines to display
measurements = temperature_long_df['Measurement'].unique()
buttons = [dict(label='All',
                method='update',
                args=[{'visible': [True] * len(measurements)},
                      {'title': 'Temperature vs Time: All Measurements'}])]

for measurement in measurements:
    buttons.append(dict(label=measurement,
                        method='update',
                        args=[{'visible': [m == measurement for m in measurements]},
                              {'title': f'Temperature vs Time: {measurement}'}]))

fig.update_layout(
    updatemenus=[dict(type="dropdown",
                      direction="down",
                      showactive=True,
                      x=0.1,
                      xanchor='left',
                      y=1.2,
                      yanchor='top',
                      buttons=buttons)]
)

# Show the figure in the browser
fig.show()
