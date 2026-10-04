# AI Cyber Threat Detection

An AI-based network intrusion detection system that uses Machine Learning to identify network traffic as **BENIGN** or **ATTACK**.

## Project Overview

This project analyzes network traffic data and uses a Machine Learning model to detect potentially malicious network activity.

The system is built using the **CIC-IDS-2017 dataset** and a **Random Forest Classifier**.

The project also provides:

- FastAPI backend for prediction
- Streamlit dashboard for user interaction
- Attack probability for every prediction
- CSV-based network traffic analysis
- Attack-wise model evaluation

## Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Random Forest
- FastAPI
- Streamlit
- Matplotlib
- Seaborn

## Dataset

The project uses the **CIC-IDS-2017** network intrusion detection dataset.

The dataset contains normal network traffic and multiple types of attacks, including:

- DoS
- DDoS
- FTP-Patator
- SSH-Patator
- Web Attacks
- Bot
- Infiltration
- PortScan

## Machine Learning Model

The project uses a **Random Forest Classifier**.

The model uses **78 network traffic features** to classify each network flow.

The output is:

- `BENIGN`
- `ATTACK`

The system also provides an attack probability between 0 and 1.

## Model Performance

Overall test performance:

| Metric | Score |
|---|---:|
| Accuracy | 99.76% |
| Precision | 99.48% |
| Recall | 99.27% |
| F1 Score | 99.38% |

### Attack-wise Detection

| Attack Type | Detection Rate |
|---|---:|
| DoS | 99.03% |
| DDoS | 99.91% |
| FTP-Patator | 99.50% |
| SSH-Patator | 98.39% |
| Web Attacks | 96.33% |
| Bot | 66.84% |
| Infiltration | 25.00% |

Benign traffic detection rate was **99.96%** in the additional evaluation.

> Note: Bot and Infiltration have lower detection rates. In particular, the CIC-IDS-2017 dataset contains only 36 Infiltration samples, so this result should be interpreted cautiously.

## Project Architecture

```text
Network Traffic CSV
        |
        v
Data Preprocessing
        |
        v
Feature Selection
        |
        v
Random Forest Model
        |
        +----------------+
        |                |
        v                v
   FastAPI API     Streamlit Dashboard
        |                |
        +-------+--------+
                |
                v
       BENIGN / ATTACK
       Attack Probability