from flask import Flask, jsonify, request, render_template_string, redirect, url_for

app = Flask(__name__)

# ============================
# In-memory database (for demo)
# ============================
students = [
    {"id": 1, "name": "Alice", "grade": 10, "section": "Zechariah"},
    {"id": 2, "name": "Bob", "grade": 9, "section": "Daniel"},
    {"id": 3, "name": "Charlie", "grade": 10, "section": "Zechariah"},
]

# ============================
# HTML Templates (inline)
# ============================
index_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Student Records</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f4f6f9; }
        .container { margin-top: 40px; }
        table { background: white; }
        th { cursor: pointer; }
    </style>
</head>
<body>
<div class="container">
    <h1 class="text-center mb-4">📚 Student Records</h1>

    <div class="d-flex justify-content-between mb-3">
        <a href="{{ url_for('add_student') }}" class="btn btn-primary">➕ Add Student</a>
        <div>
            <a href="/?sort=name" class="btn btn-outline-secondary btn-sm {% if sort_by=='name' %}active{% endif %}">Sort by Name</a>
            <a href="/?sort=grade" class="btn btn-outline-secondary btn-sm {% if sort_by=='grade' %}active{% endif %}">Sort by Grade</a>
            <a href="/?sort=section" class="btn btn-outline-secondary btn-sm {% if sort_by=='section' %}active{% endif %}">Sort by Section</a>
        </div>
    </div>

    <table class="table table-bordered table-hover shadow-sm">
        <thead class="table-dark">
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Grade</th>
                <th>Section</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for s in students %}
            <tr>
                <td>{{ s.id }}</td>
                <td>{{ s.name }}</td>
                <td>{{ s.grade }}</td>
                <td>{{ s.section }}</td>
                <td>
                    <a href="{{ url_for('edit_student', id=s.id) }}" class="btn btn-warning btn-sm">Edit</a>
                    <a href="{{ url_for('delete_student', id=s.id) }}" class="btn btn-danger btn-sm"
                       onclick="return confirm('Are you sure you want to delete this student?')">Delete</a>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
</body>
</html>
"""

add_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Add Student</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
<div class="container mt-5">
    <h2>Add New Student</h2>
    <form method="POST">
        <div class="mb-3">
            <label>Name</label>
            <input type="text" name="name" class="form-control" required>
        </div>
        <div class="mb-3">
            <label>Grade</label>
            <input type="number" name="grade" class="form-control" required>
        </div>
        <div class="mb-3">
            <label>Section</label>
            <input type="text" name="section" class="form-control" required>
        </div>
        <button class="btn btn-success">Save</button>
        <a href="/" class="btn btn-secondary">Cancel</a>
    </form>
</div>
</body>
</html>
"""

edit_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Edit Student</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
<div class="container mt-5">
    <h2>Edit Student</h2>
    <form method="POST">
        <div class="mb-3">
            <label>Name</label>
            <input type="text" name="name" class="form-control" value="{{ student.name }}" required>
        </div>
        <div class="mb-3">
            <label>Grade</label>
            <input type="number" name="grade" class="form-control" value="{{ student.grade }}" required>
        </div>
        <div class="mb-3">
            <label>Section</label>
            <input type="text" name="section" class="form-control" value="{{ student.section }}" required>
        </div>
        <button class="btn btn-success">Update</button>
        <a href="/" class="btn btn-secondary">Cancel</a>
    </form>
</div>
</body>
</html>
"""

# ============================
# Routes
# ============================

@app.route('/')
def home():
    sort_by = request.args.get('sort', 'id')
    sorted_students = sorted(students, key=lambda x: x.get(sort_by))
    return render_template_string(index_html, students=sorted_students, sort_by=sort_by)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        new_id = max([s['id'] for s in students] or [0]) + 1
        new_student = {
            "id": new_id,
            "name": request.form['name'],
            "grade": int(request.form['grade']),
            "section": request.form['section']
        }
        students.append(new_student)
        return redirect(url_for('home'))
    return render_template_string(add_html)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = next((s for s in students if s['id'] == id), None)
    if not student:
        return "Student not found", 404
    if request.method == 'POST':
        student['name'] = request.form['name']
        student['grade'] = int(request.form['grade'])
        student['section'] = request.form['section']
        return redirect(url_for('home'))
    return render_template_string(edit_html, student=student)

@app.route('/delete/<int:id>')
def delete_student(id):
    global students
    students = [s for s in students if s['id'] != id]
    return redirect(url_for('home'))

@app.route('/api/students')
def get_students():
    return jsonify(students)

# ============================
# Run the app
# ============================
if __name__ == '__main__':
    app.run(debug=True)
