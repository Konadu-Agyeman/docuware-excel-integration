from flask import Flask, request, jsonify
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# Set up Google Sheets connection
SERVICE_ACCOUNT_FILE = 'docuwareexcelintergration-40e3b9d1cd88.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)
sheet = client.open_by_key('1n8Vx60cTPEBIf5RykxPSqZ1uOWr2dt090GQkZa6gLpw').sheet1

@app.route('/update-sheet', methods=['POST'])
def update_sheet():
    data = request.json

    name = data.get('name')
    department = data.get('department')
    location = data.get('location')
    amount = data.get('amount')
    comment = data.get('comment')

    if not name:
        return jsonify({'error': 'Missing "name" field'}), 400

    # Check if the name exists
    rows = sheet.get_all_values()
    found = False

    for i, row in enumerate(rows[1:], start=2):
        if row[0].strip().lower() == name.strip().lower():
            sheet.update(f'B{i}', department)
            sheet.update(f'C{i}', location)
            sheet.update(f'D{i}', amount)
            sheet.update(f'E{i}', comment)
            found = True
            return jsonify({'status': 'updated', 'row': i}), 200

    # If not found, append
    sheet.append_row([name, department, location, amount, comment])
    return jsonify({'status': 'added'}), 200

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
