# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from dash.dependencies import Input, Output, State
import numpy as np
from PIL import Image
import cv2
import os
from plotly.subplots import make_subplots

app = dash.Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 6],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group", orientation='h')




def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y=[]))
    fig.update_layout(template=None)
    fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
    fig.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)

    return fig

from fight.pokemon import OwnPokemon

party = OwnPokemon.party

figs = []
titles = []
for pokemon in party:
    figs.append(go.Bar(x=list(pokemon.stats.values()), y=list(pokemon.stats.keys()), orientation='h'))
    titles.append(f"<b>{pokemon.name}</b>    level: {pokemon.level}")

fig_tot = make_subplots(rows=3, cols=2, horizontal_spacing=0.25,
                        subplot_titles=titles)

# add subplots
for i, fig in enumerate(figs):
    fig_tot.add_trace(
        fig,
        row=int(i / 2) + 1, col=i % 2 + 1)

fig_tot.update_layout(
    autosize=False,
    height=600,
    width=1000,
    # bargap=0.15,
    # bargroupgap=0.1,
    barmode="stack",
    hovermode="x",
    showlegend=False,
    margin=dict(l=200),
    title=f'<b>Party</b>'
)

# add the images
positions = [(-0.18, 1), (0.45, 1), (-0.18, 0.62), (0.45, 0.62), (-0.18, 0.24),
             (0.45, 0.24)]  # x, y with high h is high on page
for i, p in enumerate(party):
    source_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), f'assets\\{p.name}.png')
    fig_tot.add_layout_image(
        dict(
            source=Image.open(source_path),
            x=positions[i][0], y=positions[i][1],
            sizex=0.25, sizey=0.25,
        )
    )

app.layout = html.Div(children=[
    html.H1(children='Poké Dashboard'),
    html.Div(children='An essential tool for every PokéProgrammer'),


    # html.Div(id='my-output'),
    # dcc.Graph(
    #     id='example-graph',
    #     figure=fig
    # ),
    dcc.Graph(
        id='chart-output'
    ),
    dcc.Graph(
                id='chart-hp'
    ),
    # html.Div(dcc.Input(id='input-on-submit', type='text')),
    html.Button('Start VBA', id='vba-button', n_clicks=0),
    html.Button('Train Pokemon', id='button', n_clicks=0),

    # html.P(id='placeholder'),
    html.Div(id='hidden-div', style={'display':'none'}),
    html.Div(id='hidden-div2', style={'display': 'none'}),
    # *pokemon_images,
    # html.Div(id='live-update-time'),

    # html.Div(id='chart_output'),
    # html.Img(id='image_output',src='path'),#f'assets/{poke_name}.png')

    dcc.Interval(
        id='interval-component',
        interval=1 * 1000,  # in milliseconds
        n_intervals=0
    )
])

# pokemon_images=[]
# for p in OwnPokemon.party:
#     pokemon_images.append(html.Img(src=f'assets/{p.name}.png'))

# @app.callback(Output(component_id='my-output', component_property='children'),
#               Input('interval-component', 'n_intervals'))
# def return_time(n):
#     return 'Output: {}'.format(str(datetime.utcnow()))




# @app.callback(Output(component_id='image-output', component_property='path'),
#               Input(component_id='my-input', component_property='value'))
# def pokeimage(pokename):
#     return html.Img(src='assets/charmander.png')


@app.callback(
    Output('hidden-div', 'children'),
    Input('button', 'n_clicks'),
    # State('input-on-submit', 'value')
)
def train_action(n_clicks):
    if n_clicks>0:
        from main import train
        train(9, 'all', ('route1', 161), ('route1', 168), ('viridian_city_pc', 4, 'up'))
        print(f'test {datetime.utcnow()}')
    return


@app.callback(
    Output('hidden-div2', 'children'),
    Input('vba-button', 'n_clicks'),
    # State('input-on-submit', 'value')
)
def open_vba_action(n_clicks):
    if n_clicks>0:
        from fundamentals.open_vba import open_vba
        open_vba()
    return


@app.callback(Output(component_id='chart-output', component_property='figure'),
              Input('interval-component', 'n_intervals'))
def level_graph(n):
    from fight.pokemon import OwnPokemon

    df = pd.DataFrame(columns=['Pokemon', 'Level'])
    for p in OwnPokemon.party:
        df = df.append({'Pokemon':p.own_name, 'Level':p.level}, ignore_index=True)

    # df = pd.DataFrame({
    #     "Pokemon": ["Charmander", "Pidgey", "Rattata"],
    #     "Level": [1,2,3],
    # })

    fig = px.bar(df, x="Pokemon", y="Level", barmode="group")

    return fig




