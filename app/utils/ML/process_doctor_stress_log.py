from models import EmpaticaIotData, StressLog
from datetime import datetime
import pandas as pd
from utils.ML.stress_detection import predict_avg_probability
import pytz

def process_doctor_stress_log(doctor_id: int, doctor_name: str, db):
    
    # Fetch latest 5 IoT records for the doctor
    recent_records = db.query(EmpaticaIotData).filter_by(doctor_id=doctor_id).order_by(EmpaticaIotData.timestamp.desc()).limit(5).all()

    if not recent_records or len(recent_records) < 1:
        return None  # No data to process

    # Convert records to DataFrame
    records_df = pd.DataFrame([{
        "X": r.x,
        "Y": r.y,
        "Z": r.z,
        "EDA": r.eda,
        "HR": r.heart_rate,
        "TEMP": r.temperature,
        "time_of_day": r.time_of_day,
        "day_of_week": r.day_of_week
    } for r in recent_records])

    # pass to the predictor function
    result = predict_avg_probability(records_df)

    tz = pytz.timezone("Africa/Nairobi")
    if result["predicted_class"] == 1 or result["predicted_class"] == 2:
        log = StressLog(
            doctor_id=doctor_id,
            doctor_name=doctor_name,
            stress_level="mild" if result["predicted_class"] == 1 else "severe",
            timestamp=datetime.now(tz)
        )
        db.add(log)
        db.commit()
        print("Stress Detection Successful!")
        print(result["predicted_class"])
    return result
