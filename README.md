# Leave Management API

This is a simple Flask-based API for managing employee leave requests. It supports creating leave requests and fetching them by `employee_id`. The API also performs validations like checking for overlapping leaves and enforcing maximum leave days.

## Setup Instructions

### Prerequisites

- Python 3.6 or higher
- `pip` (Python package installer)

### Install Dependencies

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/leave-management-api.git
   cd leave-management-api

## Create a virtual environment (optional but recommended):
    
    python3 -m venv venv
    source venv/bin/activate  

## Install the required dependencies:


    pip install -r requirements.txt

## Run the Application
To run the Flask application, use the following command:

    python main.py

This will start the server on http://127.0.0.1:5000/ (or localhost:5000).

