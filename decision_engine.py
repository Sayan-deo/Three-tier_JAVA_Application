import os
import json
from datetime import datetime

# -----------------------------
# CONFIGURATION
# -----------------------------
RISK_THRESHOLD = 0.30   # 30% deviation allowed
HISTORY_FILE = "metrics/history.json"

# -----------------------------
# READ BUILD TIME
# -----------------------------
build_time = int(os.getenv("BUILD_TIME", "0"))

if build_time == 0:
    print("false")
    exit(0)

# -----------------------------
# CREATE METRICS DIRECTORY
# -----------------------------
if not os.path.exists("metrics"):
    os.makedirs("metrics")

# -----------------------------
# LOAD HISTORY
# -----------------------------
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r") as f:
        history = json.load(f)
else:
    history = []

# -----------------------------
# CALCULATE HISTORICAL AVERAGE
# -----------------------------
if history:
    avg_build_time = sum(run["build_time"] for run in history) / len(history)
else:
    avg_build_time = build_time  # First run baseline

# -----------------------------
# CALCULATE RISK SCORE
# -----------------------------
risk_score = abs(build_time - avg_build_time) / (avg_build_time + 1)

# -----------------------------
# DECISION LOGIC
# -----------------------------
if risk_score <= RISK_THRESHOLD:
    deploy = "true"
else:
    deploy = "false"

# -----------------------------
# SAVE CURRENT RUN
# -----------------------------
history.append({
    "timestamp": str(datetime.now()),
    "build_time": build_time,
    "risk_score": risk_score,
    "decision": deploy
})

with open(HISTORY_FILE, "w") as f:
    json.dump(history, f, indent=2)

# -----------------------------
# PRINT FOR GITHUB ACTIONS
# -----------------------------
print(deploy)
