import os
from prettytable import PrettyTable
from collections import defaultdict

class Student:
    pt_fileds = ['CWID', 'Name', 'Completed Courses']

    def __init__(self, cwid, name, major):
        self._cwid = cwid
        self._name = name
        self._major = major
        self._courses = defaultdict(str)

    def add_course(self, course, grade):
        self._courses[course] = grade

    def output(self, cwid):
        return (self._cwid, self._name, self._major, sorted(self.courses.keys()))

class Instructor:
    pt_fileds = ['CWID', 'Name', 'Dept', 'Course', 'Students']

    def __init__(self, cwid, name, dept):
        self.cwid = cwid
        self.name = name
        self.dept = dept
        self._classes = defaultdict(int)

    def add(self, course, container):
        self._classes[course] += 1

    def output(self):
        return [[self._cwid, self._name, self._dept, courses, students] for courses, students in self._classes.items()]


class University:
    def __init__(self, dir_path, pt = True):

        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if file == 'students.txt':
                    path1 = os.path.join(root, file)
                    student_gene = file_reader(path1, fields = 3, sep = '\t', header = True)
                if file == 'instructors.txt':
                    path2 = os.path.join(root, file)
                    instructors_gene = file_reader(path2, fields = 3, sep = '\t', header = True)
                if file == 'grades.txt':
                    path3 = os.path.join(root, file)
                    grades_gene = file_reader(path3, fields = 3, sep = '\t', header = True)

        for student_cwid, student_name, student_major in student_gene:
            self._students[student_cwid] = Student(student_cwid, student_name, student_major)

        for instructors_cwid, instructors_name, instructors_dept in instructors_gene:
            self._instructors[instructors_cwid].add(course)

        for

        # student_list = [cwid, name, completed_courses for cwid, name in student_gene for completed_courses in
        # instructors_list =
        #
        # student_pt = PrettyTable(field_names = ['CWID', 'Name', 'Completed Courses'])
        # for cwid, name, completed_courses in student_list:
        #     student_pt.add_row([cwid, name, completed_courses])
        #
        # instructors_pt = PrettyTable(field_names= ['CWID', 'Name', 'Dept', 'Course', 'Students'])
        # for cwid, name, dept, course, students in student_list:
        #     instructors_pt.add_row([cwid, name, dept, course, students])

def file_reader(path, fields, sep = ',', header = False):
    try:
        file_hand = open(path, 'r')
        if header:
            next(file_hand)

    except FileNotFoundError:
        print("can't open", path)

    else:
        line = file_hand.readline()
        while line:
            yield(line.split(sep, fields - 1))
            line = file_hand.readline()

        file_hand.close()

def main():
    stevens = Repository('/Users/lawrencewang/Documents/Homework/SSW810/Stevens')  # read files and generate prettytables

main()
