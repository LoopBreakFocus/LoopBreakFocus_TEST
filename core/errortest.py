import pandas as pd

features_df = pd.read_csv("/Users/VyomeshJoshi/Downloads/eeg_all_features.csv")
labels_df = pd.read_csv("/Users/VyomeshJoshi/Desktop/NeuroSage/labels.csv")

print("\n🧠 Feature CSV Columns:")
print(features_df.columns)

print("\n🏷️ Labels CSV Columns:")
print(labels_df.columns)

print("\n🧪 Sample rows from labels.csv:")
print(labels_df.head())