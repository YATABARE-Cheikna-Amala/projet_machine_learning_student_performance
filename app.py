import streamlit as st
import pandas as pd
from visualisation import afficher_page_visualisation
from introduction import page_introduction
from modelisation import page_modelisation
from prediction import page_prediction  # Assurez-vous que page_prediction est importé

# Définir la configuration de la page en premier
st.set_page_config(page_title="Student Performance Analysis", page_icon="📊", layout="wide")

st.markdown("""
    <style>
    /* Arrière-plan global */
    .main {
        background-color: #f4f7fb;
        background-image: linear-gradient(135deg, #e0f7fa, #f4f4f9);
    }
    
    /* Appliquer une ombre douce aux titres */
    h1, h2, h3, h4, h5, h6 {
        color: #4CAF50;
        font-family: 'Arial', sans-serif;
        text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.1);
    }
    
    /* Modification des sous-titres avec plus de contraste */
    .subheader {
        font-size: 22px;
        color: #555555;
        font-family: 'Verdana', sans-serif;
        font-weight: 600;
    }

    /* Style des boutons avec animation de survol */
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 14px 28px;
        border-radius: 8px;
        font-size: 16px;
        font-weight: bold;
        transition: background-color 0.3s ease, transform 0.2s ease;
    }

    .stButton button:hover {
        background-color: #45a049;
        transform: translateY(-2px);
    }

    /* Personnalisation des champs de saisie avec un effet de focus */
    .stNumberInput input, .stTextInput input, .stSelectbox select {
        background-color: #ffffff;
        border-radius: 6px;
        border: 1px solid #cccccc;
        padding: 10px;
        font-size: 16px;
        transition: border 0.3s ease, box-shadow 0.3s ease;
    }

    .stNumberInput input:focus, .stTextInput input:focus, .stSelectbox select:focus {
        border-color: #4CAF50;
        box-shadow: 0 0 8px rgba(76, 175, 80, 0.3);
    }

    /* Améliorer l'apparence des sélecteurs */
    .stSelectbox select {
        color: #333333;
        background-color: #f9f9f9;
        border: 1px solid #ccc;
        border-radius: 6px;
        padding: 8px;
        font-size: 16px;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
    }

    .stSelectbox select:focus {
        border-color: #4CAF50;
        box-shadow: 0 0 8px rgba(76, 175, 80, 0.3);
    }

    /* Style des alertes avec une touche douce */
    .stAlert {
        background-color: #fffbe7;
        border: 1px solid #f0e68c;
        color: #dca100;
        border-radius: 6px;
        padding: 12px;
        font-weight: 600;
    }

    /* Section de navigation dans la barre latérale */
    .block-container {
        padding: 20px;
        border-radius: 12px;
        border: 2px solid #e1e1e1;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
        background-color: #ffffff;
    }

    /* Ajouter des bordures arrondies et des ombres aux sections */
    .stSlider, .stNumberInput, .stSelectbox {
        margin-bottom: 20px;
    }

    /* Améliorer la lisibilité des textes dans la sidebar */
    .sidebar .sidebar-content {
        font-family: 'Roboto', sans-serif;
        color: #333333;
    }

    .sidebar .sidebar-content h2 {
        color: #4CAF50;
    }
    </style>
""", unsafe_allow_html=True)


# Ajouter un titre principal
st.title("Student Performance Analysis 📊")
st.markdown("""
    Bienvenue dans l'application d'analyse des performances des étudiants !  
    Cette application vous permet d'explorer différentes techniques d'analyse, y compris l'introduction des données, la modélisation, et la visualisation des résultats.  
    Vous pouvez naviguer entre les différentes pages pour découvrir les insights cachés dans les données.
""")

PAGES = {
    "Introduction": page_introduction,
    "Modélisation": lambda: page_modelisation(data),  # Passer data ici
    "Visualisation": lambda:afficher_page_visualisation(data),
    "Prédiction": page_prediction   # Pas besoin de data ici
}
# Sélection de la page via un menu déroulant dans la barre latérale
page = st.sidebar.selectbox(
    "Choisissez une page",
    options=list(PAGES.keys()),
    label_visibility="collapsed"  # Masquer l'étiquette de la sélection
)

# Ajout d'une section dans la barre latérale pour la description et les informations sur le projet
st.sidebar.header("Navigation")
st.sidebar.markdown("""
    L'application est structurée autour de trois principales sections :
    - **Introduction** : Un aperçu des données et du projet.
    - **Modélisation** : Utilisation de modèles de régression pour prédire les performances des étudiants.
    - **Visualisation** : Graphiques interactifs pour explorer les résultats.
    - **Prédiction** : Modèles de machine learning pour prédire les scores d'examen en fonction des données.
""")

# Ajout d'un petit texte d'information dans la barre latérale (facultatif)
st.sidebar.markdown("### 📊 Student Performance Data")
st.sidebar.markdown("Cette analyse est basée sur les facteurs influençant la performance des étudiants.")
st.sidebar.markdown("---")

# Chargement des données
data = pd.read_csv("https://raw.githubusercontent.com/OusseynouDIOP16/IML_STUDENT_PERFORMANCE/main/StudentPerformanceFactors.csv", sep=",")

# Appel de la fonction de la page sélectionnée
PAGES[page]()  # Remarquez qu'on ne passe plus `data` ici, car page_prediction ne prend pas d'argument
