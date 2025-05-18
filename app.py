from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import date 


# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///habits.db"
# disable SQLAlchemy from tracking every object change and sending warning signals
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable = False)
    completed = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()


    if not Habit.query.first():
        test_habits = [
            Habit(name="Drink water", date=date.today(), completed=True),
            Habit(name="Exercise", date=date.today(), completed=False),
            Habit(name="Read book", date=date.today(), completed=True),
        ]
        db.session.add_all(test_habits)
        db.session.commit()


@app.route('/api/habits', methods=['GET'])
def get_habits():
    habits = Habit.query.all()
    return jsonify([
        {
            "id": h.id,
            "name": h.name,
            "date": h.date.isoformat(),
            "completed" : h.completed
        }
        for h in habits
    ])
        

@app.route('/api/habits', methods=['POST'])
def add_habit():
    data = request.get_json()
    new_habit = Habit(
        name = data['name'],
        date = date.fromisoformat(data['date']),
        completed = data.get('completed', False)
    )
    db.session.add(new_habit)
    db.session.commit()
    return jsonify({"message": "New habit added"}), 201

@app.route('/api/habits/<int:habit_id>', methods=['PUT'])
def update_habit(habit_id):
    data = request.get_json()
    habit = Habit.query.get_or_404(habit_id)
    habit.name = data.get('name', habit.name)
    habit.date = data.get('date', habit.date)
    habit.completed = data.get('completed', habit.completed)
    db.session.commit()
    return jsonify({'message': 'Habit updated successfully'})

@app.route('/api/habits/<int:habit_id>', methods=['DELETE'])
def delete_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    db.session.delete(habit)
    db.session.commit()
    return jsonify({'message': 'Habit deleted successfully'})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug = True)
