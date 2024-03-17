import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split

import comparison.constants as c

if __name__ == "__main__":
    csv_file_path = c.DATA_DIR / "dummy_fraud_data.csv"
    # Load the data
    df = pd.read_csv(csv_file_path)

    # Prepare the data
    X = df.drop('is_fraud', axis=1)
    # Convert 'transaction_time' to a numerical feature, e.g., hour of the day
    X['transaction_time'] = pd.to_datetime(X['transaction_time']).dt.hour
    y = df['is_fraud']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create a LightGBM dataset
    train_data = lgb.Dataset(X_train, label=y_train)
    test_data = lgb.Dataset(X_test, label=y_test, reference=train_data)

    # Define the model parameters
    params = {
        'objective': 'binary',
        'metric': 'binary_logloss',
        'learning_rate': 0.1,
        'num_leaves': 31,
        'verbose': -1,
    }

    # Train the model
    gbm = lgb.train(params, train_data, valid_sets=[test_data], num_boost_round=100)

    # Save the trained model
    model_path = c.DATA_DIR / 'trained_lgbm_model.txt'
    gbm.save_model(model_path)
