# Contract-Time-Manager

A South African labour-law-compliant payroll and time-tracking app for households employing domestic workers or gardeners.

## Table of Contents
- [Description](#description)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)

## Description
This project is a Python-based application designed to manage payroll and time tracking for domestic workers and gardeners in South Africa, ensuring compliance with local labour laws. It provides functionalities for managing worker data, time entries, leaves, and loans, and calculates salaries based on these inputs.

## Features
- Worker management (add, update, view)
- Time entry tracking
- Leave management
- Loan management
- Payroll calculations compliant with South African labour law
- Data persistence using JSON files

## Installation

To set up the project locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/Contract-Time-Manager.git
    cd Contract-Time-Manager
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    -   On Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    -   On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt # Assuming a requirements.txt will be created or is present
    ```

## Usage

To run the application, ensure your virtual environment is activated and then execute the main application file:

```bash
python src/app.py
```

The application will then be accessible via its command-line interface or web interface (depending on its implementation, which isn't fully clear from the file list).

## Project Structure

```
Contract-Time-Manager/
├── data/
│   ├── leaves.json
│   ├── loans.json
│   ├── time_entries.json
│   └── workers.json
├── src/
│   ├── app.py           # Main application logic and entry point
│   ├── calculations.py  # Contains payroll and time calculation logic
│   ├── data_manager.py  # Handles reading from and writing to JSON data files
│   └── models.py        # Defines data models (e.g., Worker, TimeEntry, Leave, Loan)
├── test_app.py          # Unit tests for the application
└── README.md            # This README file
```

## Technologies Used
- Python 3.x
- (Potentially other libraries, to be added if a `requirements.txt` is provided or inferred.)
