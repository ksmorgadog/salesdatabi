# Base https://stackoverflow.com/questions/63592900/plotly-dash-how-to-design-the-layout-using-dash-bootstrap-components
from dash import Dash, dcc, html, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from urllib.request import urlopen #Cargado de información en línea
import json #Análisis de archivos Json

df2=pd.read_csv("./src/data/CT_Municipalities.csv",dtype={'FIPS': object})

df_fin=pd.read_csv("./src/data/CT_Towns.csv")


with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

with urlopen('https://raw.githubusercontent.com/HandsOnDataViz/ct-boundaries/main/ct-towns-2021-datactgov.geojson') as response:
    towns = json.load(response)

@callback(
    Output('graph-with-slider', 'figure'),
    Input('year--slider', 'value'),
    Input('variable_tipo', 'value'),
    Input('variable_tranformacion', 'value'))
# Iris bar figure
def drawMap(selected_year,selected_variable,variable_transformacion):
    if variable_transformacion == "County":
        fig=px.choropleth_mapbox(df2[df2["List Year"]==selected_year], geojson=counties, locations='FIPS', color=selected_variable,
                color_continuous_scale="Viridis",
                #labels={'Sale Ratio':'Ratio de ventas'},
                center={"lat": 41.599998, "lon": -72.699997},
                mapbox_style="carto-positron"
                ).update_layout(
            template='plotly_dark',
            plot_bgcolor= 'rgba(0, 0, 0, 0)',
            paper_bgcolor= 'rgba(0, 0, 0, 0)',
            height=500,
            margin={"r":0,"t":0,"l":0,"b":0}
        )
    else:
        fig=px.choropleth_mapbox(df_fin[df_fin["List Year"]==selected_year], geojson=towns, locations='Town', color=selected_variable,
                           color_continuous_scale="Viridis",
                           featureidkey="properties.town",
                           #range_color=(0, 12),
                           labels={'TOT_POP':'Población',
                                   'TOT_MALE' : "Número Hombres"},
                           center={"lat": 41.599998, "lon": -72.699997},
                           mapbox_style="carto-positron"
                          ).update_layout(
            template='plotly_dark',
            plot_bgcolor= 'rgba(0, 0, 0, 0)',
            paper_bgcolor= 'rgba(0, 0, 0, 0)',
            height=500,
            margin={"r":0,"t":0,"l":0,"b":0})
    return fig

def drawFigure2():
    return  html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    figure=px.bar(
                        df, x="sepal_width", y="sepal_length", color="species"
                    ).update_layout(
                        template='plotly_dark',
                        plot_bgcolor= 'rgba(0, 0, 0, 0)',
                        paper_bgcolor= 'rgba(0, 0, 0, 0)',
                        height=300
                    ),
                    config={
                        'displayModeBar': False
                    }
                ) 
            ])
        ),  
    ])

# Text field
def drawText():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.H2("Visualización Ventas Inmuebles Connecticut"),
                ], style={'textAlign': 'center'}) 
            ])
        ),
    ])

# Filtro
def drawFilter():
    return html.Div([
        dbc.Card(
        dbc.CardBody(dcc.Slider(
        df2['List Year'].min(),
        df2['List Year'].max(),
        step=None,
        id='year--slider',
        value=df2['List Year'].max(),
        marks={str(year): str(year) for year in df2['List Year'].unique()}))
        ),
    ])

# Botones
def drawButtons():
    return html.Div([
        dbc.Card(
        dbc.CardBody(dcc.Dropdown(
                ["Assessed Value","Sale Amount","Sale Ratio"],
                'Assessed Value',
                id='variable_tipo'
            ))
        ),
    ])

def drawButtonsTown():
    return html.Div([
        dbc.Card(
        dbc.CardBody(dcc.Dropdown(
                ["Town","County"],
                'County',
                id='variable_tranformacion'
            ))
        ),
    ])

#Filtrado de tabla
@callback(
    Output('filtered_table', 'data'),
    Input('year--slider', 'value'))
def drawTable(year_filter):
    dff=df2
    dff=dff[dff["List Year"]==year_filter]
    return dff.to_dict('records')

# Data
df = px.data.iris()

# Build App
app = Dash(external_stylesheets=[dbc.themes.SLATE])

app.layout = html.Div([
    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col([drawText()], width=12)
            ], align='center'), 
            html.Br(),
            dbc.Row([
                dbc.Col([drawFilter()], width=12)
            ], align='center'), 
            html.Br(),
            dbc.Row([
                dbc.Col([dcc.Graph(id='graph-with-slider')], width=8),
                dbc.Col([dbc.Row(drawButtons(),style={"height": "10vh"}),
                         html.Br(),
                         dbc.Row(drawButtonsTown(),style={"height": "10vh"})
                         ], width=4),
            ], align='center'),
            html.Br(),
            dbc.Row([
                html.Br(),
                dbc.Col([dash_table.DataTable(id = "filtered_table", columns=
                            [{"name": i, "id": i} for i in df2.columns],    style_header={
        'backgroundColor': 'rgb(30, 30, 30)',
        'color': 'white'
    },
    style_data={
        'backgroundColor': 'rgb(50, 50, 50)',
        'color': 'white'
    }),
                            ], width=12)
            ], align='center'),      
        ]), color = 'dark'
    )
])

# Run app and display result inline in the notebook
app.run_server()

