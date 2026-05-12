import pandas as pd
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from xgboost import XGBRegressor

def train_model():
    data_path = 'ml_pipeline/data/house_prices.csv'
    if not os.path.exists(data_path):
        print(f"Error: Place your CSV in {data_path}")
        return

    # Load Data
    df = pd.read_csv(data_path)
    
    # 1. Define Features (Dropping Property_ID as it has no predictive power)
    # Features: Area, Bedrooms, Bathrooms, Age, Location, Property_Type
    X = df[['Area', 'Bedrooms', 'Bathrooms', 'Age', 'Location', 'Property_Type']]
    y = df['Price']
    
    # 2. Preprocessing Logic
    num_cols = ['Area', 'Bedrooms', 'Bathrooms', 'Age']
    cat_cols = ['Location', 'Property_Type']
    
    preprocessor = ColumnTransformer([
        ('num', StandardScaler(), num_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore'), cat_cols)
    ])
    
    # 3. Create Pipeline with XGBoost
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', XGBRegressor(n_estimators=150, learning_rate=0.08, max_depth=5))
    ])
    
    # 4. Train
    pipeline.fit(X, y)
    
    # 5. Export
    os.makedirs('backend/models', exist_ok=True)
    with open('backend/models/house_model.pkl', 'wb') as f:
        pickle.dump(pipeline, f)
        
    print("✅ Success: Model updated with new columns and saved.")

if __name__ == "__main__":
    train_model()
