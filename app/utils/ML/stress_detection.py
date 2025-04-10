import joblib
import numpy as np
import json
import pickle
import os


model_directory = r'/home/davidnene/dawaChat/app/utils/ML/models'

# Use os.path.join to create file paths
xgb_classifier_path = os.path.join(model_directory, 'xgb_classifier_model.pkl')
scaler_path = os.path.join(model_directory, 'scaler.pkl')
le_time_path = os.path.join(model_directory, 'label_encoder_time.pkl')
le_day_path = os.path.join(model_directory, 'label_encoder_day.pkl')

# Load the models and encoders
xgb_classifier = pickle.load(open(xgb_classifier_path, 'rb'))
MinMaxScaler = pickle.load(open(scaler_path, 'rb'))
le_time = pickle.load(open(le_time_path, 'rb'))
le_day = pickle.load(open(le_day_path, 'rb'))

def predict_avg_probability(records_df):
    records_df['time_of_day'] = le_time.transform(records_df['time_of_day'])
    records_df['day_of_week'] = le_day.transform(records_df['day_of_week'])

    records_scaled = MinMaxScaler.transform(records_df)
    proba = xgb_classifier.predict_proba(records_scaled)

    avg_probs = np.mean(proba, axis=0)
    predicted_class = np.argmax(avg_probs)

    return {
        "predicted_class": int(predicted_class),
        "avg_probabilities": avg_probs.tolist()
    }
