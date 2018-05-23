#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 10:50:06 2018

@author: melanie
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

import parametres

NOM_DOSSIER = parametres.NOM_DOSSIER
NOM_FICHIER_SORTIE = parametres.NOM_FICHIER_SORTIE
NOM_FICHIER_RESULTATS = parametres.NOM_FICHIER_RESULTATS
NOM_FICHIER_TEMPERATURES = parametres.NOM_FICHIER_TEMPERATURES

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

# lecture des derniers resultats
RESULTATS = pd.read_csv(NOM_DOSSIER + NOM_FICHIER_RESULTATS)
RES_MODEL = pd.read_csv(NOM_DOSSIER + NOM_FICHIER_SORTIE, names=['Valeur'])
TEMPERATURES = pd.read_csv(NOM_DOSSIER + NOM_FICHIER_TEMPERATURES, names=['Temperature'])

app = dash.Dash()
app.css.append_css({"external_url": "/static/{}".format('style.css')})

app.layout = html.Div(children=[
    dcc.Tabs(
        tabs=[
            {'label': 'Resultats', 'value': 1},
			{'label': 'Isothermes estimes', 'value': 2},
        ],
        value=3,
        id='tabs'
    ),
    html.H1(children='Bucole 2'),

#    html.Div(children='Traitement du fichier ' + RES_MODEL[1]),

    html.Div([
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


    ], style={'width': '49%', 'display': 'inline-block', 'align': 'center'})
])

if __name__ == '__main__':
    app.run_server(debug=True)
