import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import Ridge, Lasso, ElasticNet
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt
import json
import os
import joblib
from sklearn.preprocessing import StandardScaler

# Liste des variables explicatives et cible
features = [
    'Hours_Studied', 'Attendance', 'Sleep_Hours', 'Previous_Scores', 'Tutoring_Sessions',
    'Physical_Activity', 'Parental_Involvement_Encoded', 'Access_to_Resources_Encoded',
    'Motivation_Level_Encoded', 'Family_Income_Encoded', 'Teacher_Quality_Encoded',
    'Extracurricular_Activities_Encoded', 'Internet_Access_Encoded', 'Learning_Disabilities_Encoded',
    'School_Type_Encoded', 'Peer_Influence_Encoded', 'Parental_Education_Level_Encoded',
    'Distance_from_Home_Encoded', 'Gender_Encoded'
]
target = 'Exam_Score'

# Chargement des données
data = pd.read_csv("https://raw.githubusercontent.com/OusseynouDIOP16/IML_STUDENT_PERFORMANCE/main/data_clean.csv")

# Préparation des données
X = data[features]
y = data[target]

# Normalisation des données
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Fonction pour enregistrer le modèle avec joblib
def save_model(model, model_name):
    model_filename = os.path.join("models", f"{model_name}_model.pkl")
    
    # Créer le répertoire 'models' s'il n'existe pas
    os.makedirs(os.path.dirname(model_filename), exist_ok=True)
    
    try:
        # Enregistrer le modèle avec joblib
        joblib.dump(model, model_filename)
        st.write(f"Le modèle a été enregistré avec succès dans le fichier : `{model_filename}`")
    except Exception as e:
        st.error(f"Erreur lors de l'enregistrement du modèle : {e}")

# Fonction principale de la page de modélisation
def page_modelisation(data):
    st.title("Page de Modélisation des Performances Étudiantes")

    try:
        # Division des données en ensembles d'entraînement et de test
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

        # Liste des modèles disponibles
        models = {
            "Régression Ridge": Ridge(),
            "Régression Lasso": Lasso(),
            "Régression ElasticNet": ElasticNet(),
            "Random Forest Regressor": RandomForestRegressor(),
            "Gradient Boosting Regressor": GradientBoostingRegressor(),
            "K-Nearest Neighbors (KNN)": KNeighborsRegressor(),
            "Support Vector Regressor (SVR)": SVR(),
            "Decision Tree Regressor": DecisionTreeRegressor()
        }

        # Choix des modèles à inclure
        st.sidebar.header("Choisissez les modèles à inclure")
        selected_models = {model_name: st.sidebar.checkbox(model_name, value=True) for model_name in models.keys()}

        # Dictionnaire pour stocker les résultats
        results = {}

        # Entraînement et évaluation
        for model_name, model in models.items():
            if selected_models[model_name]:
                model.fit(X_train, y_train)
                y_train_pred = model.predict(X_train)  # Prédictions pour l'ensemble d'entraînement
                y_test_pred = model.predict(X_test)    # Prédictions pour l'ensemble de test

                # Validation croisée pour le R²
                cv_r2 = cross_val_score(model, X_train, y_train, cv=5, scoring="r2").mean()

                # Calcul des métriques
                mae = mean_absolute_error(y_test, y_test_pred)
                mse_train = mean_squared_error(y_train, y_train_pred)  # MSE pour l'entraînement
                mse_test = mean_squared_error(y_test, y_test_pred)     # MSE pour le test
                rmse = mse_test ** 0.5
                r2 = r2_score(y_test, y_test_pred)

                # Stockage des résultats
                results[model_name] = {
                    "MAE": mae,
                    "MSE Entraînement": mse_train,  # MSE pour l'entraînement
                    "MSE Test": mse_test,            # MSE pour le test
                    "RMSE": rmse,
                    "Validation R² (CV)": cv_r2,     # R² de la validation croisée
                    "Test R²": r2
                }

        # Affichage des résultats sous forme de tableau
        st.subheader("Comparaison des Modèles")
        results_df = pd.DataFrame(results).T.sort_values(by="Test R²", ascending=False)
        st.dataframe(results_df)

        # Sélection du meilleur modèle basé sur le Test R²
        best_model_name = results_df.index[0]
        st.write(f"**Modèle avec le meilleur R² sur le test**: {best_model_name}")
        best_model = models[best_model_name]

        # Entraînement du meilleur modèle
        best_model.fit(X_train, y_train)
        y_best_pred = best_model.predict(X_test)

        # Enregistrement du meilleur modèle
        save_model(best_model, best_model_name)

        # Enregistrement des prédictions du meilleur modèle dans un fichier local
        predictions_dict = {
            "Valeurs Réelles": y_test.tolist(),
            "Prédictions": y_best_pred.tolist()
        }

        file_path = os.path.join("predictions", f"{best_model_name}_predictions.json")

        # Créer le répertoire 'predictions' s'il n'existe pas
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Sauvegarder les prédictions dans un fichier JSON
        with open(file_path, "w") as f:
            json.dump(predictions_dict, f, indent=4)

        st.write(f"Les prédictions ont été enregistrées dans le fichier : `{file_path}`")

        # Proposer le téléchargement du fichier JSON
        st.download_button(
            label="Télécharger les prédictions du meilleur modèle en JSON",
            data=open(file_path, "r").read(),  # Lire le contenu du fichier pour le téléchargement
            file_name=f"{best_model_name}_predictions.json",
            mime="application/json"
        )

        # Optionnel: Vous pouvez également permettre à l'utilisateur de télécharger le modèle
        st.download_button(
            label="Télécharger le modèle entraîné",
            data=open(os.path.join("models", f"{best_model_name}_model.pkl"), "rb").read(),  # Lire le modèle binaire pour le téléchargement
            file_name=f"{best_model_name}_model.pkl",
            mime="application/octet-stream"
        )

        # Sélection d'un modèle pour l'analyse détaillée
        st.subheader("Analyse d'un modèle spécifique")
        selected_model_name = st.selectbox("Choisissez un modèle pour l'analyse", list(results.keys()))
        selected_model = models[selected_model_name]
        selected_model.fit(X_train, y_train)
        y_pred = selected_model.predict(X_test)

        # Visualisation des prédictions vs valeurs réelles
        st.write(f"**→ Prédictions vs Valeurs Réelles : {selected_model_name}**")
        fig, ax = plt.subplots(figsize=(10, 6))  # Explicitement créer la figure et les axes
        ax.scatter(y_test, y_pred, color="blue", alpha=0.6)
        ax.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color="red", linestyle="--")
        ax.set_xlabel("Valeurs Réelles")
        ax.set_ylabel("Prédictions")
        st.pyplot(fig)  # Passer explicitement la figure

    except Exception as e:
        st.error(f"Erreur : {e}")
