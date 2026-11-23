
import pandas as pd
import numpy as np


def load_data(file_path):
    """
    Load the credit card fraud dataset.
    """
    df = pd.read_csv(file_path)

    print("Dataset loaded successfully!")
    print("Original dataset shape:", df.shape)

    return df


def remove_duplicates(df):
    """
    Remove exact duplicate records.
    Returns a cleaned copy of the dataset.
    """
    df_clean = df.drop_duplicates().copy()

    print("Duplicate removal completed!")
    print("Original rows:", len(df))
    print("Cleaned rows:", len(df_clean))
    print("Remaining duplicates:", df_clean.duplicated().sum())

    return df_clean


def separate_features_target(df):
    """
    Separate input features (X) and target variable (y).
    """
    X = df.drop(columns=["Class"]).copy()
    y = df["Class"].copy()

    print("Features shape:", X.shape)
    print("Target shape:", y.shape)

    return X, y


def engineer_features(X):
    """
    Add the log-transformed transaction amount feature.
    """
    X_engineered = X.copy()
    X_engineered["Amount_log"] = np.log1p(X_engineered["Amount"])

    print("Feature engineering completed!")
    print("Engineered features shape:", X_engineered.shape)

    return X_engineered
