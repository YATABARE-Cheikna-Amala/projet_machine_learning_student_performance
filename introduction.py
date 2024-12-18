import streamlit as st

def page_introduction(data=None):  # Ajoute un argument par défaut
    # Titre principal
    st.title("🎓 Analyse et Prédiction des Performances Académiques")
    
    # Bannière ou sous-titre
    st.markdown(
        """
        <h4 style="text-align: center; color: #4CAF50;">
        Exploiter le Machine Learning pour mieux comprendre et prédire la réussite éducative
        </h4>
        """, unsafe_allow_html=True
    )

    # **Contexte et Justification**
    st.subheader("📚 Contexte et Justification")
    st.write("""
    La réussite éducative est un enjeu central des sociétés modernes. Dans un monde en constante évolution, il devient crucial de comprendre 
    les facteurs influençant la performance académique des étudiants.  
    """)
    st.info("""
    *"L’éducation n’est pas l’apprentissage des faits, mais la formation de l’esprit à penser."*  
    — Albert Einstein
    """)

    st.write("""
    Aujourd’hui, les outils de **Machine Learning** offrent des opportunités inédites pour analyser les données éducatives.  
    Ils permettent :
    - **D'identifier les variables** ayant un impact majeur sur la réussite académique.  
    - **D'accompagner les étudiants** en difficulté de manière proactive.  
    - **D'améliorer les stratégies pédagogiques** pour un enseignement plus efficace.  
    """)
    
    st.divider()

    # **Objectifs**
    st.subheader("🎯 Objectif Général")
    st.write("""
    Développer un modèle de régression capable de **prédire la performance académique** des étudiants en exploitant des données contextuelles 
    et sociodémographiques.
    """)

    st.subheader("🔍 Objectifs Spécifiques")
    st.markdown("""
    - Identifier les variables ayant une **influence significative** sur la performance académique.  
    - Construire un **modèle prédictif robuste** avec des techniques de Machine Learning.  
    - Évaluer la **pertinence** et la **précision** des prédictions à l’aide de métriques fiables.  
    - Déployer ce modèle sur une **plateforme** accessible aux acteurs du secteur éducatif.
    """)

    st.divider()

    # **Plan du Projet**
    st.subheader("🗺️ Plan du Projet")
    plan_steps = [
        "Analyse des données sources et description des variables retenues.",
        "Exploration des statistiques descriptives avec des visualisations claires.",
        "Prétraitement des données pour assurer leur qualité.",
        "Construction et entraînement du modèle de régression.",
        "Évaluation des performances et interprétation des résultats.",
        "Déploiement du modèle sur une plateforme interactive."
    ]

    # Affichage du plan sous forme de liste stylisée
    for i, step in enumerate(plan_steps):
        st.markdown(f"**{i+1}.** {step}")

    st.divider()

    # **Conclusion de l'Introduction**
    st.subheader("🚀 Vision et Ambition")
    st.write("""
    En suivant cette démarche structurée, ce projet ambitionne d'apporter des outils concrets pour améliorer la compréhension des performances 
    académiques et soutenir les acteurs éducatifs dans la prise de décisions stratégiques.
    """)

    st.success("Prêt à explorer les données et construire un modèle prédictif ? 🚀")

    # Petit rappel visuel pour naviguer dans l'application
    st.markdown(
        """
        <h5 style="text-align: center; color: #4CAF50;">
        Utilisez le menu de navigation pour accéder aux différentes étapes de l'analyse.
        </h5>
        """, unsafe_allow_html=True
    )
