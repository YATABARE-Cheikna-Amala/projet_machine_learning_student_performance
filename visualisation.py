import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Charger la base de données existante
@st.cache_data
def charger_donnees():
    # Simuler la base "data" existante
    try:
        data = pd.read_csv("https://raw.githubusercontent.com/OusseynouDIOP16/IML_STUDENT_PERFORMANCE/main/StudentPerformanceFactors.csv", sep=",")
        return data
    except Exception as e:
        st.error(f"Erreur lors du chargement des données : {e}")
        return pd.DataFrame()

# Affichage des statistiques générales sous une forme améliorée
def afficher_statistiques_generales(total_students, moyenne_exam_score, moyenne_sleep, heures_etude_median):
    # Titre de la section
    st.subheader("📊 Statistiques Générales")

    # Création des colonnes pour un affichage propre et esthétique
    col1, col2, col3, col4 = st.columns(4)
    
    # Affichage des métriques sous forme de cartes avec icônes et valeurs
    col1.metric(
        label="Total Étudiants", 
        value=total_students, 
        delta_color="normal",  # Couleur du changement
        help="Nombre total d'étudiants dans la base de données"
    )
    
    col2.metric(
        label="Score Moyen Examen", 
        value=f"{moyenne_exam_score:.2f}", 
        delta_color="normal",
        help="Score moyen des étudiants lors de l'examen"
    )

    col3.metric(
        label="Sommeil Moyen (heures)", 
        value=f"{moyenne_sleep:.2f}", 
        delta_color="normal",
        help="Nombre moyen d'heures de sommeil des étudiants"
    )

    col4.metric(
        label="Médiane Heures Étudiées", 
        value=f"{heures_etude_median:.1f}", 
        delta_color="normal",
        help="Médiane des heures étudiées par les étudiants"
    )

    st.divider()  # Ajout d'un séparateur pour une meilleure organisation visuelle

# Fonction pour afficher toutes les visualisations
def afficher_page_visualisation(data):
    st.title("📊 Visualisation des Données Étudiantes")

    if data.empty:
        st.warning("Aucune donnée à afficher.")
        return

    # **Statistiques générales**
    total_students = data.shape[0]
    moyenne_exam_score = data["Exam_Score"].mean()
    moyenne_sleep = data["Sleep_Hours"].mean()
    heures_etude_median = data["Hours_Studied"].median()

    afficher_statistiques_generales(total_students, moyenne_exam_score, moyenne_sleep, heures_etude_median)

    # **Analyse des variables quantitatives**
    st.subheader("📈 Analyse des Variables Quantitatives")
    quantitative_vars = data.select_dtypes(include=['int64', 'float64']).columns
    var_quant = st.selectbox("Choisissez une variable quantitative", quantitative_vars)

    # Histogramme avec courbe KDE
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(data[var_quant], kde=True, color="skyblue", bins=30, ax=ax)
    plt.title(f"Distribution de {var_quant}")
    st.pyplot(fig)

    # Boxplot pour voir les valeurs aberrantes
    st.subheader("Boxplot de la variable sélectionnée")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data[var_quant], color="lightgreen", ax=ax)
    plt.xlabel(var_quant)
    st.pyplot(fig)

    st.divider()

    # **Analyse des variables qualitatives**
    st.subheader("📊 Analyse des Variables Qualitatives")
    qualitative_vars = data.select_dtypes(include=['object']).columns
    var_qual = st.selectbox("Choisissez une variable qualitative", qualitative_vars)

    # Diagramme en barres
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(x=var_qual, data=data, palette="Set2", ax=ax)
    plt.title(f"Répartition de {var_qual}")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Pie Chart
    st.subheader("Diagramme Circulaire")
    fig, ax = plt.subplots(figsize=(8, 8))
    data[var_qual].value_counts().plot.pie(autopct='%1.1f%%', startangle=90, cmap="Pastel1", ax=ax)
    plt.ylabel("")
    st.pyplot(fig)

    st.divider()

    # **Analyse croisée : Qualitatif vs Quantitatif**
    st.subheader("🔄 Analyse Croisée : Qualitatif vs Quantitatif")
    quant_cross = st.selectbox("Variable Quantitative", quantitative_vars, key="quant_cross")
    qual_cross = st.selectbox("Variable Qualitative", qualitative_vars, key="qual_cross")

    # Boxplot croisé
    st.subheader(f"Boxplot : {quant_cross} en fonction de {qual_cross}")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x=qual_cross, y=quant_cross, data=data, palette="coolwarm", ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Barplot moyen pour analyser la moyenne
    st.subheader(f"Barplot : Moyenne de {quant_cross} par {qual_cross}")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=qual_cross, y=quant_cross, data=data, palette="viridis", estimator="mean", ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.divider()

    # **Heatmap de corrélation des variables quantitatives**
    st.subheader("🔥 Matrice de Corrélation des Variables Quantitatives")
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(data[quantitative_vars].corr(), annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    plt.title("Matrice de Corrélation")
    st.pyplot(fig)

    st.divider()

    # **Statistiques détaillées pour les variables sélectionnées**
    st.subheader("📋 Statistiques Résumées")
    stats_var = st.multiselect("Sélectionnez les variables pour voir leurs statistiques", data.columns)
    if stats_var:
        st.write(data[stats_var].describe())
    else:
        st.warning("Aucune variable sélectionnée pour les statistiques.")

# Lancer l'application Streamlit
if __name__ == "__main__":
    data = charger_donnees()
    afficher_page_visualisation(data)
