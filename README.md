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
    pip install Flask Flask-CORS
    ```

## Usage

The application now has a web interface.

To run the web application, ensure your virtual environment is activated and follow these steps:

1.  **Start the Flask API:**
    Navigate to the `src` directory and run the API:
    ```bash
    cd src
    python api.py
    ```
    The API will run on `http://127.0.0.1:5000`.

2.  **Open the Web Interface:**
    Open the `index.html` file in your web browser. You can do this by navigating to the project's root directory and double-clicking `index.html`, or by opening it through your browser's file menu.

## Project Structure

```
Contract-Time-Manager/
├── data/
│   ├── leaves.json
│   ├── loans.json
│   ├── time_entries.json
│   └── workers.json
├── index.html           # Web interface for the application
├── style.css            # Stylesheet for the web interface
├── script.js            # JavaScript for frontend logic and API calls
├── src/
│   ├── api.py           # Flask API to expose application functionalities
│   ├── app.py           # Contains the core application logic and data models (not a direct entry point for execution as a CLI application anymore.)
│   ├── calculations.py  # Contains payroll and time calculation logic
│   ├── data_manager.py  # Handles reading from and writing to JSON data files
│   └── models.py        # Defines data models (e.g., Worker, TimeEntry, Leave, Loan)

├── test_app.py          # Unit tests for the application
└── README.md            # This README file
```

## Technologies Used
- Python 3.x
- Flask (for the web API)
- Flask-CORS (for handling Cross-Origin Resource Sharing)

- HTML5, CSS3, JavaScript (for the web interface)

