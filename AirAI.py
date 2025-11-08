import os
import pandas as pd
from datetime import datetime, timedelta
import json

# Path to your air quality text file
REF_PATH = "/Users/daofficial_cam/Downloads/TigerTech/AirQuality/AirData"

def load_reference():
    """Read AirQualityData.txt and return a cleaned DataFrame"""
    if not os.path.exists(REF_PATH):
        print(f"[x] Reference file '{REF_PATH}' not found")
        return None

    with open(REF_PATH, "r") as f:
        lines = f.read().strip().splitlines()

    if not lines:
        print("[x] Reference file is empty")
        return None

    rows = []
    for line in lines:
        lower = line.lower()
        if "datetime" in lower or "aqi" in lower or "quality" in lower:
            continue

        parts = line.split(",")
        if len(parts) < 5:
            continue
        try:
            rows.append({
                "datetime": parts[0].strip(),
                "pm25": float(parts[1]),
                "pm10": float(parts[2]),
                "aqi": float(parts[3]),
                "quality": parts[4].strip()
            })
        except ValueError:
            print(f"[!] Skipping bad line: {line}")
            continue

    if not rows:
        print("[x] No valid rows found")
        return None

    df = pd.DataFrame(rows)
    print(f"[+] Loaded {len(df)} air quality records")
    return df


def simple_predict_next_day(df):
    """Make a simple forecast by assuming next day ≈ latest reading"""
    last = df.iloc[-1]

    next_day = datetime.fromisoformat(last["datetime"].split(" ")[0]) + timedelta(days=1)
    pred = {
        "date": next_day.date().isoformat(),
        "pm25": last["pm25"],
        "pm10": last["pm10"],
        "aqi": last["aqi"]
    }

    # Simple air quality rule
    if pred["aqi"] <= 50:
        pred["label"] = "Good"
    elif pred["aqi"] <= 100:
        pred["label"] = "Moderate"
    elif pred["aqi"] <= 150:
        pred["label"] = "Unhealthy (Sensitive)"
    elif pred["aqi"] <= 200:
        pred["label"] = "Unhealthy"
    else:
        pred["label"] = "Very Unhealthy"

    return pred


def save_status(pred):
    """Save next-day prediction to a status.json file"""
    status = {
        "next_date": pred["date"],
        "pred_pm25": pred["pm25"],
        "pred_pm10": pred["pm10"],
        "pred_aqi": pred["aqi"],
        "pred_label": pred["label"],
        "updated_at": datetime.now().isoformat()
    }

    with open("/Users/daofficial_cam/Downloads/TigerTech/Air_status.json", "w") as f:
        json.dump(status, f, indent=4)
    print("[+] Air_status.json updated with next-day prediction")


if __name__ == "__main__":
    df = load_reference()
    if df is not None:
        pred = simple_predict_next_day(df)
        print("[+] Next-day prediction:", pred)
        save_status(pred)
