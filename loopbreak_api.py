from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime
import os
import sys

# Add backend path
sys.path.append(os.path.abspath("core"))
from models import db, EmployeeData

app = Flask(__name__)

# MySQL config
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/loopbreak'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()

# ---------- ROUTES ---------- #

@app.route('/hr/')
@app.route('/hr/<path:path>')
def serve_hr(path='index.html'):
    hr_dist = os.path.abspath('dashboard/dist')
    file_path = os.path.join(hr_dist, path)
    if not os.path.isfile(file_path):
        path = 'index.html'
    return send_from_directory(hr_dist, path)

@app.route('/employee/')
@app.route('/employee/<path:path>')
def serve_employee(path='index.html'):
    emp_dist = os.path.abspath('employee_frontend/dist')
    file_path = os.path.join(emp_dist, path)
    if not os.path.isfile(file_path):
        path = 'index.html'
    return send_from_directory(emp_dist, path)

# ---------- API ---------- #

@app.route('/api/submit_goals', methods=['POST'])
def submit_goals():
    data = request.json
    try:
        new_entry = EmployeeData(
            name=data['name'],
            department=data['department'],
            date=datetime.today().date(),
            goal=data['goal'],
            hours_worked=data['hours_worked'],
            blockers=data['blockers']
        )
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({"message": "Data submitted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------- FALLBACK FOR ROUTER ---------- #

@app.errorhandler(404)
def not_found(e):
    if request.path.startswith('/hr'):
        return send_from_directory('dashboard/dist', 'index.html')
    if request.path.startswith('/employee'):
        return send_from_directory('employee_frontend/dist', 'index.html')
    return jsonify({"error": "Not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)