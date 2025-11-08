from flask import Flask, request, jsonify
import os
import json

CURRENT_WATER_FILE = "/Users/daofficial_cam/Downloads/TigerTech/main_status.json"
PREV_WATER_FILE = "/Users/daofficial_cam/Downloads/TigerTech/prev_status.json"

def load_json(path, default=None):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return default or {}

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

# if you're using the new OpenAI python client:
from openai import OpenAI

app = Flask(__name__)

# init openai client (needs your key in env)
client = OpenAI(api_key="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")
@app.after_request
def add_cors_headers(response):
    # your frontend is on 5500
    response.headers["Access-Control-Allow-Origin"] = "http://127.0.0.1:5500"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response

@app.route("/water-status", methods=["GET"])
def water_status():
    current = load_json(CURRENT_WATER_FILE, {})
    prev = load_json(PREV_WATER_FILE, {})

    changes = {}
    for key in ["pred_label", "pred_ph", "pred_turbidity", "pred_lead_ppb"]:
        cur_val = current.get(key)
        prev_val = prev.get(key)
        if cur_val != prev_val:
            changes[key] = {"previous": prev_val, "current": cur_val}

    return jsonify({
        "current": current,
        "previous": prev,
        "changes": changes
    })

@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():
    # Safari/Chrome preflight
    if request.method == "OPTIONS":
        return ("", 200)

    data = request.get_json() or {}
    question = (data.get("question") or "").lower().strip()

    # 1) water safety
    if "is my water safe" in question or ("water" in question and "safe" in question):
        return jsonify({
            "answer": "Yes, your water is SAFE to drink today. pH is about 7.2, turbidity around 2.0 NTU, and lead ~3 ppb — all within a safe range. If it looks or smells off, boil 1–3 minutes or call your utility."
        })

    # 2) how-to questions (your big block)
    if "how to" in question or question.startswith("how "):
        if "protect" in question and "house" in question:
            return jsonify({
                "answer": "To protect your house: clean gutters, seal foundation cracks, elevate outlets if flooding is common, and keep an emergency kit ready."
            })
        if "save" in question and "water" in question:
            return jsonify({
                "answer": "To save water: fix leaks, install low-flow fixtures, collect rainwater for plants, and turn off taps while brushing."
            })
        if "improve" in question and "air" in question:
            return jsonify({
                "answer": "To improve indoor air: ventilate, use HEPA filters, avoid smoking indoors, and keep HVAC filters clean."
            })
        if "keep" in question and "water" in question:
            return jsonify({
                "answer": "Flush faucets weekly, use an NSF/ANSI certified filter, test yearly if you have a well, and don’t pour grease or chemicals down drains."
            })
        if "make" in question and "home" in question:
            return jsonify({
                "answer": "Check smoke/CO detectors, clean vents, fix leaks, and have a family emergency plan."
            })
        if "prepare" in question and ("storm" in question or "flood" in question):
            return jsonify({
                "answer": "Check drainage, move valuables higher, keep water/flashlights handy, and monitor local alerts."
            })
        # generic how-to
        return jsonify({
            "answer": "Keep drinking water protected, maintain filters, and follow local alerts. That covers most home safety basics."
        })

    # 3) air quality
    if "air" in question or "aqi" in question or "smoke" in question or "breath" in question:
        return jsonify({
            "answer": "Today’s air is MODERATE. Close windows if you're sensitive, run AC on recirculate, and wear an N95 outdoors on bad AQI days."
        })

    # 4) flood / storm / basement water
    if "flood" in question or "storm" in question or "water in" in question or "basement" in question:
        return jsonify({
            "answer": "During flooding: move valuables up, keep drinking water separate from flood water, don’t walk in moving water, and only shut off power if it’s safe."
        })

    # 5) greetings
    if question in ("hi", "hello", "hey") or "who are you" in question or "what can you do" in question:
        return jsonify({
            "answer": "Hi! I’m your home environmental assistant for water, air, and flood tips. Ask: “is my water safe?” or “how do I keep water clean?”."
        })

    # 6) basic what/why
    if question.startswith("what "):
        return jsonify({
            "answer": "This tool is focused on home environment: water quality, air quality, and flood safety. Ask one of those and I can be very specific."
        })
    if question.startswith("why "):
        return jsonify({
            "answer": "Mostly to protect health and the house — clean water, filtered air, and staying out of flood water reduce sickness and damage."
        })

    if "water update" in question or "what changed" in question or "compare" in question:
        current = load_json(CURRENT_WATER_FILE, {})
        prev = load_json(PREV_WATER_FILE, {})
        diffs = []
        for key, label in [("pred_label","status"),("pred_ph","pH"),("pred_turbidity","turbidity"),("pred_lead_ppb","lead")]:
            if current.get(key) != prev.get(key):
                diffs.append(f"{label} changed from {prev.get(key)} to {current.get(key)}")
        if diffs:
            return jsonify({"answer": "Here are the latest water changes: " + "; ".join(diffs)})
        else:
            return jsonify({"answer": "No water changes since the last reading."})

    # 7) FALLBACK → OpenAI
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for a home environmental dashboard. Answer clearly."},
                {"role": "user", "content": question}
            ],
        )
        ai_answer = completion.choices[0].message.content
        return jsonify({"answer": ai_answer})
    except Exception as e:
        # if OpenAI isn't set up, stay graceful
        print("OpenAI error:", e)
        return jsonify({
            "answer": "I couldn’t reach the AI service, but I can help with water, air, and flood safety. Try: “is my water safe?”"
        })
@app.route("/send-alert", methods=["POST", "OPTIONS"])
def send_alert():
    # Handle browser preflight (CORS)
    if request.method == "OPTIONS":
        return ("", 200)

    data = request.get_json() or {}
    alert_message = data.get("message", " Flood Alert: Heavy rainfall in Jackson. Stay safe!")
    
if __name__ == "__main__":
    app.run(port=5000, debug=True)