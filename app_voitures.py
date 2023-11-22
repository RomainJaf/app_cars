import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly_express as px
from streamlit_dynamic_filters import DynamicFilters

st.header('Hello, welcome to my application!')
st.markdown("J'applique mon filtre uniquement sur les 3 premiers graphes. Les commentaires sur les graphes disparaissent si vous filtrez le dataframe pour rester cohérents.")

link = "https://raw.githubusercontent.com/murpi/wilddata/master/quests/cars.csv"

df_cars = pd.read_csv(link)

# création du filtre
dynamic_filters = DynamicFilters(df_cars, filters=['continent'])

# affichage du dataframe
dynamic_filters.display_df() 

# création de la zone du filtre en barre latérale
with st.sidebar:
    dynamic_filters.display_filters()

df_filtered = dynamic_filters.filter_df()

# on enregistre la condition
conditon = {
        'test': ((' US.' in df_filtered['continent'].values) &
                 (' Europe.' in df_filtered['continent'].values) &
                 (' Japan.' in df_filtered['continent'].values))
    }

# graphique pour afficher le temps pour aller à 60 m/h en fonction du poids
fig_vitesse = px.bar(df_filtered,  x="weightlbs", y="time-to-60", title='temps pour aller à 60 m/h en fonction du poids',
              labels = {"weightlbs" : "Poids", "time-to-60" : "temps"})
st.write(fig_vitesse)

if conditon['test']:
    st.markdown("On voit que le poids n'est pas un facteur déterminant de la vitesse. Des voitures plus lourdes vont aussi vites à 60 m/h que des voitures légères.")

# graphique pour afficher temps pour aller à 60 m/h en fonction de l'année
fig_vitesse_year = px.bar(df_filtered,  x="year", y="time-to-60", title='temps pour aller à 60 m/h en fonction de l\'année',
              labels = {"year" : "année", "time-to-60" : "temps"})
st.write(fig_vitesse_year)

if conditon['test']:
    st.markdown("Il n'y a pas de corrélation entre l'année de sortie de la voiture et le temps pour aller à 60 m/h")

# matrice de corrélation
viz_correlation = sns.heatmap(df_filtered.select_dtypes(include='number').corr(), center=0, cmap = sns.color_palette("vlag", as_cmap=True))
plt.title("Heatmap")
st.pyplot(viz_correlation.figure)

# camembert en fonction de l'origine
fig_camembert = px.pie(df_cars, values= df_cars.index, names='continent', title='Pays d\'origine des voitures')
st.write(fig_camembert)

st.markdown("La plupart des voitures du dataframe viennent des Etats-Unis")
