import random

import numpy as np
import pandas as pd

import comparison.constants as c


def generate_dummy_data(num_records: int) -> pd.DataFrame:
    """Generate dummy data for training."""
    data = {
        "transaction_amount": np.random.uniform(10, 1000, num_records),
        "transaction_time": [
            random.randint(0, 23) for _ in range(num_records)
        ],  # Hour of the day
        "new_device": np.random.choice([True, False], num_records),
        "previous_purchases": np.random.randint(0, 100, num_records),
        "user_logged_in": np.random.choice([True, False], num_records),
        "num_items_in_basket": np.random.randint(1, 10, num_records),
        "min_basket_item_price": np.random.uniform(1, 100, num_records),
        "max_basket_item_price": np.random.uniform(100, 1000, num_records),
    }

    # Ensure min price is not more than max price
    for i in range(num_records):
        if data["min_basket_item_price"][i] > data["max_basket_item_price"][i]:
            data["min_basket_item_price"][i], data["max_basket_item_price"][i] = (
                data["max_basket_item_price"][i],
                data["min_basket_item_price"][i],
            )

    # Add a binary target variable for fraud (1) or not fraud (0)
    data["is_fraud"] = np.random.choice([0, 1], num_records)

    return pd.DataFrame(data)

if __name__ == "__main__":
    # Generate dummy data
    num_records = 1000  # Adjust the number of records as needed
    df = generate_dummy_data(num_records)

    # Save to CSV
    csv_file_name = "dummy_fraud_data.csv"
    c.DATA_DIR.mkdir(exist_ok=True)
    df.to_csv(c.DATA_DIR / csv_file_name, index=False)
