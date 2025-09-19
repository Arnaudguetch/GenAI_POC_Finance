import os
import pandas as pd
import pytest
from source.main import generate_client_data, save_data, train_model, prediction_client, stress_test

def test_generate_client_data_shape():
    
    data = generate_client_data(50)
    assert data.shape == (50, 5)
    expected_columns = ["revenu_mensuel", "age", "historique_defaut", "montant_demande", "octroi"]
    for col in expected_columns:
        assert col in data.columns
    
def test_generate_client_data_logic():
    
    data = generate_client_data(10)
    for _, row in data.iterrows():
        if row["revenu_mensuel"] > 4000 and row ["historique_defaut"] == 0:
            assert row["octroi"] == 1
        else:
            assert row["octroi"] == 0
            
def test_save_data(tmp_path):
    
    data = generate_client_data(20)
    file_path = tmp_path/"clients.csv"
    save_data(data, path=file_path)
    assert os.path.exists(file_path)
            
def test_train_and_predict():
    
    data = generate_client_data(100)
    model_octroi, scaler = train_model(data)
    client = pd.DataFrame({
        
        "revenu_mensuel":[5000],
        "age":[30],
        "historique_defaut":[0],
        "montant_demande":[10000]
    })
    
    decision, proba = prediction_client(model_octroi, scaler, client)
    assert decision in [0, 1]
    assert 0 <= proba <= 1
    
def test_stress_test_effect():
    
    data = generate_client_data(100)
    model_octroi, scaler = train_model(data)
    client = pd.DataFrame({
        
       "revenu_mensuel":[5000],
        "age":[30],
        "historique_defaut":[0],
        "montant_demande":[10000]
    })
    
    factors, results = stress_test(model_octroi, scaler, client, revenu=5000, montant_demande=1000)
    assert len(factors) == len(results) == 3
    assert all(0 <= p <= 1 for p in results)
    
    