# @app.callback(Output(component_id='chart-hp', component_property='figure'),
#               Input('interval-component', 'n_intervals'))
# def hp_chart(n):
#     from fight.pokemon import OwnPokemon
#
#     df = pd.DataFrame(columns=['Pokemon', 'HP'])
#     for p in OwnPokemon.party:
#         df = df.append({'Pokemon':p.own_name, 'HP':p.current_hp/p.stats['hp']}, ignore_index=True)
#
#     fig = px.bar(df, x="Pokemon", y="HP",color='HP', range_y=[0,1],
#                  #color_continuous_scale=["red", "yellow","green"]
#                  range_color=[0.0, 1.0],
#                  color_continuous_scale=[(0.00, "red"),   (0.20, "red"),
#                                           (0.20, "yellow"), (0.50, "yellow"),
#                                           (0.50, "green"),  (1.00, "green")])
#
#     return fig

@app.callback(Output(component_id='chart-hp', component_property='figure'),
              Input('interval-component', 'n_intervals'))
def party_charts(n):
    from fight.pokemon import OwnPokemon

    party = OwnPokemon.party

    figs = []
    titles=[]
    for pokemon in party:
        figs.append(go.Bar(x=list(pokemon.stats.values()), y=list(pokemon.stats.keys()), orientation='h'))
        titles.append(f"<b>{pokemon.name}</b>    level: {pokemon.level}")

    fig_tot = make_subplots(rows=3, cols=2,horizontal_spacing=0.25,
                            subplot_titles=titles)

    # add subplots
    for i, fig in enumerate(figs):
        fig_tot.add_trace(
            fig,
            row=int(i/2)+1, col=i%2+1)

    fig_tot.update_layout(
        autosize=False,
        height=600,
        width=1000,
        # bargap=0.15,
        # bargroupgap=0.1,
        barmode="stack",
        hovermode="x",
        showlegend = False,
        margin=dict(l=200),
        title=f'<b>Party</b>'
    )

    # add the images
    positions = [(-0.18, 1),(0.45, 1),(-0.18, 0.62), (0.45, 0.62), (-0.18, 0.24),(0.45, 0.24) ] # x, y with high h is high on page
    for i, p in enumerate(party):
        source_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), f'assets\\{p.name}.png')
        fig_tot.add_layout_image(
            dict(
                source=Image.open(source_path),
                x=positions[i][0], y=positions[i][1],
                sizex=0.25, sizey=0.25,
            )
        )
    return fig_tot

def test_charts(n):

    df = pd.DataFrame({
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Amount": [4, 1, 2, 2, 4, 6],
        "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
    })

    fig = go.Bar(x=[4, 1, 2, 2, 4, 6],
                 y=["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
                orientation= 'h')
    figs = [fig, fig]

    fig_tot = make_subplots(rows=1, cols=2,horizontal_spacing=0.25)

    # add subplots
    for i, fig in enumerate(figs):
        fig_tot.add_trace(
            fig,
            row=int(i/2)+1, col=i%2+1)

    fig_tot.update_layout(
        autosize=False,
        height=600,
        width=1000,
        # bargap=0.15,
        # bargroupgap=0.1,
        barmode="stack",
        hovermode="x",
        showlegend = False,
        margin=dict(l=200),
        title=f'<b>Party</b>'
    )

    # add the images
    positions = [(-0.18, 1),(0.45, 1),(-0.18, 0.62), (0.45, 0.62), (-0.18, 0.24),(0.45, 0.24) ] # x, y with high h is high on page
    for i, p in enumerate(party):
        source_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), f'assets\\{p.name}.png')
        fig_tot.add_layout_image(
            dict(
                source=Image.open(source_path),
                x=positions[i][0], y=positions[i][1],
                sizex=0.25, sizey=0.25,
            )
        )
    return (fig_tot)



def create_pidgey_chart():
    pokemon_name = 'pidgey'

    # im_cv = cv2.imread(f'assets\\{pokemon_name}.png')
    # img = cv2.cvtColor(im_cv, cv2.COLOR_BGR2RGB)

    source_path = os.path.join(os.getcwd(), f'assets\\{pokemon_name}.png')
    img = np.array(Image.open(source_path))

    fig = px.imshow(img)

    df = pd.DataFrame({
        "hp": ["hp"],
        "Amount": [0.7]})

    fig = px.bar(df, y="hp", x="Amount", orientation='h', range_x=[0,1])

    df = pd.DataFrame({
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Amount": [4, 1, 2, 2, 4, 6],
        "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
    })

    fig = px.bar(df, y="Fruit", x="Amount", color="City", barmode="group", orientation= 'h')


    # fig.update_layout(coloraxis_showscale=False)
    # fig.update_xaxes(showticklabels=False)
    # fig.update_yaxes(showticklabels=False)

    fig.add_layout_image(
        dict(
            source=Image.open(source_path),
            xref="paper", yref="paper",
            x=0, y=1.05,
            sizex=1, sizey=1,
            xanchor="left", yanchor="top"
        )
    )

    fig.update_layout(
        autosize=False,
        height=300,
        width=500,
        bargap=0.15,
        bargroupgap=0.1,
        barmode="stack",
        hovermode="x",

        margin=dict(r=20, l=100, b=75, t=125),
        title="Pidgey",
    )

    fig.show()

