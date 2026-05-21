from flask import Flask, request, jsonify
from flask_cors import CORS
from app import ContractTimeManagerApp
import datetime

app = Flask(__name__)
CORS(app) # Enable CORS for all routes
contract_app = ContractTimeManagerApp()

@app.route("/", methods=["GET"])
def home():
    return "Contract Time Manager API"

@app.route("/workers", methods=["POST"])
def add_worker():
    data = request.json
    worker_id = data.get("worker_id")
    name = data.get("name")
    hourly_rate = data.get("hourly_rate", 28.79)

    if not worker_id or not name:
        return jsonify({"error": "Worker ID and name are required."}), 400

    # Capture print output temporarily
    import io
    import sys
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()

    contract_app.add_worker(worker_id, name, hourly_rate)
    output = redirected_output.getvalue().strip()
    sys.stdout = old_stdout # Restore stdout

    if "already exists" in output:
        return jsonify({"message": output}), 409
    return jsonify({"message": output}), 201

@app.route("/workers", methods=["GET"])
def list_workers():
    # Capture print output temporarily
    import io
    import sys
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()

    contract_app.list_workers()
    output = redirected_output.getvalue().strip()
    sys.stdout = old_stdout # Restore stdout

    # Parse the output to return structured data if possible, otherwise return raw output
    workers_list = []
    if output and "--- Registered Workers ---" in output:
        lines = output.split("\n")
        for line in lines:
            if line.startswith("ID:"):
                parts = line.split(", ")
                worker_data = {}
                for part in parts:
                    if ": " in part:
                        key, value = part.split(": ", 1)
                        worker_data[key.lower().replace(" ", "_")] = value.replace("R", "").replace("days", "").strip()
                workers_list.append(worker_data)
        return jsonify(workers_list), 200
    elif "No workers registered." in output:
        return jsonify({"message": "No workers registered."}), 200
    return jsonify({"message": output}), 500


@app.route("/time_entries", methods=["POST"])
def record_time_entry():
    data = request.json
    worker_id = data.get("worker_id")
    date_str = data.get("date")
    start_time_str = data.get("start_time")
    end_time_str = data.get("end_time")

    if not all([worker_id, date_str, start_time_str, end_time_str]):
        return jsonify({"error": "All fields (worker_id, date, start_time, end_time) are required."}), 400
    
    import io, sys
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()

    contract_app.record_time_entry(worker_id, date_str, start_time_str, end_time_str)
    output = redirected_output.getvalue().strip()
    sys.stdout = old_stdout

    if "not found" in output or "Invalid" in output:
        return jsonify({"message": output}), 404
    return jsonify({"message": output}), 201

@app.route("/leaves", methods=["POST"])
def record_leave():
    data = request.json
    worker_id = data.get("worker_id")
    leave_type = data.get("leave_type")
    start_date_str = data.get("start_date")
    end_date_str = data.get("end_date")
    days_taken = data.get("days_taken")

    if not all([worker_id, leave_type, start_date_str, end_date_str, days_taken is not None]):
        return jsonify({"error": "All fields (worker_id, leave_type, start_date, end_date, days_taken) are required."}), 400
    
    import io, sys
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()

    contract_app.record_leave(worker_id, leave_type, start_date_str, end_date_str, float(days_taken))
    output = redirected_output.getvalue().strip()
    sys.stdout = old_stdout

    if "not found" in output or "Invalid" in output:
        return jsonify({"message": output}), 404
    return jsonify({"message": output}), 201

@app.route("/loans", methods=["POST"])
def record_loan():
    data = request.json
    worker_id = data.get("worker_id")
    loan_amount = data.get("loan_amount")
    start_date_str = data.get("start_date")
    repayment_schedule_str = data.get("repayment_schedule")

    if not all([worker_id, loan_amount is not None, start_date_str, repayment_schedule_str]):
        return jsonify({"error": "All fields (worker_id, loan_amount, start_date, repayment_schedule) are required."}), 400
    
    import io, sys
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()

    contract_app.record_loan(worker_id, float(loan_amount), start_date_str, repayment_schedule_str)
    output = redirected_output.getvalue().strip()
    sys.stdout = old_stdout

    if "not found" in output or "Invalid" in output:
        return jsonify({"message": output}), 404
    return jsonify({"message": output}), 201

@app.route("/payslips", methods=["POST"])
def generate_payslip():
    data = request.json
    worker_id = data.get("worker_id")
    month_str = data.get("month")

    if not all([worker_id, month_str]):
        return jsonify({"error": "Worker ID and month are required."}), 400

    import io, sys
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()

    contract_app.generate_payslip(worker_id, month_str)
    output = redirected_output.getvalue().strip()
    sys.stdout = old_stdout

    if "not found" in output or "Invalid" in output:
        return jsonify({"message": output}), 404
    
    # The payslip content is part of the output, so we return it directly
    return jsonify({"message": output}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000) # Running on port 5000
