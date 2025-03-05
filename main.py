from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# This will act as an in-memory database for the example.
leave_requests = []

# Helper function to calculate leave days excluding weekends (Saturday and Sunday)
def calculate_leave_days(start_date, end_date):
    current_date = start_date
    leave_days = 0
    while current_date <= end_date:
        if current_date.weekday() < 5:  # Monday to Friday are weekdays (0-4)
            leave_days += 1
        current_date += timedelta(days=1)
    return leave_days

# Helper function to check for overlapping leave requests
def has_overlapping_leave(employee_id, start_date, end_date):
    for leave in leave_requests:
        if leave['employee_id'] == employee_id:
            existing_start_date = datetime.strptime(leave['start_date'], "%Y-%m-%d")
            existing_end_date = datetime.strptime(leave['end_date'], "%Y-%m-%d")
            if (start_date <= existing_end_date and end_date >= existing_start_date):
                return True
    return False

# Endpoint to create a leave request
@app.route('/api/v1/leave-requests', methods=['POST'])
def create_leave_request():
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Initialize an empty list to collect error details
        error_details = []

        # Check if all required fields are present
        required_fields = ['employee_id', 'start_date', 'end_date', 'leave_type', 'reason']
        for field in required_fields:
            if field not in data:
                error_details.append(f"Missing {field} in request")

        # Parse dates and ensure they are valid
        try:
            start_date = datetime.strptime(data['start_date'], "%Y-%m-%d")
            end_date = datetime.strptime(data['end_date'], "%Y-%m-%d")
        except ValueError:
            error_details.append("Invalid date format. Use YYYY-MM-DD")

        # Ensure start date is not after end date
        if start_date > end_date:
            error_details.append("end_date must be after start_date")

        # Ensure the maximum consecutive leave days is not exceeded (14 days)
        max_consecutive_days = 14
        consecutive_leave_days = (end_date - start_date).days + 1
        if consecutive_leave_days > max_consecutive_days:
            error_details.append("Maximum consecutive leave days is 14")

        # If there are any errors, return them
        if error_details:
            return jsonify({"error": "VALIDATION_ERROR", "message": "Invalid request", "details": error_details}), 400

        # Check for overlapping leave requests for the employee
        if has_overlapping_leave(data['employee_id'], start_date, end_date):
            error_details.append("This leave request overlaps with an existing leave request")

        # If there are any overlapping errors, return them
        if error_details:
            return jsonify({"error": "VALIDATION_ERROR", "message": "Invalid request", "details": error_details}), 400

        # Calculate leave days excluding weekends (Saturday and Sunday)
        leave_days = calculate_leave_days(start_date, end_date)

        # Create a leave request object
        leave_request = {
            'employee_id': data['employee_id'],
            'start_date': start_date.strftime("%Y-%m-%d"),
            'end_date': end_date.strftime("%Y-%m-%d"),
            'leave_type': data['leave_type'],
            'reason': data['reason'],
            'leave_days': leave_days
        }

        # Add the leave request to the in-memory database
        leave_requests.append(leave_request)

        return jsonify({"message": "Leave request created successfully", "leave_request": leave_request}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Endpoint to get leave requests by employee_id
@app.route('/api/v1/leave-requests/<employee_id>', methods=['GET'])
def get_leave_requests_by_employee(employee_id):
    # Filter leave requests by employee_id
    employee_leaves = [leave for leave in leave_requests if leave['employee_id'] == employee_id]

    if not employee_leaves:
        return jsonify({"message": "No leave requests found for this employee"}), 404

    return jsonify({"employee_id": employee_id, "leave_requests": employee_leaves}), 200


if __name__ == '__main__':
    app.run(debug=True)
