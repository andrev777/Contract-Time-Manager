import json
import os
import datetime
from typing import List, Dict, Any
from models import Worker, TimeEntry, Leave, Loan, Payslip

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
            return obj.isoformat()
        if isinstance(obj, (Worker, TimeEntry, Leave, Loan, Payslip)):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)

def decode_datetime(dct):
    for key, value in dct.items():
        if isinstance(value, str):
            try:
                # Try parsing as datetime, then date, then time
                if 'T' in value:
                    dct[key] = datetime.datetime.fromisoformat(value)
                elif len(value.split('-')) == 3:
                    dct[key] = datetime.date.fromisoformat(value)
                elif len(value.split(':')) >= 2:
                    dct[key] = datetime.time.fromisoformat(value)
            except ValueError:
                pass
    return dct

class DataManager:
    def __init__(self, data_dir: str = 'data'):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        self.workers_file = os.path.join(data_dir, 'workers.json')
        self.time_entries_file = os.path.join(data_dir, 'time_entries.json')
        self.leaves_file = os.path.join(data_dir, 'leaves.json')
        self.loans_file = os.path.join(data_dir, 'loans.json')

    def save_data(self, workers: List[Worker], time_entries: List[TimeEntry], leaves: List[Leave], loans: List[Loan]):
        with open(self.workers_file, 'w') as f:
            json.dump([w.__dict__ for w in workers], f, cls=CustomEncoder, indent=4)
        with open(self.time_entries_file, 'w') as f:
            json.dump([t.__dict__ for t in time_entries], f, cls=CustomEncoder, indent=4)
        with open(self.leaves_file, 'w') as f:
            json.dump([l.__dict__ for l in leaves], f, cls=CustomEncoder, indent=4)
        with open(self.loans_file, 'w') as f:
            json.dump([l.__dict__ for l in loans], f, cls=CustomEncoder, indent=4)

    def load_data(self) -> tuple[List[Worker], List[TimeEntry], List[Leave], List[Loan]]:
        workers: List[Worker] = []
        time_entries: List[TimeEntry] = []
        leaves: List[Leave] = []
        loans: List[Loan] = []

        if os.path.exists(self.workers_file):
            with open(self.workers_file, 'r') as f:
                worker_dicts = json.load(f, object_hook=decode_datetime)
                for wd in worker_dicts:
                    worker = Worker(wd['worker_id'], wd['name'], wd['hourly_rate'])
                    worker.accrued_annual_leave_days = wd.get('accrued_annual_leave_days', 0.0)
                    # Time entries, leaves, and loans are loaded separately and linked later
                    workers.append(worker)

        if os.path.exists(self.time_entries_file):
            with open(self.time_entries_file, 'r') as f:
                entry_dicts = json.load(f, object_hook=decode_datetime)
                for td in entry_dicts:
                    time_entries.append(TimeEntry(td['worker_id'], td['date'], td['start_time'], td['end_time']))

        if os.path.exists(self.leaves_file):
            with open(self.leaves_file, 'r') as f:
                leave_dicts = json.load(f, object_hook=decode_datetime)
                for ld in leave_dicts:
                    leaves.append(Leave(ld['worker_id'], ld['leave_type'], ld['start_date'], ld['end_date'], ld['days_taken']))

        if os.path.exists(self.loans_file):
            with open(self.loans_file, 'r') as f:
                loan_dicts = json.load(f, object_hook=decode_datetime)
                for lnd in loan_dicts:
                    loan = Loan(lnd['worker_id'], lnd['loan_amount'], lnd['start_date'],
                                [(datetime.date.fromisoformat(d), a) for d, a in lnd['repayment_schedule']])
                    loan.repaid_amount = lnd.get('repaid_amount', 0.0)
                    loans.append(loan)

        # Link time entries, leaves, and loans to workers after loading all
        worker_map = {worker.worker_id: worker for worker in workers}
        for entry in time_entries:
            if entry.worker_id in worker_map:
                worker_map[entry.worker_id].time_entries.append(entry)
        for leave_item in leaves:
            if leave_item.worker_id in worker_map:
                worker_map[leave_item.worker_id].leave_days.append(leave_item)
        for loan_item in loans:
            if loan_item.worker_id in worker_map:
                worker_map[loan_item.worker_id].loans.append(loan_item)

        return workers, time_entries, leaves, loans
