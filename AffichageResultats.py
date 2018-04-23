# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

import parametres

nomDossier = parametres.NOM_DOSSIER
nomFichierSortie = parametres.NOM_FICHIER_SORTIE
nomFichierResultats = parametres.NOM_FICHIER_RESULTATS
nomFichierTemperatures = parametres.NOM_FICHIER_TEMPERATURES

def arrondi(valeur):
    try: 
        float(valeur)
        return '%.3f' %(float(valeur))
    except:
        return valeur

def generate_table(dataframe, col, hauteur, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th('Donnée'), html.Th(col)])] +

        # Body
        [html.Tr([
            html.Td(dataframe.index[i], style=dict(textAlign="center")), html.Td(arrondi(dataframe.iloc[i][col]), style=dict(textAlign="center"))
        ]) for i in range(min(len(dataframe), max_rows))],
		style={'height': hauteur}
)
	
# lecture des derniers resultats
resultats = pd.read_csv(nomDossier + nomFichierResultats)
resModel = pd.read_csv(nomDossier + nomFichierSortie, names = ['Valeur'])
temperatures = pd.read_csv(nomDossier + nomFichierTemperatures, names = ['Temperature'])

app = dash.Dash()
app.css.append_css({"external_url": "/static/{}".format('style.css')})

app.layout = html.Div(children=[
    html.H1(children='Bucole 2'),

    html.Div(children='''
        
    '''),

	html.Div([
		dcc.Graph(
			figure=go.Figure(
				data=[
					go.Scatter(
						x = resultats[resultats['Temperature'] == temperatures['Temperature'][0]]['Temps'],
						y = resultats[resultats['Temperature'] == temperatures['Temperature'][0]]['Sestime'],
						mode = 'lines',
						name = 'S estime'
					),
					go.Scatter(
						x = resultats[resultats['Temperature'] == temperatures['Temperature'][0]]['Temps'],
						y = resultats[resultats['Temperature'] == temperatures['Temperature'][0]]['S'],
						mode = 'lines',
						name = 'S mesure'
					)
				],
				layout=go.Layout(
					title='Test courbe a 170',
					showlegend=True,
					legend=go.Legend(
						x=0.8,
						y=0.95
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
						x = resultats[resultats['Temperature'] == temperatures['Temperature'][1]]['Temps'],
						y = resultats[resultats['Temperature'] == temperatures['Temperature'][1]]['Sestime'],
						mode = 'lines',
						name = 'S estime'
					),
					go.Scatter(
						x = resultats[resultats['Temperature'] == temperatures['Temperature'][1]]['Temps'],
						y = resultats[resultats['Temperature'] == temperatures['Temperature'][1]]['S'],
						mode = 'lines',
						name = 'S mesure'
					)
				],
				layout=go.Layout(
					title='Test courbe a 150',
					showlegend=True,
					legend=go.Legend(
						x=0.8,
						y=0.95
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
						x = resultats[resultats['Temperature'] == temperatures['Temperature'][2]]['Temps'],
						y = resultats[resultats['Temperature'] == temperatures['Temperature'][2]]['Sestime'],
						mode = 'lines',
						name = 'S estime'
					),
					go.Scatter(
						x = resultats[resultats['Temperature'] == temperatures['Temperature'][2]]['Temps'],
						y = resultats[resultats['Temperature'] == temperatures['Temperature'][2]]['S'],
						mode = 'lines',
						name = 'S mesure'
					)
				],
				layout=go.Layout(
					title='Test courbe a 130',
					showlegend=True,
					legend=go.Legend(
						x=0.8,
						y=0.95
					),
					margin=go.Margin(l=40, r=0, t=40, b=30)
				)
			),
			style={'height': 300},
			id='graph3'
		),
		
		generate_table(resModel[1:], 'Valeur', 300)
		
		
	], style={'width': '49%', 'display': 'inline-block', 'align': 'center'})
])

if __name__ == '__main__':
    app.run_server(debug=True)