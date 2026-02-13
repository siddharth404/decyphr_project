
import pandas as pd
import numpy as np
import random

def generate_telco_data(num_rows=1000, seed=42):
    """
    Generates a synthetic Telco Customer Churn dataset with realistic correlations.
    """
    np.random.seed(seed)
    random.seed(seed)
    
    data = []
    
    for i in range(num_rows):
        customer_id = f"{random.randint(1000,9999)}-{random.choice(['Alpha', 'Beta', 'Gamma'])}-{i}"
        gender = random.choice(['Male', 'Female'])
        senior_citizen = random.choice([0, 1])
        partner = random.choice(['Yes', 'No'])
        dependents = random.choice(['Yes', 'No'])
        
        # Tenure: skewed distribution
        tenure = int(np.random.beta(2, 2) * 72) + 1
        
        phone_service = random.choice(['Yes', 'No'])
        multiple_lines = 'No phone service' if phone_service == 'No' else random.choice(['Yes', 'No'])
        
        internet_service = np.random.choice(['DSL', 'Fiber optic', 'No'], p=[0.3, 0.5, 0.2])
        
        online_security = 'No internet service' if internet_service == 'No' else random.choice(['Yes', 'No'])
        online_backup = 'No internet service' if internet_service == 'No' else random.choice(['Yes', 'No'])
        device_protection = 'No internet service' if internet_service == 'No' else random.choice(['Yes', 'No'])
        tech_support = 'No internet service' if internet_service == 'No' else random.choice(['Yes', 'No'])
        streaming_tv = 'No internet service' if internet_service == 'No' else random.choice(['Yes', 'No'])
        streaming_movies = 'No internet service' if internet_service == 'No' else random.choice(['Yes', 'No'])
        
        contract = np.random.choice(['Month-to-month', 'One year', 'Two year'], p=[0.5, 0.3, 0.2])
        paperless_billing = random.choice(['Yes', 'No'])
        payment_method = random.choice(['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'])
        
        # Monthly Charges based on services
        base_charge = 18.25
        if phone_service == 'Yes': base_charge += 20
        if multiple_lines == 'Yes': base_charge += 9
        if internet_service == 'Fiber optic': base_charge += 40
        elif internet_service == 'DSL': base_charge += 20
        
        if online_security == 'Yes': base_charge += 5
        if online_backup == 'Yes': base_charge += 5
        if device_protection == 'Yes': base_charge += 5
        if tech_support == 'Yes': base_charge += 5
        if streaming_tv == 'Yes': base_charge += 10
        if streaming_movies == 'Yes': base_charge += 10
        
        monthly_charges = round(base_charge + np.random.normal(0, 2), 2)
        total_charges = round(monthly_charges * tenure, 2)
        
        # Churn Logic (Encoded Risks)
        churn_prob = 0.1
        if contract == 'Month-to-month': churn_prob += 0.4
        if internet_service == 'Fiber optic': churn_prob += 0.15
        if tech_support == 'No': churn_prob += 0.1
        if payment_method == 'Electronic check': churn_prob += 0.1
        if tenure < 12: churn_prob += 0.1
        if tenure > 60: churn_prob -= 0.3
        
        churn_prob = max(0, min(1, churn_prob))
        churn = np.random.choice(['Yes', 'No'], p=[churn_prob, 1-churn_prob])
        
        data.append([
            customer_id, gender, senior_citizen, partner, dependents, tenure,
            phone_service, multiple_lines, internet_service, online_security,
            online_backup, device_protection, tech_support, streaming_tv,
            streaming_movies, contract, paperless_billing, payment_method,
            monthly_charges, total_charges, churn
        ])
        
    columns = [
        'customerID', 'gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure',
        'PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity',
        'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV',
        'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod',
        'MonthlyCharges', 'TotalCharges', 'Churn'
    ]
    
    df = pd.DataFrame(data, columns=columns)
    output_file = 'telco_customer_churn.csv'
    df.to_csv(output_file, index=False)
    print(f"✅ Generated {len(df)} rows of Telco Churn data to '{output_file}'")

if __name__ == "__main__":
    generate_telco_data()
