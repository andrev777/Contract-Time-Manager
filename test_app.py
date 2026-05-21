import datetime
from src.app import ContractTimeManagerApp
import os

def run_tests():
    # Clean up previous data for a fresh test run
    data_dir = "data"
    if os.path.exists(data_dir):
        for file_name in os.listdir(data_dir):
            os.remove(os.path.join(data_dir, file_name))
        os.rmdir(data_dir)

    app = ContractTimeManagerApp()

    print("\n--- Test: Add Worker ---")
    app.add_worker("W001", "Alice Smith", 35.00)
    app.list_workers()

    print("\n--- Test: Record Time Entries ---")
    # Normal hours
    app.record_time_entry("W001", "2026-04-01", "08:00", "17:00") # 9 hours
    app.record_time_entry("W001", "2026-04-02", "08:00", "17:00") # 9 hours
    app.record_time_entry("W001", "2026-04-03", "08:00", "17:00") # 9 hours
    app.record_time_entry("W001", "2026-04-04", "08:00", "17:00") # 9 hours
    app.record_time_entry("W001", "2026-04-05", "08:00", "17:00") # 9 hours
    # Overtime hours (10 hours daily)
    app.record_time_entry("W001", "2026-04-08", "08:00", "18:00") # 10 hours (1 overtime)
    app.record_time_entry("W001", "2026-04-09", "08:00", "18:00") # 10 hours (1 overtime)
    # Another worker to ensure data separation
    app.add_worker("W002", "Bob Johnson", 30.00)
    app.record_time_entry("W002", "2026-04-01", "09:00", "17:00") # 8 hours

    print("\n--- Test: Record Leave ---")
    app.record_leave("W001", "annual", "2026-04-06", "2026-04-06", 1.0)
    app.record_leave("W001", "sick", "2026-04-07", "2026-04-07", 1.0)

    print("\n--- Test: Record Loan ---")
    repayment_schedule = "2026-05-31:100.00,2026-06-30:100.00"
    app.record_loan("W001", 200.00, "2026-04-15", repayment_schedule)

    print("\n--- Test: Generate Payslip for W001 (April 2026) ---")
    app.generate_payslip("W001", "2026-04")

    print("\n--- Test: Generate Payslip for W002 (April 2026) ---")
    app.generate_payslip("W002", "2026-04")

    print("\n--- Test: Accrued Annual Leave for W001 after time entries ---")
    worker_w001 = app._get_worker("W001")
    if worker_w001:
        print(f"Worker W001 Accrued Annual Leave: {worker_w001.accrued_annual_leave_days:.2f} days")

    # Test loan deduction in May payslip
    print("\n--- Test: Generate Payslip for W001 (May 2026) with loan deduction ---")
    app.record_time_entry("W001", "2026-05-01", "08:00", "17:00") # Some hours in May
    app.generate_payslip("W001", "2026-05")

    print("\n--- All tests completed ---")

if __name__ == "__main__":
    run_tests()
