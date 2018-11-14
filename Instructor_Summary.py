import sqlite3
from prettytable import PrettyTable

DB_FILE = "HW11-DB"
db = sqlite3.connect(DB_FILE)

instructors_pt_fields = ['CWID', 'Name', 'Dept', 'Course', 'Student Numbers']

instructors_pt = PrettyTable(field_names=instructors_pt_fields)
for row in db.execute("select CWID, Name, Dept, Course, count(Student_CWID) from HW11_instructors join HW11_grades "
                      "on CWID = Instructor_CWID group by Course order by CWID"):
    instructors_pt.add_row(row)

print("Instructor Summary\n", instructors_pt)