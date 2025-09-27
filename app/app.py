from flask import Flask, request, render_template
import joblib
import pandas as pd
import numpy as np

# Initialize the Flask app
app = Flask(__name__)

try:
    model_pipeline = joblib.load('churn_model_pipeline.joblib')
except FileNotFoundError:
    model_pipeline = None
    print("ERROR: Model file 'churn_model_pipeline.joblib' not found.")
    print("Please ensure the 'Customer_Analytics.ipynb' notebook has been run successfully.")

MODEL_COLUMNS = [
    'credit_score', 'geography', 'gender', 'age', 'tenure', 'balance',
    'num_of_products', 'has_cr_card', 'is_active_member', 'estimated_salary'
]


@app.route('/')
def home():
    """Renders the home page with the input form."""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handles the prediction request from the form."""
    if model_pipeline is None:
        return render_template('index.html', prediction_text='Error: Model not loaded. Please check server logs.')

    try:
        form_data = request.form.to_dict()
        
        input_df = pd.DataFrame([form_data])
        
        input_df['credit_score'] = pd.to_numeric(input_df['credit_score'])
        input_df['age'] = pd.to_numeric(input_df['age'])
        input_df['tenure'] = pd.to_numeric(input_df['tenure'])
        input_df['balance'] = pd.to_numeric(input_df['balance'])
        input_df['num_of_products'] = pd.to_numeric(input_df['num_of_products'])
        input_df['has_cr_card'] = pd.to_numeric(input_df['has_cr_card'])
        input_df['is_active_member'] = pd.to_numeric(input_df['is_active_member'])
        input_df['estimated_salary'] = pd.to_numeric(input_df['estimated_salary'])
        input_df = input_df[MODEL_COLUMNS]
        probability = float(model_pipeline.predict_proba(input_df)[0][1])
        prediction = 1 if probability > 0.55 else 0
        result = "Likely to Churn" if prediction == 1 else "Unlikely to Churn"
        confidence = f"Churn Probability: {probability*100:.2f}%"
        
        return render_template('index.html', 
                               prediction_text=f'Prediction: {result}',
                               confidence_text=confidence)

    except Exception as e:
        return render_template('index.html', prediction_text=f'An error occurred: {e}')

if __name__ == "__main__":
    app.run(debug=True)