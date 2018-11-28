from flask import Flask, render_template
import sqlite3

DB_FILE = "HW11 Data/HW11-DB"
db = sqlite3.connect(DB_FILE)
instructors_pt_fields = ['CWID', 'Name', 'Dept', 'Course', 'Student Numbers']
list1 = []
for row in db.execute("select CWID, Name, Dept, Course, count(Student_CWID) from HW11_instructors join HW11_grades "
                      "on CWID = Instructor_CWID group by Course order by CWID"):
    list1.append(row)

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World"

@app.route('/Goodbye')
def see_ya():
    return "see you later!"

@app.route('/Instructors')
def template_demo():
    print(list1)
    return render_template('instructor_table.html',
                           title="Stevens Repository",
                           my_header="My Stevens Repository",
                           instructorlist=list1)

app.run(debug=True)