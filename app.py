# app.py
from flask import Flask, request, jsonify, render_template
from db import db, Patient
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME
from utility import this_time

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# 第一次啟動時建立 table
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    # return jsonify({"message": "tung_register_app running (Flask + SQLAlchemy + MySQL)"}), 200
    data = get_patients()[0].get_json() 
    return render_template('index.html', show_data=data, today=this_time())

# GET all
@app.route("/patients", methods=["GET"])
def get_patients():
    patients = Patient.query.order_by(Patient.id).all()
    return jsonify([p.to_dict() for p in patients]), 200

# GET single
@app.route("/patients/<int:pid>", methods=["GET"])
def get_patient(pid):
    p = Patient.query.get(pid)
    if not p:
        return jsonify({"error": "Patient not found"}), 404
    return jsonify(p.to_dict()), 200

# POST create
@app.route("/patients", methods=["POST"])
def add_patient():
    data = request.get_json() or {}
    name = data.get("name")
    age = data.get("age")
    department = data.get("department")
    if not name or age is None or not department:
        return jsonify({"error": "Missing fields (name, age, department)"}), 400

    try:
        age = int(age)
    except ValueError:
        return jsonify({"error": "age must be integer"}), 400

    p = Patient(name=name, age=age, department=department)
    db.session.add(p)
    db.session.commit()
    return jsonify({"message": "Patient added", "id": p.id}), 201

# PUT update
@app.route("/patients/<int:pid>", methods=["PUT"])
def update_patient(pid):
    p = Patient.query.get(pid)
    if not p:
        return jsonify({"error": "Patient not found"}), 404

    data = request.get_json() or {}
    name = data.get("name")
    age = data.get("age")
    department = data.get("department")

    if name:
        p.name = name
    if age is not None:
        try:
            p.age = int(age)
        except ValueError:
            return jsonify({"error": "age must be integer"}), 400
    if department:
        p.department = department

    db.session.commit()
    return jsonify({"message": "Patient updated"}), 200

# DELETE
@app.route("/patients/<int:pid>", methods=["DELETE"])
def delete_patient(pid):
    p = Patient.query.get(pid)
    if not p:
        return jsonify({"error": "Patient not found"}), 404
    db.session.delete(p)
    db.session.commit()
    return jsonify({"message": "Patient deleted"}), 200

if __name__ == "__main__":
    app.run(debug=True)
