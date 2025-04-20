import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

class BankingProductRecommender:
    def __init__(self, training_data_path: str = "CustomerData.csv"):
        self.model = None
        self.output_columns = [
            "needs_savings_account",
            "needs_cd_account",
            "needs_checking_account",
            "needs_money_market_account"
        ]

        # Store encoders to reuse them at prediction
        self.emp_encoder = LabelEncoder().fit(["Employed", "Unemployed", "Self-employed", "Retired"])
        self.risk_encoder = LabelEncoder().fit(["Low", "Medium", "High"])

        self.train_model(training_data_path)

    def train_model(self, file_path: str):
        df = pd.read_csv(file_path)

        for col in self.output_columns:
            if col not in df.columns:
                raise ValueError(f"CSV must contain a target column named '{col}'")

        df['employment_status'] = self.emp_encoder.transform(df['employment_status'])
        df['risk_tolerance'] = self.risk_encoder.transform(df['risk_tolerance'])

        X = df[['age', 'income', 'credit_score', 'employment_status',
                'risk_tolerance', 'monthly_expense', 'has_credit_card',
                'investment_balance']].copy()

        X['has_credit_card'] = X['has_credit_card'].astype(int)
        y = df[self.output_columns]

        X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)

        base_model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model = MultiOutputClassifier(base_model)
        self.model.fit(X_train, y_train)

    def recommend_all(self, input_data: dict) -> dict:
        df = pd.DataFrame([input_data])
        df['has_credit_card'] = df['has_credit_card'].astype(int)

        # Encode using trained encoders
        df['employment_status'] = self.emp_encoder.transform([df.loc[0, 'employment_status']])[0]
        df['risk_tolerance'] = self.risk_encoder.transform([df.loc[0, 'risk_tolerance']])[0]

        input_features = df[['age', 'income', 'credit_score', 'employment_status',
                             'risk_tolerance', 'monthly_expense', 'has_credit_card',
                             'investment_balance']]

        predictions = self.model.predict(input_features)[0]
        return dict(zip(self.output_columns, predictions))
