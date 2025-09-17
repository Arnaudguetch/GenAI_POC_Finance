import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
from openai import OpenAI

from main import generate_client_data, save_data, train_model, prediction_client, stress_test
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

data = generate_client_data()
save_data(data)
model_octroi, scaler = train_model(data)

st.title("POC : Moteur d'octroi et Fragilité bancaire")

st.header("Informations Client")

revenu = st.number_input("Revenu mensuel (Euro)", min_value=1000, max_value=20000, value=5000)
age = st.number_input("Age", min_value=18, max_value=100, value=35)
historique_defaut = st.selectbox("Historique de défaut (0 = Non, 1 = Oui)", [0, 1])
montant_demande = st.number_input("Montant démandé (Euro)", min_value=500, max_value=100000, value=10000)

client_input = pd.DataFrame({
    
   "revenu_mensuel": [revenu],
   "age": [age],
   "historique_defaut": [historique_defaut],
   "montant_demande": [montant_demande]
})

decision, proba = prediction_client(model_octroi, scaler, client_input)

st.subheader("Décision d'octroi")
if decision == 1:
    st.success(f"Crédit accordé (Probabilité de succès {proba:.2f})")
else:
    st.error(f"Crédit refusé (Probabilité d'éechec {proba:.2f})")

st.header("Scénarios de Stress")
stress_factors, stress_results = stress_test(model_octroi, scaler, client_input, revenu, montant_demande)
    
fig, ax = plt.subplots()
ax.bar(stress_factors, stress_results, color=["green", "orange", "red"])
ax.set_ylim(0, 1)
ax.set_ylabel("Probabilité d'octroi")
ax.set_title("Impact des Scénarios de Stress")
st.pyplot(fig)

st.header("Analyse Fragilité Bancaire")
prompt = f"""
Analyse la fragilité pour un client ayant : 
- Revenu mensuel : {revenu} Euro
- Age : {age} ans
- Historique de défaut : {historique_defaut}
- Montant demandé : {montant_demande} Euro

Fournis un score de fragilité (faible, modéré, élevé), explique les facteurs 
principaux et commente l'impact des scénarios des stress suivants :
1- Baisse de revenu
2- Hausse du montant
3- Historique de défaut
"""  

if st.button("Géneré analyse"):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
       
        st.markdown(response.choices[0].message.content)
    except Exception as e:
        st.error(f"Erreur OpenAI : {e}")

