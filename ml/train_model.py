import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

# Project paths
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(
    BASE_PATH,
    "dataset",
    "MachineLearningCSV",
    "MachineLearningCVE"
)

MODEL_PATH = os.path.join(BASE_PATH, "models")
FEATURE_PATH = os.path.join(MODEL_PATH, "feature_names.pkl")

os.makedirs(MODEL_PATH, exist_ok=True)


# Dataset files
files = [
    "Monday-WorkingHours.pcap_ISCX.csv",
    "Tuesday-WorkingHours.pcap_ISCX.csv",
    "Wednesday-workingHours.pcap_ISCX.csv",
    "Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv",
    "Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv",
    "Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv",
    "Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv",
    "Friday-WorkingHours-Morning.pcap_ISCX.csv"
]


# Load a sample from each file
dataframes = []

for file in files:
    file_path = os.path.join(DATA_PATH, file)

    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()

    sample_size = min(20000, len(df))
    df = df.sample(sample_size, random_state=42)

    dataframes.append(df)


# Combine datasets
df = pd.concat(dataframes, ignore_index=True)

print("Dataset shape:", df.shape)


# Convert labels to binary
df["Target"] = df["Label"].apply(
    lambda x: 0 if str(x).strip() == "BENIGN" else 1
)

# Remove original label
df = df.drop(columns=["Label"])


# Clean infinite and missing values
df = df.replace([float("inf"), float("-inf")], pd.NA)
df = df.dropna()


# Separate features and target
X = df.drop(columns=["Target"])
y = df["Target"]


# Convert numeric columns stored as text
for col in ["Flow Bytes/s", "Flow Packets/s"]:
    X[col] = pd.to_numeric(X[col], errors="coerce")


# Remove rows created as NaN after conversion
valid_rows = X.notna().all(axis=1)
X = X.loc[valid_rows]
y = y.loc[valid_rows]


# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# Train Random Forest
print("Training Random Forest...")

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

print("Training completed!")


# Predictions
y_pred = model.predict(X_test)


# Evaluation
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print("\nModel Performance")
print("------------------")
print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1 Score : {f1:.4f}")


print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))


print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        target_names=["BENIGN", "ATTACK"]
    )
)


# Save model
joblib.dump(
    model,
    os.path.join(MODEL_PATH, "random_forest_model.pkl")
)

# Save feature names
joblib.dump(
    list(X.columns),
    FEATURE_PATH
)

print("\nModel saved successfully!")
print("Location:", MODEL_PATH)