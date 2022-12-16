# Import required libraries
import pandas as pd
import dash
#import dash_html_components as html
from dash import html
#import dash_core_components as dcc
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                dcc.Dropdown(id='site-dropdown',
                                options=[
                                    {'label': 'All Sites', 'value': 'ALL'},
                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                ],
                                value='ALL',
                                placeholder="Select a Launch Site here",
                                searchable=True
                                ),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                min=0, max=10000, step=1000,
                                marks={0:'0', 2000:'2000', 4000:'4000', 6000:'6000', 8000:'8000', 10000:'10000'},   
                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Total Success Launches by Site')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']==(entered_site)]
        #filtered_df = filtered_df['Launch_Site'].groupby(spacex_df['class']).count().reset_index()
        fig = px.pie(filtered_df, values='class', names=filtered_df['class'], 
        title='Total Success Launches For Site ' +  entered_site)
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output 
#def payload(entered_site,Range):
#    low, high = Range
#    filtered_df = spacex_df
#    if entered_site == 'ALL':
#        fig = px.scatter(filtered_df, y="class", x="Payload Mass (kg)", color="Boosster Version Category", symbol="Boosster Version Category")
#        return fig
#    else:
#        filtered_df = spacex_df[spacex_df['Launch Site']==(entered_site)]
#        fig = px.scatter(filtered_df, y="class", x="Payload Mass (kg)", color="Boosster Version Category", symbol="Boosster Version Category")
#        return fig
@app.callback(
     Output(component_id = 'success-payload-scatter-chart', component_property = 'figure'),
     [Input(component_id = 'site-dropdown', component_property = 'value'), 
     Input(component_id = "payload_slider", component_property = "value")]
)
def update_scattergraph(site_dropdown,payload_slider):
    if (site_dropdown == 'All' or site_dropdown == 'None'):
        low, high = payload_slider
        all_sites  = spacex_df
        inrange = (all_sites['Payload Mass (kg)'] > low) & (all_sites['Payload Mass (kg)'] < high)
        fig = px.scatter(
                all_sites[inrange], 
                x = "Payload Mass (kg)", 
                y = "class",
                title = 'Correlation Between Payload and Success for All Sites',
                color="Booster Version Category",
                size='Payload Mass (kg)',
                hover_data=['Payload Mass (kg)']
            )
    else:
        low, high = payload_slider
        site_specific  = spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
        inrange = (site_specific['Payload Mass (kg)'] > low) & (site_specific['Payload Mass (kg)'] < high)
        fig = px.scatter(
                site_specific[inrange],
                x = "Payload Mass (kg)",
                y = "class",
                title = 'Correlation Between Payload and Success for Site &#8608; '+site_dropdown,
                color="Booster Version Category",
                size='Payload Mass (kg)',
                hover_data=['Payload Mass (kg)']
            )
    return fig    

# Run the app
if __name__ == '__main__':
    app.run_server()
