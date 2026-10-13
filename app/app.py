from datetime import datetime
import os
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

# Demo-only in-memory data. It resets when the app restarts.
doctors = [
    {"name": "Dr. Asha Mehta", "department": "Cardiology"},
    {"name": "Dr. Rahul Shah", "department": "Pediatrics"},
    {"name": "Dr. Neha Patil", "department": "General Medicine"},
]
appointments = [
    {"patient": "Demo Patient", "doctor": "Dr. Asha Mehta",
     "date": "2026-11-05", "department": "Cardiology"}
]

@app.get("/")
def index():
    return render_template(
        "index.html",
        appointments=appointments,
        doctors=doctors,
        departments=sorted({d["department"] for d in doctors}),
        today=datetime.today().date().isoformat(),
        message=request.args.get("message", ""),
    )

@app.post("/book")
def book():
    patient = request.form.get("patient", "").strip()
    doctor_name = request.form.get("doctor", "").strip()
    department = request.form.get("department", "").strip()
    date_value = request.form.get("date", "").strip()
    doctor = next((d for d in doctors if d["name"] == doctor_name
                   and d["department"] == department), None)
    try:
        date_obj = datetime.strptime(date_value, "%Y-%m-%d").date()
    except ValueError:
        date_obj = None

    if not patient or not doctor or not date_obj or date_obj < datetime.today().date():
        return redirect(url_for("index", message="Please enter valid demo appointment details."))

    appointments.append({
        "patient": patient[:60],
        "doctor": doctor["name"],
        "date": date_obj.isoformat(),
        "department": doctor["department"],
    })
    return redirect(url_for("index", message="Demo appointment added successfully."))

@app.get("/health")
def health():
    return {"status": "healthy"}, 200

if __name__ == "__main__":
    # Local learning server only; use a production WSGI server for deployment.
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "5000")), debug=False)
