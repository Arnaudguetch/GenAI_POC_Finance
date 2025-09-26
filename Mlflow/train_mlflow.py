
from source.main import generate_client_data, save_data, train_model, prediction_client, stress_test
import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn


if __name__ == "__main__":

    mlflow.set_experiment("Credit_Octroi_Model")

    with mlflow.start_run(run_name="RandomForest_Octroi"):
        
        data = generate_client_data(500)
        data_path = save_data(data)
        mlflow.log_param("n_samples", len(data))
    
        model, scaler, accuracy = train_model(data)
        mlflow.log_param("model_type", "RandomForestClassifier")
        mlflow.log_metric("accuracy", accuracy)

        client_input = pd.DataFrame([{
            "revenu_mensuel": 5000,
            "age": 35,
            "historique_defaut": 0,
            "montant_demande": 10000
        }])
        decision, proba = prediction_client(model, scaler, client_input)
        mlflow.log_metric("prediction_proba", proba)

        stress_factors, stress_results = stress_test(
            model, scaler, client_input.copy(),
            revenu=client_input["revenu_mensuel"].iloc[0],
            montant_demande=client_input["montant_demande"].iloc[0]
        )

        for factor, proba_stress in zip(stress_factors, stress_results):
            mlflow.log_metric(f"stress_{factor}_proba", proba_stress)

        mlflow.sklearn.log_model(model, "model_octroi")
        mlflow.sklearn.log_model(scaler, "scaler")

        mlflow.log_artifact(data_path)

        print("Entraînement terminé !")
        print(f"Accuracy : {accuracy:.2f}")
        print(f"Probabilité octroi : {proba:.2f}")
        print("Stress test :", dict(zip(stress_factors, stress_results)))
        
        