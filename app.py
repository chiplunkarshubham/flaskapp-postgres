from flask import Flask, jsonify, render_template, request
from models import db, Student

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@dev-postgres:5432/student'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

// 'postgresql://<username>:<password>@<db-container-name/db-service-name>:5432/<db-name>'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/students', methods=['POST'])
def create_student():
    name = request.json.get('name')
    course = request.json.get('course')
    date_joined = request.json.get('date_joined')

    student = Student(name=name, course=course, date_joined=date_joined)
    db.session.add(student)
    db.session.commit()

    return jsonify({'message': 'Student created successfully'})

@app.route('/students', methods=['GET'])
def get_students():
    name = request.args.get('name')

    if name:
        students = Student.query.filter_by(name=name).all()
    else:
        students = Student.query.all()

    result = []

    for student in students:
        result.append({
            'name': student.name,
            'course': student.course,
            'date_joined': student.date_joined.strftime('%Y-%m-%d')
        })

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
