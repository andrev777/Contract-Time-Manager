import datetime
from typing import List, Dict
from src.models import Worker, TimeEntry, Leave, Loan, Payslip
from src.calculations import calculate_monthly_pay, accrue_annual_leave, calculate_daily_hours
from src.data_manager import DataManager

class ContractTimeManagerApp:
    def __init__(self):
        self.data_manager = DataManager()
        self.workers: List[Worker] = []
        self.time_entries: List[TimeEntry] = []
        self.leaves: List[Leave] = []
        self.loans: List[Loan] = []
        self._load_all_data()

    def _load_all_data(self):
        self.workers, self.time_entries, self.leaves, self.loans = self.data_manager.load_data()
        # Ensure worker objects have their associated lists properly linked after load
        worker_map = {w.worker_id: w for w in self.workers}
        for entry in self.time_entries:
            if entry.worker_id in worker_map:
                worker_map[entry.worker_id].time_entries.append(entry)
        for leave_item in self.leaves:
            if leave_item.worker_id in worker_map:
                worker_map[leave_item.worker_id].leave_days.append(leave_item)
        for loan_item in self.loans:
            if loan_item.worker_id in worker_map:
                worker_map[loan_item.worker_id].loans.append(loan_item)


    def _save_all_data(self):
        self.data_manager.save_data(self.workers, self.time_entries, self.leaves, self.loans)

    def _get_worker(self, worker_id: str) -> Worker | None:
        return next((w for w in self.workers if w.worker_id == worker_id), None)

    def add_worker(self, worker_id: str, name: str, hourly_rate: float = 28.79):
        if any(w.worker_id == worker_id for w in self.workers):
            print(f"Worker with ID {worker_id} already exists.")
            return
        worker = Worker(worker_id, name, hourly_rate)
        self.workers.append(worker)
        self._save_all_data()
        print(f"Worker {name} ({worker_id}) added.")

    def record_time_entry(self, worker_id: str, date_str: str, start_time_str: str, end_time_str: str):
        worker = self._get_worker(worker_id)
        if not worker:
            print(f"Worker with ID {worker_id} not found.")
            return

        try:
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            start_time = datetime.datetime.strptime(start_time_str, "%H:%M").time()
            end_time = datetime.datetime.strptime(end_time_str, "%H:%M").time()
        except ValueError:
            print("Invalid date or time format. Use YYYY-MM-DD for date and HH:MM for time.")
            return
        
        if calculate_daily_hours(start_time, end_time) < 0:
            print("End time cannot be before start time.")
            return

        entry = TimeEntry(worker_id, date, start_time, end_time)
        self.time_entries.append(entry)
        worker.time_entries.append(entry)  # Link to worker for easy access
        
        # Accrue annual leave directly when time is recorded
        accrue_annual_leave(worker, 1) # Assume 1 day worked for simplicity for accrual

        self._save_all_data()
        print(f"Time entry recorded for {worker.name} on {date} from {start_time} to {end_time}.")


    def record_leave(self, worker_id: str, leave_type: str, start_date_str: str, end_date_str: str, days_taken: float):
        worker = self._get_worker(worker_id)
        if not worker:
            print(f"Worker with ID {worker_id} not found.")
            return

        try:
            start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")
            return

        leave = Leave(worker_id, leave_type, start_date, end_date, days_taken)
        self.leaves.append(leave)
        worker.leave_days.append(leave) # Link to worker
        self._save_all_data()
        print(f"{leave_type} leave recorded for {worker.name} from {start_date} to {end_date} for {days_taken} days.")

    def record_loan(self, worker_id: str, loan_amount: float, start_date_str: str, repayment_schedule_str: str):
        worker = self._get_worker(worker_id)
        if not worker:
            print(f"Worker with ID {worker_id} not found.")
            return
        
        try:
            start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
            repayment_schedule = []
            # Expecting repayment_schedule_str like "YYYY-MM-DD:AMOUNT,YYYY-MM-DD:AMOUNT"
            for item in repayment_schedule_str.split(","):
                date_str, amount_str = item.strip().split(":")
                repayment_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                repayment_amount = float(amount_str)
                repayment_schedule.append((repayment_date, repayment_amount))
        except ValueError:
            print("Invalid date, amount, or repayment schedule format. Use YYYY-MM-DD for date, X.XX for amount, and comma-separated pairs (e.g., \'2023-01-31:100.00,2023-02-28:100.00\').")
            return

        loan = Loan(worker_id, loan_amount, start_date, repayment_schedule)
        self.loans.append(loan)
        worker.loans.append(loan) # Link to worker
        self._save_all_data()
        print(f"Loan of R{loan_amount:.2f} recorded for {worker.name} starting {start_date}.")

    def generate_payslip(self, worker_id: str, month_str: str):
        worker = self._get_worker(worker_id)
        if not worker:
            print(f"Worker with ID {worker_id} not found.")
            return

        try:
            month = datetime.datetime.strptime(month_str, "%Y-%m").date()
        except ValueError:
            print("Invalid month format. Use YYYY-MM.")
            return

        payslip = calculate_monthly_pay(worker, month, self.time_entries)
        print(payslip.generate_payslip_content())
        # For email/WhatsApp, you would integrate with respective APIs here
        print("Payslip generated. (Email/WhatsApp sharing not implemented in this version)")

    def list_workers(self):
        if not self.workers:
            print("No workers registered.")
            return
        print("--- Registered Workers ---")
        for worker in self.workers:
            print(f"ID: {worker.worker_id}, Name: {worker.name}, Hourly Rate: R{worker.hourly_rate:.2f}, Annual Leave Accrued: {worker.accrued_annual_leave_days:.2f} days")
        print("--------------------------")

    def run(self):
        while True:
            print("\n--- Contract Time Manager ---")
            print("1. Add Worker")
            print("2. Record Time Entry")
            print("3. Record Leave")
            print("4. Record Loan")
            print("5. Generate Payslip")
            print("6. List Workers")
            print("7. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                worker_id = input("Enter worker ID: ")
                name = input("Enter worker name: ")
                rate = input("Enter hourly rate (default 28.79): ")
                hourly_rate = float(rate) if rate else 28.79
                self.add_worker(worker_id, name, hourly_rate)
            elif choice == "2":
                worker_id = input("Enter worker ID: ")
                date_str = input("Enter date (YYYY-MM-DD): ")
                start_time_str = input("Enter start time (HH:MM): ")
                end_time_str = input("Enter end time (HH:MM): ")
                self.record_time_entry(worker_id, date_str, start_time_str, end_time_str)
                # The leave accrual is now handled directly within record_time_entry
            elif choice == "3":
                worker_id = input("Enter worker ID: ")
                leave_type = input("Enter leave type (annual, sick, family): ")
                start_date_str = input("Enter start date (YYYY-MM-DD): ")
                end_date_str = input("Enter end date (YYYY-MM-DD): ")
                days_taken = float(input("Enter number of days taken: "))
                self.record_leave(worker_id, leave_type, start_date_str, end_date_str, days_taken)
            elif choice == "4":
                worker_id = input("Enter worker ID: ")
                loan_amount = float(input("Enter loan amount: "))
                start_date_str = input("Enter loan start date (YYYY-MM-DD): ")
                repayment_schedule_str = input("Enter repayment schedule (e.g., \'YYYY-MM-DD:AMOUNT,YYYY-MM-DD:AMOUNT\'): ")
                self.record_loan(worker_id, loan_amount, start_date_str, repayment_schedule_str)
            elif choice == "5":
                worker_id = input("Enter worker ID: ")
                month_str = input("Enter month for payslip (YYYY-MM): ")
                self.generate_payslip(worker_id, month_str)
            elif choice == "6":
                self.list_workers()
            elif choice == "7":
                print("Exiting application.")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    app = ContractTimeManagerApp()
    app.run()
