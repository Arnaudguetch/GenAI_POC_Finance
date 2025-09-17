## Ce **POC** a pour objectif de lancer une architecture Générative AI capable d'analyser ou travailler sur un **moteurs d'octroi** et **fragilité bancaire.** Cependant ayant une approche **conceptuel/démonstractif** et **technique avec codes et données factices**.

## **1 - Moteurs d'octroi :**

## **Objectif :** Simuler ou analyser l'octroi e crédit ou de produits financiers via des modéles intelligents. 

## **Idée du POC GenAI:**
    - **Entrées :** données clients (profils, historique de paiement, revenu, etc...)
    - **GenAI :** propose un scoring de risque ou des recommendations pour l'octroi 
    - **Sorties :** décision "Accordé/Réfusé/Besoin d'info complémentaire" + explication synthétique par l'IA 
    - **Techniques possibles :**
        - Classification supervisée avec un modéle e scoring
        - Génération de recommandations textuelles explicatives pour les décideurs. 


## **2 - Fragilité bancaire :**

## **Objectifs :** détecter la vulnérabilité financière ou le risque systémique de banques ou de portefeuilles. 

## **Idée POC GenAI :** 
    - **Entrées :** indicateurs financiers (ratio de liquidité, capital, créances douteuses…)
    - **GenAI :** génère un rapport de fragilité, alertes et scénarios de stress test
    - **Sorties :**
        - Score de fragilité (faible/modéré/élevé)
        - Résumé explicatif avec les facteurs de risques principaux
    - **Techniques possibles :**
        - Analyse prédictive via ML pour le risque de défaut
        - Génération de rapports automatisé en langue naturel
  
## 3 - Proposition de POC combiné : Pratique
    > Le but est de faire est de faire un **mini tableau de board intéractif** ou :
        - L'utilisateur renseigne des informations clients et bancaires.
        - GenAI propose :
            1. Décision d'octroi et justification
            2. Analyse de fragilité bancaire avec recommandations
        - **Technologies :** Python + Streamlit + modéles GPT pour la génération de texte et ML pour le scoring.


    |- GenAI_POC_Finance/
    |                   - main.py
    |                   - Dockerfile
    |                   - Docker-compose
    |                   - GithubActions
    |                   - Jenkins
    |                   - TestUnitaires
    |                   - Mlflow
    |                   - Requirements