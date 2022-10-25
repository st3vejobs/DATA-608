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
        "Stewardship_Status",
        dcc.Dropdown(
            id='stewardship-dropdown', clearable=False,
            value='None', options=[
                {'label': c, 'value': c}
                for c in list(trees['steward'].unique())
            ])
    ]),
])

@app.callback(
    Output('graph', 'figure'),
    [Input("Borough-dropdown", "value")],
    [Input("stewardship-dropdown", "value")]
)
def update_figure(Borough,Stewardship_Status):
    new_trees = trees[trees.boroname == Borough]
    new_trees = new_trees[new_trees.steward == Stewardship_Status]
    fig = px.histogram(new_trees, x="health", title = f"Street Tree Stewardship Impact on Health for {Borough}")
    return fig


if __name__ == "__main__": app.run_server(debug=False, host='0.0.0.0', port=8050)
    
#app.run_server(debug = True) #mode='inline'
