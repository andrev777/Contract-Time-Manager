import datetime
from typing import List, Optional

class Worker:
    def __init__(self, worker_id: str, name: str, hourly_rate: float = 28.79):
        self.worker_id = worker_id
        self.name = name
        self.hourly_rate = hourly_rate
        self.time_entries: List[TimeEntry] = []
        self.leave_days: List[Leave] = []
        self.loans: List[Loan] = []
        self.accrued_annual_leave_days = 0.0

class TimeEntry:
    def __init__(self, worker_id: str, date: datetime.date, start_time: datetime.time, end_time: datetime.time):
        self.worker_id = worker_id
        self.date = date
        self.start_time = start_time
        self.end_time = end_time

class Leave:
    def __init__(self, worker_id: str, leave_type: str, start_date: datetime.date, end_date: datetime.date, days_taken: float):
        self.worker_id = worker_id
        self.leave_type = leave_type  # e.g., 'annual', 'sick', 'family'
        self.start_date = start_date
        self.end_date = end_date
        self.days_taken = days_taken

class Loan:
    def __init__(self, worker_id: str, loan_amount: float, start_date: datetime.date, repayment_schedule: List[tuple[datetime.date, float]]):
        self.worker_id = worker_id
        self.loan_amount = loan_amount
        self.start_date = start_date
        self.repayment_schedule = repayment_schedule # list of (date, amount) tuples
        self.repaid_amount = 0.0

class Payslip:
    def __init__(self, worker_id: str, month: datetime.date, total_hours: float, gross_pay: float, uif_deduction: float, loan_deduction: float, net_pay: float, total_overtime_hours: float = 0.0):
        self.worker_id = worker_id
        self.month = month
        self.total_hours = total_hours
        self.total_overtime_hours = total_overtime_hours
        self.gross_pay = gross_pay
        self.uif_deduction = uif_deduction
        self.loan_deduction = loan_deduction
        self.net_pay = net_pay
        self.deductions: List[tuple[str, float]] = [("UIF", uif_deduction), ("Loan", loan_deduction)] # For general deductions

    def add_deduction(self, name: str, amount: float):
        self.deductions.append((name, amount))
        self.net_pay -= amount

    def generate_payslip_content(self) -> str:
        content = f"""
        --- PAYSLIP ---
        Worker ID: {self.worker_id}
        Month: {self.month.strftime('%Y-%m')}
        Total Hours Worked: {self.total_hours:.2f} (including {self.total_overtime_hours:.2f} overtime hours)
        Gross Pay: R{self.gross_pay:.2f}
        UIF Deduction: R{self.uif_deduction:.2f}
        Loan Deduction: R{self.loan_deduction:.2f}
        -----------------
        Net Pay: R{self.net_pay:.2f}
        -----------------
        """
        for name, amount in self.deductions:
            if name != "UIF" and name != "Loan": # Already included above
                content += f"{name} Deduction: R{amount:.2f}\n"
        return content
