import time
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn import accuracy_score
from sklearn.model_selection import train_test_split
import os


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

def save_data(data, path="/data/clients.csv"):
    
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data.to_csv(path, index=False)
    
    return path

def train_model(data):
    
    X = data[["revenu_mensuel", "age", "historique_defaut", "montant_demande"]]
    Y = data["octroi"]
    
    X_train, X_test, y_train, y_test = train_test_split(X,Y, test_size=0.2, random_state=42)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    model_octroi = RandomForestClassifier(n_estimators=100, random_state=42)
    model_octroi.fit(X_train_scaled,y_train)
    
    y_pred = model_octroi.predict(X_test_scaled)
    acc = accuracy_score(y_test, y_pred)
    
    return model_octroi, scaler, acc

def prediction_client(model_octroi, scaler, client_input):
    
    client_scaled = scaler.transform(client_input)
    decision = model_octroi.predict(client_scaled)[0]
    proba = model_octroi.predict_proba(client_scaled)[0][1]
    
    return decision, proba

def stress_test(model_octroi, scaler, client_input, revenu, montant_demande):
    
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
        
    return stress_factors, stress_results
        

