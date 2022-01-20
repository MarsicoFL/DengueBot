import re
from typing import Collection

import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

df = pd.read_csv('dengue.csv')
px.set_mapbox_access_token("pk.eyJ1IjoiYWd1c3RpbmRkZmVybmFuZGV6IiwiYSI6ImNreWFqanQzdTAyNmQycXFlMzdleWVyY3gifQ.aPHHvQb5czl7goVd9x8f1A")

blackbold={'color':'black', 'font-weight': 'bold'}


fig1 = px.pie(
    data_frame = df,
    names = df['tipo'],
    color = df['tipo'],
    color_discrete_map =  {'Basural a cielo abierto': '#B68E00',
    'Acumulación de basura en la calle': '#00FE35',
    'Neumáticos en desuso': '#6A76FC',
    'Chatarra, chapas u otros objetos voluminosos al descubierto': '#FF9616',
    'Recipiente': '#FE00CE',
    'Terreno sin desmalezar': '#FC6955',
    'Vivienda con objetos que acumulan agua':'#F6F926'}, 
    title = 'Porcentaje de cada tipo de criadero',
    width = 750,
    height= 500)


fig2 = px.pie(
    data_frame = df,
    names = df['espacio'],
    color = df['espacio'],
    color_discrete_map =  {'¡Sí pude eliminarlo!': '#636EFA',
    'Predio deshabilitado o sin acceso': '#EF553B',
    'No se encuentra lx residente presente': '#FF6692',
    'El gran volumen requiere asistencia': '#FFA15A',
    'Lx residente no accedió a realizar la acción': '#FF6692'},
    title = 'Porcentaje de cada acción realizada',
    width = 630,
    height= 500
)


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])



app.layout = dbc.Container([
    dbc.Row(
    dbc.Col(html.H1("Proyecto DengueBot - Provincia de Buenos Aires",
    className = "text-center" ),
    width= 12)
),

dbc.Row([
    dbc.Col([
        html.Label(children=['Selección general: '], style=blackbold),
            dcc.RadioItems(id='general',
                    options=[{'label':  'Tipo de criadero', 'value': 'tip'},
                            {'label': 'Acción realizada', 'value': 'acc'},
                            {'label': 'Ambas', 'value': 'amb'}],
                    value= 'amb',
            ),
        html.Label(children=['Tipo de criadero: '], style=blackbold),
            dcc.Checklist(id='tipo',
                    options=[{'label':str(b),'value':b} for b in sorted(df['tipo'].unique())],
                    #value=[b for b in sorted(df['tipo'].unique())],
                    value = []
            ),

            # accion_checklist
            html.Label(children=['Acción realizada: '], style=blackbold),
            dcc.Checklist(id='accion',
                    options=[{'label':str(b),'value':b} for b in sorted(df['espacio'].unique())],
                    #value=[b for b in sorted(df['espacio'].unique())],
                    value=[]
            ),
            dcc.Graph(id='graph', config={'displayModeBar': False, 'scrollZoom': True} )
        

    ] )

], align ='start', justify = 'start'),

dbc.Row([
    dbc.Col([dcc.Graph(
        id='torta1',
        figure=fig1)],width={'size':6, 'offset':0, 'order':1},#xs=12, sm=12, md=12, lg=5, xl=5
        ),
        
    dbc.Col([dcc.Graph(
        id='torta2',
        figure=fig2)],width={'size':5, 'offset':0, 'order':2}#xs=12, sm=12, md=12, lg=5, xl=5
        )
]),

])

@app.callback(
    Output("accion", "options"),
    Output("tipo", "options"), 
    Input("general", "value"),
)