# app.layout = html.Div([
#     html.Img(src='assets/char.png')
# ])

if __name__ == '__main__':
    app.run_server(debug=True)

    # party_charts(1).show()

    # from fight.pokemon import OwnPokemon
    #
    # party = OwnPokemon.party
    #
    # figs = []
    # titles=[]
    # for pokemon in party:
    #     figs.append(go.Bar(x=list(pokemon.stats.values()), y=list(pokemon.stats.keys()), orientation='h'))
    #     titles.append(f"<b>{pokemon.name}</b>    level: {pokemon.level}")
    #
    # fig_tot = make_subplots(rows=3, cols=2,horizontal_spacing=0.25,
    #                         subplot_titles=titles)
    #
    # # add subplots
    # for i, fig in enumerate(figs):
    #     fig_tot.add_trace(
    #         fig,
    #         row=int(i/2)+1, col=i%2+1)
    #
    # fig_tot.update_layout(
    #     autosize=False,
    #     height=600,
    #     width=1000,
    #     # bargap=0.15,
    #     # bargroupgap=0.1,
    #     barmode="stack",
    #     hovermode="x",
    #     showlegend = False,
    #     margin=dict(l=200),
    #     title=f'<b>Party</b>'
    # )
    #
    # # add the images
    # positions = [(-0.18, 1),(0.45, 1),(-0.18, 0.62), (0.45, 0.62), (-0.18, 0.24),(0.45, 0.24) ] # x, y with high h is high on page
    # for i, p in enumerate(party):
    #     source_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), f'assets\\{p.name}.png')
    #     fig_tot.add_layout_image(
    #         dict(
    #             source=Image.open(source_path),
    #             x=positions[i][0], y=positions[i][1],
    #             sizex=0.25, sizey=0.25,
    #         )
    #     )

    # fig_tot.show()



    test=1





















    # from fight.pokemon import OwnPokemon
    #
    # pokemon = OwnPokemon.party[0]
    #
    # source_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), f'assets\\{pokemon.name}.png')
    # img = np.array(Image.open(source_path))
    #
    # df = pd.DataFrame({'stats':list(pokemon.stats.keys()), 'value': list(pokemon.stats.values())})
    #
    # # fig = go.Bar(df, y="stats", x="value", orientation='h', barmode='group',category_orders={'stats': list(pokemon.stats.keys())} )
    #
    # fig = go.Bar(x=list(pokemon.stats.values()), y=list(pokemon.stats.keys()), orientation='h')
    #
    # fig_tot = make_subplots(rows=3, cols=2,horizontal_spacing=0.25,
    #                         subplot_titles=[f"<b>{pokemon.name}</b>    level: {pokemon.level}",
    #                                         'plot',
    #                                         'plot3',
    #                                         'plot4'])
    #
    # fig_tot.add_trace(
    #     fig,
    #     row=1, col=1
    # )
    #
    # fig_tot.add_trace(
    #     fig,
    #     row=1, col=2
    # )
    # fig_tot.add_trace(
    #     fig,
    #     row=2, col=1
    # )
    # fig_tot.add_trace(
    #     fig,
    #     row=2, col=2
    # )
    #
    #
    # fig_tot.update_layout(
    #     autosize=False,
    #     height=600,
    #     width=1000,
    #     # bargap=0.15,
    #     # bargroupgap=0.1,
    #     barmode="stack",
    #     hovermode="x",
    #     showlegend = False,
    #     margin=dict(l=200),
    #     title=f'<b>Party</b>'
    # )
    #
    # fig_tot.add_layout_image(
    #     dict(
    #         source=Image.open(source_path),
    #         # xref="paper", yref="paper",
    #         x=-0.18, y=0.62,
    #         sizex=0.25, sizey=0.25,
    #         # xanchor="left", yanchor="top"
    #     )
    # )
    # fig_tot.add_layout_image(
    #     dict(
    #         source=Image.open(source_path),
    #         # xref="paper", yref="paper",
    #         x=-0.18, y=1,
    #         sizex=0.25, sizey=0.25,
    #         # xanchor="left", yanchor="top"
    #     )
    # )
    # fig_tot.add_layout_image(
    #     dict(
    #         source=Image.open(source_path),
    #         # xref="paper", yref="paper",
    #         x=0.45, y=1,
    #         sizex=0.25, sizey=0.25,
    #         # xanchor="left", yanchor="top"
    #     )
    # )
    # # right middle
    # fig_tot.add_layout_image(
    #     dict(
    #         source=Image.open(source_path),
    #         # xref="paper", yref="paper",
    #         x=0.45, y=0.62,
    #         sizex=0.25, sizey=0.25,
    #         # xanchor="left", yanchor="top"
    #     )
    # )

