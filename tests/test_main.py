import os
import pandas as pd
import numpy as np
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
            
def test_generate_client_data_values():
    data = generate_client_data(10)
    assert data["revenu_mensuel"].between(2000, 10000).all()
    assert data["age"].between(18, 70).all()
    assert data["historique_defaut"].isin([0, 1]).all()
    assert data["montant_demande"].between(1000, 50000).all()
    assert data["octroi"].isin([0, 1]).all()
            
def test_save_data(tmp_path):
    
    data = generate_client_data(20)
    file_path = tmp_path/"clients.csv"
    save_data(data, path=file_path)
    assert os.path.exists(file_path)
 
@pytest.fixture(scope="module")           
def trained_model():
    
    data = generate_client_data(200)
    model_octroi, scaler = train_model(data)
    client = pd.DataFrame([{
        
        "revenu_mensuel":5000,
        "age":30,
        "historique_defaut":0,
        "montant_demande":10000
    }])
    return model_octroi, scaler, client

def test_train_model_ouput(trained_model):
    
    model_octroi, scaler, _ = trained_model
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import StandardScaler
    
    assert isinstance(model_octroi, RandomForestClassifier)
    assert isinstance(scaler, StandardScaler)
    
def test_prediction_client(trained_model):
    
    model_octroi, scaler, client = trained_model
    decision, proba = prediction_client(model_octroi, scaler, client)
    assert decision in [0, 1]
    assert 0.0 <= proba <= 1.0
    
def test_stress_test_structure(trained_model):
    
    model_octroi, scaler, client_input = trained_model
    revenu = client_input["revenu_mensuel"].iloc[0]
    montant = client_input["montant_demande"].iloc[0]
    
    factors, results = stress_test(model_octroi, scaler, client_input.copy(), revenu, montant)
    assert isinstance(factors, list)
    assert isinstance(results, list)
    assert len(factors) == len(results)
    assert all(isinstance(f, str) for f in factors)
    assert all(isinstance(r, (float, int, np.floating)) for r in results)
    
def test_stress_test_probability_range(trained_model):
    
    model_octroi, scaler, client_input = trained_model
    revenu = client_input["revenu_mensuel"].iloc[0]
    montant = client_input["montant_demande"].iloc[0]
    
    _, results = stress_test(model_octroi, scaler, client_input.copy(), revenu, montant)
    assert all(0.0 <= r <= 1.0 for r in results)
    
def test_stress_test_effect(trained_model):
    
    model_octroi, scaler, client_input = trained_model
    revenu = client_input["revenu_mensuel"].iloc[0]
    montant = client_input["montant_demande"].iloc[0]
    
    baseline_proba = prediction_client(model_octroi, scaler, client_input)[1]
    _, results = stress_test(model_octroi, scaler, client_input.copy(), revenu, montant)
    assert any(abs(r - baseline_proba) > 1e-6 for r in results)
    
    