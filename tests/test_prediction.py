import requests
import pandas as pd


# CIC-IDS2017 file
file_path = r"C:\Users\KIIT0001\Desktop\ai-cyber-threat-detection\dataset\MachineLearningCSV\MachineLearningCVE\Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv"


# Read one row
df = pd.read_csv(file_path)
df.columns = df.columns.str.strip()

row = df.iloc[0]

# Remove label
features = row.drop("Label")

# Convert the two columns that may be stored as text
for col in ["Flow Bytes/s", "Flow Packets/s"]:
    features[col] = pd.to_numeric(features[col], errors="coerce")

# Replace invalid values
features = features.replace([float("inf"), float("-inf")], 0)
features = features.fillna(0)

# Send features to FastAPI
response = requests.post(
    "http://127.0.0.1:8000/predict",
    json={"features": features.tolist()}
)

print("Status code:", response.status_code)
print("Response:")
print(response.json())