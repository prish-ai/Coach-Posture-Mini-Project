from flask import Flask, jsonify, send_file
from flask_cors import CORS
import csv
import os
import json

app = Flask(__name__)
CORS(app)  # allows frontend to talk to Python

# ── Route 1: serve the frontend ──────────────────────
@app.route('/')
def index():
    return send_file('frontend/coach_posture_frontend.html')

# ── Route 2: live posture status ─────────────────────
@app.route('/api/posture')
def posture():
    try:
        with open('posture_flag.txt', 'r') as f:
            status = f.read().strip()
    except:
        status = 'good'

    try:
        with open('posture_data.json', 'r') as f:
            data = json.load(f)
    except:
        data = {'angle': 0, 'status': status, 'good_pct': 0, 'bad_pct': 0, 'streak': 0}

    return jsonify(data)

# ── Route 3: session analytics from CSV ──────────────
@app.route('/api/sessions')
def sessions():
    csv_file = 'logs/posture_sessions.csv'
    rows = []
    if os.path.exists(csv_file):
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
    return jsonify(rows[-20:])  # last 20 sessions

# ── Route 4: weekly summary ───────────────────────────
@app.route('/api/weekly')
def weekly():
    csv_file = 'logs/posture_sessions.csv'
    if not os.path.exists(csv_file):
        return jsonify([])

    from datetime import datetime, timedelta
    today = datetime.now().date()
    week = {str(today - timedelta(days=i)): {'good':0,'bad':0,'count':0} for i in range(6,-1,-1)}

    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                date = row['date'][:10]
                if date in week:
                    week[date]['good']  += float(row['good_posture_pct'])
                    week[date]['bad']   += float(row['bad_posture_pct'])
                    week[date]['count'] += 1
            except:
                pass

    result = []
    for date, vals in week.items():
        if vals['count'] > 0:
            result.append({'date':date,'good':round(vals['good']/vals['count'],1),'bad':round(vals['bad']/vals['count'],1)})
        else:
            result.append({'date':date,'good':0,'bad':0})
    return jsonify(result)

if __name__ == '__main__':
    print("Starting Flask server...")
    try:
        app.run(debug=False, port=5000, use_reloader=False)
    except Exception as e:
        print("ERROR:", e)
        input("Press Enter to exit")