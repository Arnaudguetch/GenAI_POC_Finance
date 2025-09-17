import time
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import openai

# openia.api_key = ...

def generate_client_data(n=100):
    
    np.random.seed(42)
    data = pd.DataFrame({
        
        "revenu_mensuel": np.random.randint(2000, 10000, n),
        "age": np.random.randint(18, 70, n),
        "historique_defaut": np.random.randint(0, 2, n),
        "montant_demande": np.random.randint(1000, 50000, n)
    })
    
    data["octroi"] = (data["revenu_mensuel"] > 4000) &(data["historique_defaut"] == 0)
    data["octroi"] = data["octroi"].astype(int)
    
    return data 

data = generate_client_data()

data.to_csv("./data/clients.csv", index=False)
print("Données sauvegardées dans data/clients.csv")

X = data[["revenu_mensuel", "age", "historique_defaut", "montant_demande"]]
Y = data["octroi"]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model_octroi = RandomForestClassifier(n_estimators=100, random_state=42)
model_octroi.fit(X_scaled, Y)

st.title("POC : Moteur d'octroi et Fragilité bancaire")

st.header("Informations Client")

revenu = st.number_input("Revenu mensuel (Euro)", min_value=1000, max_value=2000, value=5000)
age = st.number_input("Age", min_value=18, max_value=100, value=35)
historique_defaut = st.selectbox("Historique de défaut (0 = Non, 1 = Oui)", [0, 1])
montant_demande = st.number_input("Montant démandé (Euro)", min_value=500, max_value=100000, value=10000)

client_input = pd.DataFrame({
    
   "revenu_mensuel": [revenu],
   "age": [age],
   "historique_defaut": [historique_defaut],
   "montant_demande": [montant_demande]
})

client_scaled = scaler.transform(client_input)
decision = model_octroi.predict(client_scaled)[0]
proba = model_octroi.predict_proba(client_scaled)[0][1]

st.subheader("Décision d'octroi")
if decision == 1:
    st.success(f"Crédit accordé (Probabilité de succès {proba:.2f})")
else:
    st.error(f"Crédit refusé (Probabilité d'éechec {proba:.2f})")

st.header("Scénarios de Stress")

stress_factors = ["baisse_revenu", "hausse_montant", "historique_defaut"]
stress_results = []

for factor in stress_factors:
    stressed_client = client_input.copy()
    if factor == "baisse_revenu":
        stressed_client["revenu_mensuel"] = max(500, revenu*0.7)
    elif factor == "hausse_montant":
        stressed_client["montant_demande"] = montant_demande*1.5
    elif factor == "historique_defaut":
        stressed_client["historique_defaut"] = 1
        
    stressed_scaled = scaler.transform(stressed_client)
    stressed_proba = model_octroi.predict_proba(stressed_scaled)[0][1]
    stress_results.append(stressed_proba)
    
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
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature = 0.7
    )
    
    st.markdown(response.choices[0].message.content)

    