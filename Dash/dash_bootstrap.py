# Base https://stackoverflow.com/questions/63592900/plotly-dash-how-to-design-the-layout-using-dash-bootstrap-components
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px

# Iris bar figure
def drawFigure():
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
                        height=500
                    ),
                    config={
                        'displayModeBar': False
                    }
                ) 
            ])
        ),  
    ])

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
                    html.H2("Visualización Connecticut"),
                ], style={'textAlign': 'center'}) 
            ])
        ),
    ])

# Filtro
def drawFilter():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.H2("Aquí va filtro"),
                ], style={'textAlign': 'center'}) 
            ])
        ),
    ])

# Tabla
def drawTable():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.H2("Aquí va Tabla"),
                ], style={'textAlign': 'center'}) 
            ])
        ),
    ])

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
                dbc.Col([drawFigure()], width=8),
                dbc.Col([dbc.Row(drawFigure2(),style={"height": "50vh"}),
                         html.Br(),
                         dbc.Row(drawFigure2(),style={"height": "50vh"})
                         ], width=4),
            ], align='center'),
            html.Br(),
            dbc.Row([
                html.Br(),
                dbc.Col([drawTable()], width=12)
            ], align='center'),      
        ]), color = 'dark'
    )
])

# Run app and display result inline in the notebook
app.run_server()

