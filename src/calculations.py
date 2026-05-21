import datetime
from typing import List
from models import TimeEntry, Worker, Payslip, Leave, Loan

# SA Legal Limits
MAX_NORMAL_DAILY_HOURS = 9
MAX_NORMAL_WEEKLY_HOURS = 45
UIF_RATE = 0.01  # 1% of gross salary
UIF_MAX_EARNINGS_FOR_CONTRIBUTION = 17712  # R17,712 per month, for example
ANNUAL_LEAVE_ACCRUAL_RATE = 1 / 17  # 1 day per 17 days worked

def calculate_daily_hours(start_time: datetime.time, end_time: datetime.time) -> float:
    dt_start = datetime.datetime.combine(datetime.date.min, start_time)
    dt_end = datetime.datetime.combine(datetime.date.min, end_time)
    time_diff = dt_end - dt_start
    return time_diff.total_seconds() / 3600

def calculate_overtime(daily_hours: float) -> float:
    if daily_hours > MAX_NORMAL_DAILY_HOURS:
        return daily_hours - MAX_NORMAL_DAILY_HOURS
    return 0.0

def calculate_monthly_pay(worker: Worker, month: datetime.date, all_time_entries: List[TimeEntry]) -> Payslip:
    total_normal_hours = 0.0
    total_overtime_hours = 0.0
    days_worked_in_month = set()

    # Filter time entries for the specific worker and month
    monthly_entries = [entry for entry in all_time_entries
                       if entry.worker_id == worker.worker_id and
                       entry.date.year == month.year and
                       entry.date.month == month.month]

    # Group entries by week to calculate weekly overtime
    # A simpler approach for daily and then total overtime for now.
    # Weekly overtime calculation can be more complex if daily overtime is deducted from weekly normal hours.
    # For this task, we'll focus on daily overtime first and total hours.

    for entry in monthly_entries:
        daily_total_hours = calculate_daily_hours(entry.start_time, entry.end_time)
        daily_overtime = calculate_overtime(daily_total_hours)

        total_normal_hours += (daily_total_hours - daily_overtime)
        total_overtime_hours += daily_overtime
        days_worked_in_month.add(entry.date)

    # Calculate gross pay
    gross_pay = (total_normal_hours * worker.hourly_rate) + (total_overtime_hours * worker.hourly_rate * 1.5) # Overtime at 1.5x

    # Calculate UIF
    uif_deduction = min(gross_pay * UIF_RATE, UIF_MAX_EARNINGS_FOR_CONTRIBUTION * UIF_RATE * 2) # Employer and Employee contribute

    # Calculate loan deductions for the month
    loan_deduction_for_month = 0.0
    for loan in worker.loans:
        for repayment_date, amount in loan.repayment_schedule:
            if repayment_date.year == month.year and repayment_date.month == month.month and loan.repaid_amount < loan.loan_amount:
                deductible_amount = min(amount, loan.loan_amount - loan.repaid_amount)
                loan_deduction_for_month += deductible_amount
                loan.repaid_amount += deductible_amount
                # Break after finding the first applicable repayment for the month
                break

    net_pay = gross_pay - uif_deduction - loan_deduction_for_month

    payslip = Payslip(
        worker_id=worker.worker_id,
        month=month,
        total_hours=total_normal_hours + total_overtime_hours,
        total_overtime_hours=total_overtime_hours,
        gross_pay=gross_pay,
        uif_deduction=uif_deduction,
        loan_deduction=loan_deduction_for_month,
        net_pay=net_pay
    )

    return payslip

def accrue_annual_leave(worker: Worker, days_worked: int) -> None:
    worker.accrued_annual_leave_days += days_worked * ANNUAL_LEAVE_ACCRUAL_RATE

