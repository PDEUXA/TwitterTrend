from datetime import datetime

import dash_table
from dash import dependencies
from dash.dependencies import Input, Output
import pandas as pd
from utils_to_mongoDB import *
import plotly.express as px
from app import app
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc



@app.callback(Output('live-update-stream-by-lang', 'figure'),
              Input('interval-component', 'n_intervals'))
def generate_pie_stream_lang(n):
    top_docs = pd.DataFrame(get_first_nth_stream(10, group_lang=True))
    fig = px.pie(top_docs, values="NB_HASH_TOTAL", names="lang", template='ggplot2')
    return fig


@app.callback(Output('live-update-stream', 'children'),
              [Input('interval-component', 'n_intervals'),
               Input('lang_dropdown', 'value')])
def update_streams(n, value):
    top_docs = get_first_nth_stream(5, lang=value)
    df = pd.DataFrame(top_docs)
    df = df[["NB_HASH_TOTAL", "TAG_NAME"]]
    table_header = [
        html.Thead(html.Tr([html.Th("Nombre de hash Tag"), html.Th("Hash Tag")]))
    ]
    rows = [html.Tr([html.Td(i.NB_HASH_TOTAL), html.Td(i.TAG_NAME)]) for i in df.iloc]

    table_body = [html.Tbody(rows)]

    return dbc.Table(table_header + table_body, borderless=True, dark=True,
                     hover=True,
                     responsive=True,
                     striped=True, size="sm", style={"text-align": "center"})

@app.callback(
    dependencies.Output('output-container-batch-range', 'children'),
    [dependencies.Input('my-date-picker-range', 'start_date'),
     dependencies.Input('my-date-picker-range', 'end_date')])
def update_batch(start_date, end_date):
    if start_date and end_date:
        top_docs = get_first_10_from_batch(datetime.strptime(start_date, "%Y-%m-%d"),
                                           datetime.strptime(end_date, "%Y-%m-%d"))
        df = pd.DataFrame(top_docs)
        top_tags = list(
            df.groupby("TAG_NAME").agg({'NB_HASH': 'sum'}).reset_index().sort_values("NB_HASH", ascending=False)[
                'TAG_NAME'].head(5))
        df = df[df.TAG_NAME.isin(top_tags)]
        df["dates"] = pd.to_datetime(df['WINDOW_START'])
        df = df.groupby(["TAG_NAME", pd.Grouper(key='dates', freq="H")]).agg({'NB_HASH': 'sum'}).reset_index()
        df = df.sort_values(by=['dates', 'NB_HASH'], ascending=[True, False]).reset_index(drop=True)
        group = df.groupby(['dates']).head(10).reset_index(drop=True)
        group = group.groupby('TAG_NAME')
        fig = go.Figure()
        # each group iteration returns a tuple
        # (group name, dataframe)
        for group_name, df in group:
            fig.add_trace(go.Bar(x=df['dates'],
                                 y=df['NB_HASH'].cumsum(),
                                 name=group_name))
        fig.update_layout(barmode='stack', template="ggplot2",
                          legend=dict(
                              yanchor="top",
                              y=0.99,
                              xanchor="left",
                              x=0.01))
        return html.Div([dcc.Graph(figure=fig)
                         ])
