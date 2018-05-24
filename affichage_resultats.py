#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 10:50:06 2018

@author: melanie
"""

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy

import parametres
import calcul_params

TEMPS_AFFICHE = 150000
NOM_DOSSIER = parametres.NOM_DOSSIER
NOM_FICHIER_SORTIE = parametres.NOM_FICHIER_SORTIE
NOM_FICHIER_RESULTATS = parametres.NOM_FICHIER_RESULTATS
NOM_FICHIER_TEMPERATURES = parametres.NOM_FICHIER_TEMPERATURES
NOM_FICHIER_COEFFICIENTS = parametres.NOM_FICHIER_COEFFICIENTS

def arrondi(valeur):
    """ fonction d'arrondi des float pour l'affichage
	3 chiffres après la virgule affiches"""
    try:
        float(valeur)
        return '%.3f' %(float(valeur))
    except:
        return valeur

def generate_table(dataframe, col, hauteur, max_rows=10):
    """ fonction permettant d'afficher un dataframe
	sous forme de tableau """
    return html.Table(
        # Header
        [html.Tr([html.Th('Donnée'), html.Th(col)])] +

        # Body
        [html.Tr([
            html.Td(dataframe.index[i], style=dict(textAlign="center")), \
			html.Td(arrondi(dataframe.iloc[i][col]), style=dict(textAlign="center"))
        ]) for i in range(min(len(dataframe), max_rows))],
        style={'height': hauteur}
    )

def calcul_isothemes(param):
    donnees_isothermes = []
    for i in range(100, 210, 10):
        for j in range(TEMPS_AFFICHE):
            donnees_isothermes.append(calcul_params.fun(param['0'], i, j, param['0'][0]))
    return pd.Series(donnees_isothermes)

# lecture des derniers resultats
RESULTATS = pd.read_csv(NOM_DOSSIER + NOM_FICHIER_RESULTATS)
RES_MODEL = pd.read_csv(NOM_DOSSIER + NOM_FICHIER_SORTIE, names=['Valeur'])
TEMPERATURES = pd.read_csv(NOM_DOSSIER + NOM_FICHIER_TEMPERATURES, names=['Temperature'])
COEFFICIENTS = pd.read_csv(NOM_DOSSIER + NOM_FICHIER_COEFFICIENTS)

test = calcul_isothemes(COEFFICIENTS)

app = dash.Dash()
app.css.append_css({"external_url": "/static/{}".format('style.css')})

app.layout = html.Div(children=[
    dcc.Tabs(
        tabs=[
            {'label': 'Resultats', 'value': 1},
			{'label': 'Isothermes estimes', 'value': 2},
        ],
        value=1,
        id='tabs'
    ),
    html.H1(children='Bucole 2'),
    html.Div(id='tab-output')
])

#@app.callback(Output('tab-output', 'children'), [Input('tabs', 'value')])
@app.callback(Output('tab-output', 'children'),
    [Input('tabs', 'value')])
def display_content(value):
    if value == 1:
        return html.Div(children=[html.Div([
        dcc.Graph(
            figure=go.Figure(
                data=[
                    go.Scatter(
                        x=RESULTATS[RESULTATS['Temperature Courbe'] == \
						TEMPERATURES['Temperature'][0]]['Temps'],
                        y=RESULTATS[RESULTATS['Temperature Courbe'] == \
						TEMPERATURES['Temperature'][0]]['Sestime'],
                        mode='lines',
                        name='S estime'
                    ),
                    go.Scatter(
                        x=RESULTATS[RESULTATS['Temperature Courbe'] == \
						TEMPERATURES['Temperature'][0]]['Temps'],
                        y=RESULTATS[RESULTATS['Temperature Courbe'] == \
						TEMPERATURES['Temperature'][0]]['S'],
                        mode='lines',
                        name='S mesure'
                    )
                ],
                layout=go.Layout(
                    title='Test courbe a '+ str(TEMPERATURES['Temperature'][0]),
                    showlegend=True,
                    legend=go.Legend(
                        x=0.8,
                        y=0.1
                    ),
                    margin=go.Margin(l=40, r=0, t=40, b=30)
                )
            ),
            style={'height': 300},
            id='graph1'
        ),
        dcc.Graph(
            figure=go.Figure(
                data=[
                    go.Scatter(
                        x=RESULTATS[RESULTATS['Temperature Courbe'] == \
						TEMPERATURES['Temperature'][1]]['Temps'],
                        y=RESULTATS[RESULTATS['Temperature Courbe'] == \
						TEMPERATURES['Temperature'][1]]['Sestime'],
                        mode='lines',
                        name='S estime'
                    ),
                    go.Scatter(
                        x=RESULTATS[RESULTATS['Temperature Courbe'] == \
                        TEMPERATURES['Temperature'][1]]['Temps'],
                        y=RESULTATS[RESULTATS['Temperature Courbe'] == \
                        TEMPERATURES['Temperature'][1]]['S'],
                        mode='lines',
                        name='S mesure'
                    )
                ],
                layout=go.Layout(
                    title='Test courbe a '+ str(TEMPERATURES['Temperature'][1]),
                    showlegend=True,
                    legend=go.Legend(
                        x=0.8,
                        y=0.1
                    ),
                    margin=go.Margin(l=40, r=0, t=40, b=30)
                )
            ),
            style={'height': 300},
            id='graph2'

        )
    ], style={'width': '49%', 'display': 'inline-block'}),

    html.Div([
        dcc.Graph(
            figure=go.Figure(
                data=[
                    go.Scatter(
                        x=RESULTATS[RESULTATS['Temperature Courbe'] == \
						TEMPERATURES['Temperature'][2]]['Temps'],
                        y=RESULTATS[RESULTATS['Temperature Courbe'] == \
						TEMPERATURES['Temperature'][2]]['Sestime'],
                        mode='lines',
                        name='S estime'
                    ),
                    go.Scatter(
                        x=RESULTATS[RESULTATS['Temperature Courbe'] == \
						TEMPERATURES['Temperature'][2]]['Temps'],
                        y=RESULTATS[RESULTATS['Temperature Courbe'] == \
						TEMPERATURES['Temperature'][2]]['S'],
                        mode='lines',
                        name='S mesure'
                    )
                ],
                layout=go.Layout(
                    title='Test courbe a '+ str(TEMPERATURES['Temperature'][2]),
                    showlegend=True,
                    legend=go.Legend(
                        x=0.8,
                        y=0.1
                    ),
                    margin=go.Margin(l=40, r=0, t=40, b=30)
                )
            ),
            style={'height': 300},
            id='graph3'
        ),

        generate_table(RES_MODEL[1:], 'Valeur', 300)


    ], style={'width': '49%', 'display': 'inline-block', 'align': 'center'})])

    traces = []
    colors = ['rgba(255, 0, 0, 0.8)', 'rgba(255, 127, 0, 0.8)', 'rgba(255, 214, 0, 0.8)', 'rgba(209, 255, 51, 0.8)', 'rgba(104, 255, 51, 0.8)', 'rgba(50, 255, 255, 0.8)', 'rgba(89, 189, 255, 0.8)', 'rgba(87, 38, 255, 0.8)','rgba(147, 38, 255, 0.8)','rgba(128, 64, 64, 0.8)','rgba(0, 0, 0, 0.8)']
    labels = list(range(100, 210, 10))
    for i in range(100, 210, 10):
        traces.append(go.Scatter(
            x=pd.Series(range(TEMPS_AFFICHE)),
            y=test[int((i-100)/10)*TEMPS_AFFICHE:int((1+(i-100)/10)*TEMPS_AFFICHE-1)],
            mode='lines',
            name=i,
            line=dict(color=colors[int((i-100)/10)], width=2),
            connectgaps=True,
    ))

    return html.Div(children=[
       dcc.Graph(
           figure=go.Figure(
                data=traces, layout=go.Layout(
                    title='Test courbes')
                ),
                id='graph4'
            )
        ])

	
if __name__ == '__main__':
    app.run_server(debug=True)
