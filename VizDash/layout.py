from datetime import date

import dash_html_components as html
from utils_to_mongoDB import get_unique
import dash_core_components as dcc
import dash_bootstrap_components as dbc

OPTIONS_DATE = get_unique("WINDOW_START")
OPTIONS_LANG = get_unique("LANG", "stream")

header_layout = dbc.Row(html.H1('Twitter Live'), justify="center", className="h-10",
                        style={"height": "100%",
                               "background-color": "white",
                               "border": "1px solid black",
                               "margin-bottom": "10px"},
                        )

# STREAM LAYOUT
stream_lang_dropdown = dcc.Dropdown(id='lang_dropdown',
                                    options=OPTIONS_LANG,
                                    clearable=False)
stream_table = html.Div(id='live-update-stream')
stream_graph = dcc.Graph(id='live-update-stream-by-lang')

stream_layout = dbc.Col([dbc.Col([html.H2("Stream Feed"),
                                  stream_lang_dropdown,
                                  stream_table]),
                         dbc.Col(stream_graph, align="center")], width=5)

# BATCH LAYOUT
batch_datepicker = dcc.DatePickerRange(
    id='my-date-picker-range',
    min_date_allowed=date(2021, 1, 1),
    max_date_allowed=date(2025, 9, 19),
    initial_visible_month=date.today(),
)
batch_graph = html.Div(id='output-container-batch-range')

batch_layout = dbc.Col([dbc.Col([html.H2("Batch Feed"),
                                 batch_datepicker]),
                        dbc.Col(batch_graph)], width=5)

layout = html.Div([header_layout,
                   dbc.Row([stream_layout,
                            batch_layout], justify="center")] +
                  [dcc.Interval(id='interval-component',
                                interval=1 * 1000,  # in milliseconds
                                n_intervals=0),
                   ])
