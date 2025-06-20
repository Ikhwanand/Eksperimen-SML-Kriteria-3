import mlflow
import pandas as pd 
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import os 
import numpy as np 
import warnings 
import sys 



if __name__=='__main__':
    warnings.filterwarnings("ignore")
    np.random.seed(40)
    
    # Read the csv file
    file_path = sys.argv[3] if len(sys.argv) > 3 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "preprocessing_dataset", "train_preprocessing.csv")
    data = pd.read_csv(file_path)
    data.dropna(inplace=True)
    
    # The predicted column is "Churn"
    X_train, X_test, y_train, y_test = train_test_split(
        data.drop("Churn", axis=1),
        data["Churn"],
        random_state=42,
        test_size=0.2
    )
    input_example = X_train[0:5]
    params = {'C': 0.0010019670981854481, 'solver': 'liblinear', 'penalty': 'l2', 'max_iter': 379}
    with mlflow.start_run():
        model = LogisticRegression(**params)
        model.fit(X_train, y_train)
        
        predicted_qualities = model.predict(X_test)
        
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="model",
            input_example=input_example
        )
        model.fit(X_train, y_train)
        # Log metrics
        accuracy = model.score(X_test, y_test)
        mlflow.log_metric("accuracy", accuracy)
    
    
