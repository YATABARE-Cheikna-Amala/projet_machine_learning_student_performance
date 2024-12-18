import streamlit as st
import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import os

# Chargement des données
data = pd.read_csv("https://raw.githubusercontent.com/OusseynouDIOP16/IML_STUDENT_PERFORMANCE/main/StudentPerformanceFactors.csv", sep=",")

# Fonction de prédiction
def page_prediction():
    st.title("Page de Prédiction des Performances Étudiantes")

    # Vérifier si le modèle existe
    model_filename = "Gradient Boosting Regressor.joblib"
    if not os.path.exists(model_filename):
        st.error(f"Le modèle n'a pas été trouvé. Vérifiez que le fichier '{model_filename}' existe dans le répertoire.")
        return

    # Charger le modèle Gradient Boosting enregistré
    model = joblib.load(model_filename)
    
    # Définir les champs d'entrée pour les variables prédictives
    st.subheader("Entrez les informations de l'étudiant")
    
    # Variables d'entrée pour les prédicteurs
    hours_studied = st.number_input("Heures étudiées", min_value=0, max_value=100, value=50)
    attendance = st.number_input("Assiduité (en %)", min_value=0, max_value=100, value=80)
    parental_involvement = st.number_input("Implication des parents (en %)", min_value=0, max_value=100, value=70)
    access_to_resources = st.number_input("Accès aux ressources (en %)", min_value=0, max_value=100, value=80)
    extracurricular_activities = st.number_input("Activités extra-scolaires (en %)", min_value=0, max_value=100, value=60)
    sleep_hours = st.number_input("Heures de sommeil par nuit", min_value=0, max_value=24, value=8)
    previous_scores = st.number_input("Scores précédents", min_value=0, max_value=100, value=75)
    motivation_level = st.number_input("Niveau de motivation (1 à 10)", min_value=1, max_value=10, value=7)
    internet_access = st.number_input("Accès à Internet (en %)", min_value=0, max_value=100, value=90)
    tutoring_sessions = st.number_input("Sessions de tutorat", min_value=0, max_value=10, value=2)
    family_income = st.number_input("Revenu familial (en $)", min_value=0, max_value=200000, value=50000)
    teacher_quality = st.number_input("Qualité de l'enseignant (1 à 10)", min_value=1, max_value=10, value=8)
    school_type = st.selectbox("Type d'école", ['Public', 'Privé'])
    peer_influence = st.number_input("Influence des pairs (1 à 10)", min_value=1, max_value=10, value=6)
    physical_activity = st.number_input("Activité physique (en %)", min_value=0, max_value=100, value=50)
    learning_disabilities = st.selectbox("Troubles d'apprentissage", ['Non', 'Oui'])
    parental_education_level = st.selectbox("Niveau d'éducation des parents", ['Aucun', 'Secondaire', 'Université', 'Autre'])
    distance_from_home = st.number_input("Distance domicile-école (en km)", min_value=0, max_value=100, value=5)
    gender = st.selectbox("Genre", ['Masculin', 'Féminin'])
    
    # Collecte des entrées utilisateur dans un dictionnaire
    input_data = {
        "Hours_Studied": hours_studied,
        "Attendance": attendance,
        "Parental_Involvement": parental_involvement,
        "Access_to_Resources": access_to_resources,
        "Extracurricular_Activities": extracurricular_activities,
        "Sleep_Hours": sleep_hours,
        "Previous_Scores": previous_scores,
        "Motivation_Level": motivation_level,
        "Internet_Access": internet_access,
        "Tutoring_Sessions": tutoring_sessions,
        "Family_Income": family_income,
        "Teacher_Quality": teacher_quality,
        "School_Type": school_type,
        "Peer_Influence": peer_influence,
        "Physical_Activity": physical_activity,
        "Learning_Disabilities": learning_disabilities,
        "Parental_Education_Level": parental_education_level,
        "Distance_from_Home": distance_from_home,
        "Gender": gender,
    }
    
    # Convertir les entrées dans un DataFrame pour la prédiction
    input_df = pd.DataFrame([input_data])

    # Encodage des variables catégorielles
    le = LabelEncoder()
    input_df['School_Type'] = le.fit_transform(input_df['School_Type'])
    input_df['Learning_Disabilities'] = le.fit_transform(input_df['Learning_Disabilities'])
    input_df['Parental_Education_Level'] = le.fit_transform(input_df['Parental_Education_Level'])
    input_df['Gender'] = le.fit_transform(input_df['Gender'])
    
    # Si l'utilisateur appuie sur le bouton "Prédire"
    if st.button("Prédire"):
        # Faire la prédiction avec le modèle
        prediction = model.predict(input_df)
        
        # Afficher la prédiction
        st.subheader(f"Le score prédit pour cet étudiant est : {prediction[0]:.2f}")
