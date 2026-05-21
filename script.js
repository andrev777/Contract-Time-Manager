const API_BASE_URL = "http://127.0.0.1:5000";

// Helper function to display messages
function displayMessage(elementId, message, isError = false) {
    const element = document.getElementById(elementId);
    element.textContent = message;
    element.className = isError ? "message error" : "message success";
}

// Add Worker
document.getElementById("add-worker-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const workerId = document.getElementById("worker-id").value;
    const workerName = document.getElementById("worker-name").value;
    const hourlyRate = parseFloat(document.getElementById("hourly-rate").value);

    try {
        const response = await fetch(`${API_BASE_URL}/workers`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ worker_id: workerId, name: workerName, hourly_rate: hourlyRate }),
        });
        const data = await response.json();
        if (response.ok) {
            displayMessage("add-worker-message", data.message);
            document.getElementById("add-worker-form").reset();
            await listWorkers(); // Refresh worker list after adding
        } else {
            displayMessage("add-worker-message", data.message || data.error, true);
        }
    } catch (error) {
        console.error("Error adding worker:", error);
        displayMessage("add-worker-message", "An error occurred while adding worker.", true);
    }
});

// List Workers
async function listWorkers() {
    const workersListDiv = document.getElementById("workers-list");
    workersListDiv.innerHTML = "<p>Loading workers...</p>";
    try {
        const response = await fetch(`${API_BASE_URL}/workers`);
        const data = await response.json();
        
        workersListDiv.innerHTML = ""; // Clear previous list
        if (response.ok) {
            if (Array.isArray(data) && data.length > 0) {
                data.forEach(worker => {
                    const workerDiv = document.createElement("div");
                    workerDiv.innerHTML = `
                        <strong>ID:</strong> ${worker.id}, 
                        <strong>Name:</strong> ${worker.name}, 
                        <strong>Hourly Rate:</strong> R${parseFloat(worker.hourly_rate).toFixed(2)}, 
                        <strong>Annual Leave Accrued:</strong> ${parseFloat(worker.annual_leave_accrued).toFixed(2)} days
                    `;
                    workersListDiv.appendChild(workerDiv);
                });
                displayMessage("list-workers-message", "Workers loaded successfully.");
            } else if (data.message) {
                workersListDiv.innerHTML = `<p>${data.message}</p>`;
                displayMessage("list-workers-message", data.message);
            } else {
                workersListDiv.innerHTML = "<p>No workers registered.</p>";
                displayMessage("list-workers-message", "No workers registered.");
            }
        } else {
            displayMessage("list-workers-message", data.message || data.error, true);
            workersListDiv.innerHTML = `<p>Error: ${data.message || data.error}</p>`;
        }
    } catch (error) {
        console.error("Error listing workers:", error);
        displayMessage("list-workers-message", "An error occurred while listing workers.", true);
        workersListDiv.innerHTML = "<p>Failed to load workers.</p>";
    }
}

document.getElementById("refresh-workers").addEventListener("click", listWorkers);

// Record Time Entry
document.getElementById("record-time-entry-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const workerId = document.getElementById("time-entry-worker-id").value;
    const date = document.getElementById("time-entry-date").value;
    const startTime = document.getElementById("time-entry-start-time").value;
    const endTime = document.getElementById("time-entry-end-time").value;

    try {
        const response = await fetch(`${API_BASE_URL}/time_entries`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ worker_id: workerId, date: date, start_time: startTime, end_time: endTime }),
        });
        const data = await response.json();
        if (response.ok) {
            displayMessage("time-entry-message", data.message);
            document.getElementById("record-time-entry-form").reset();
            await listWorkers(); // Refresh worker list to show updated leave accrual
        } else {
            displayMessage("time-entry-message", data.message || data.error, true);
        }
    } catch (error) {
        console.error("Error recording time entry:", error);
        displayMessage("time-entry-message", "An error occurred while recording time entry.", true);
    }
});

// Record Leave
document.getElementById("record-leave-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const workerId = document.getElementById("leave-worker-id").value;
    const leaveType = document.getElementById("leave-type").value;
    const startDate = document.getElementById("leave-start-date").value;
    const endDate = document.getElementById("leave-end-date").value;
    const daysTaken = parseFloat(document.getElementById("leave-days-taken").value);

    try {
        const response = await fetch(`${API_BASE_URL}/leaves`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ worker_id: workerId, leave_type: leaveType, start_date: startDate, end_date: endDate, days_taken: daysTaken }),
        });
        const data = await response.json();
        if (response.ok) {
            displayMessage("leave-message", data.message);
            document.getElementById("record-leave-form").reset();
        } else {
            displayMessage("leave-message", data.message || data.error, true);
        }
    } catch (error) {
        console.error("Error recording leave:", error);
        displayMessage("leave-message", "An error occurred while recording leave.", true);
    }
});

// Record Loan
document.getElementById("record-loan-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const workerId = document.getElementById("loan-worker-id").value;
    const loanAmount = parseFloat(document.getElementById("loan-amount").value);
    const startDate = document.getElementById("loan-start-date").value;
    const repaymentSchedule = document.getElementById("repayment-schedule").value;

    try {
        const response = await fetch(`${API_BASE_URL}/loans`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ worker_id: workerId, loan_amount: loanAmount, start_date: startDate, repayment_schedule: repaymentSchedule }),
        });
        const data = await response.json();
        if (response.ok) {
            displayMessage("loan-message", data.message);
            document.getElementById("record-loan-form").reset();
        } else {
            displayMessage("loan-message", data.message || data.error, true);
        }
    } catch (error) {
        console.error("Error recording loan:", error);
        displayMessage("loan-message", "An error occurred while recording loan.", true);
    }
});

// Generate Payslip
document.getElementById("generate-payslip-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const workerId = document.getElementById("payslip-worker-id").value;
    const month = document.getElementById("payslip-month").value;

    try {
        const response = await fetch(`${API_BASE_URL}/payslips`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ worker_id: workerId, month: month }),
        });
        const data = await response.json();
        const payslipOutput = document.getElementById("payslip-output");
        if (response.ok) {
            payslipOutput.textContent = data.message; // Assuming message contains the payslip content
            displayMessage("payslip-message", "Payslip generated successfully.");
        } else {
            payslipOutput.textContent = "";
            displayMessage("payslip-message", data.message || data.error, true);
        }
    } catch (error) {
        console.error("Error generating payslip:", error);
        displayMessage("payslip-message", "An error occurred while generating payslip.", true);
    }
});

// Initial load
document.addEventListener("DOMContentLoaded", listWorkers);