def update(radio):
    """
    Selección general
    """
    if "tip" in radio:
        return [
            {'label':str(b),'value':b, "disabled": True} for b in sorted(df['espacio'].unique())
        ], [{'label':str(b),'value':b} for b in sorted(df['tipo'].unique())]  
    
    elif "acc" in radio:
        return [
            {'label':str(b),'value':b } for b in sorted(df['espacio'].unique())
        ], [{'label':str(b),'value':b, "disabled": True} for b in sorted(df['tipo'].unique())]
    
    elif "amb" in radio:
        return [
            {'label':str(b),'value':b} for b in sorted(df['espacio'].unique())
        ], [{'label':str(b),'value':b} for b in sorted(df['tipo'].unique())]



@app.callback(Output('graph', 'figure'),
              [Input('tipo', 'value'),
               Input('accion', 'value')])

def update_figure(chosen_tipo,chosen_accion):
    print(chosen_tipo)
    print(chosen_accion)


    if len(chosen_tipo) == 0 and len(chosen_accion) > 0:
        df_sub = df[df['espacio'].isin(chosen_accion)]
        fig = px.scatter_mapbox(df_sub, 
                        lat="latitud", 
                        lon="longitud", 
                        color="espacio",
                        hover_name= "espacio",  
                        hover_data=["espacio", "fecha"],
                        color_discrete_map =  {'¡Sí pude eliminarlo!': '#636EFA',
                                                'Predio deshabilitado o sin acceso': '#EF553B',
                                                'No se encuentra lx residente presente': '#FF6692',
                                                'El gran volumen requiere asistencia': '#FFA15A',
                                                'Lx residente no accedió a realizar la acción': '#FF6692'},
                        zoom=10,
                        height=1000,
                        center={"lat":-34.60652, "lon":-58.43557})
        return fig
    
    if len(chosen_tipo) > 0 and len(chosen_accion) == 0:
        df_sub = df[df['tipo'].isin(chosen_tipo)]
        fig = px.scatter_mapbox(df_sub, 
                        lat="latitud", 
                        lon="longitud", 
                        color="tipo",
                        hover_name= "tipo",  
                        hover_data=["espacio", "fecha"],
                        color_discrete_map =  {'Basural a cielo abierto': '#B68E00',
                                                'Acumulación de basura en la calle': '#00FE35',
                                                'Neumáticos en desuso': '#6A76FC',
                                                'Chatarra, chapas u otros objetos voluminosos al descubierto': '#FF9616',
                                                'Recipiente': '#FE00CE',
                                                'Terreno sin desmalezar': '#FC6955',
                                                'Vivienda con objetos que acumulan agua':'#F6F926'},
                        zoom=10,
                        height=1000,
                        center={"lat":-34.60652, "lon":-58.43557})
        return fig

    else:

        df_sub = df[(df['tipo'].isin(chosen_tipo)) &
                    (df['espacio'].isin(chosen_accion))]
        print(df_sub)

    if len(df_sub) == 0:
        df_sub = df_sub[['latitud', 'longitud']]
        df_sub = df_sub.append({'latitud': -34.60652, 'longitud' :-58.43557 }, ignore_index=True)
        fig = px.scatter_mapbox(df_sub, 
                        lat= "latitud", 
                        lon= "longitud",
                        zoom = 10,
                        height=1000,
                        center={"lat":-34.60652, "lon":-58.43557})
        return fig
    else: 

        fig = px.scatter_mapbox(df_sub, 
                        lat="latitud", 
                        lon="longitud", 
                        color="tipo",
                        hover_name= "tipo",  
                        hover_data=["espacio", "fecha"],
                        color_discrete_map =  {'Basural a cielo abierto': '#B68E00',
                                                'Acumulación de basura en la calle': '#00FE35',
                                                'Neumáticos en desuso': '#6A76FC',
                                                'Chatarra, chapas u otros objetos voluminosos al descubierto': '#FF9616',
                                                'Recipiente': '#FE00CE',
                                                'Terreno sin desmalezar': '#FC6955',
                                                'Vivienda con objetos que acumulan agua':'#F6F926'},
                        zoom=10,
                        height=1000,
                        center={"lat":-34.60652, "lon":-58.43557})
        return fig


if __name__ == '__main__':
    
    app.run_server(debug=False, port=8050)

