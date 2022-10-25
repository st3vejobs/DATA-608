import pandas as pd


trees = pd.read_json('https://data.cityofnewyork.us/resource/uvpi-gqnh.json')
trees = trees.fillna("None")


import plotly.express as px
from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import gunicorn

df = trees

app = Dash(__name__)
server = app.server
app.layout = html.Div([
    html.H1("Street Tree Health by Borough"),
    dcc.Graph(id='graph'),
    html.Label([
        "Borough",
        dcc.Dropdown(
            id='Borough-dropdown', clearable=False,
            value='Manhattan', options=[
                {'label': c, 'value': c}
                for c in ['Manhattan','Brooklyn','Queens','Bronx','Staten Island']
            ])
    ]),
    html.Label([
        "Species",
        dcc.Dropdown(
            id='species-dropdown', clearable=False,
            value='red maple', options=[
                {'label': c, 'value': c}
                for c in list(trees['spc_common'].unique())
            ])
    ]),
])

@app.callback(
    Output('graph', 'figure'),
    [Input("Borough-dropdown", "value")],
    [Input("species-dropdown", "value")]
)
def update_figure(Borough,Species):
    new_trees = trees[trees.boroname == Borough]
    new_trees = new_trees[new_trees.spc_common == Species]
    fig = px.histogram(new_trees, x="health", title = f"Street Tree ({Species}) Health for {Borough}")
    return fig

app.run_server(debug = True) #mode='inline'
