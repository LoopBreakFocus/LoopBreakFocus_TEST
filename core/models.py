from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class EmployeeData(db.Model):
    __tablename__ = 'employee_data'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    department = db.Column(db.String(100))
    date = db.Column(db.Date)
    goal = db.Column(db.Text)
    hours_worked = db.Column(db.Float)
    blockers = db.Column(db.Text)

    def __init__(self, name, department, date, goal, hours_worked, blockers):
        self.name = name
        self.department = department
        self.date = date
        self.goal = goal
        self.hours_worked = hours_worked
        self.blockers = blockers