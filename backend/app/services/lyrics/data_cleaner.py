import pandas as pd

DATASET_PATH = "datasets/lyrics/songs.csv"


def load_dataset():
    df = pd.read_csv(DATASET_PATH)
    return df


def show_columns(df):
    print(df.columns)