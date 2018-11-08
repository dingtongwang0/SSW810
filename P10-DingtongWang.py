import os
from prettytable import PrettyTable
from collections import defaultdict


class Student:
    pt_fields = ['CWID', 'Name', 'Major', 'Passed Courses', 'Remaining Required Courses', 'Remaining Elective Courses']

    def __init__(self, cwid, name, major):
        self.cwid = cwid
        self.name = name
        self.major = major
        self.courses = dict()

    def add_course(self, course_name, grade):
        self.courses[course_name] = grade

    def get_passed_courses(self):
        passed_courses = dict()
        passed_course_names = [course_name for course_name in self.courses.keys()
                               if self.courses[course_name] == 'A' or 'A-' or 'B+' or 'B' or 'B-' or 'C+' or 'C']

        for passed_course_name in passed_course_names:
            passed_courses[passed_course_name] = self.courses[passed_course_name]
        return passed_courses

    def get_remaining_courses(self):
        remaining_courses = Major(self.major).get_remaining_courses(self.get_passed_courses())
        return remaining_courses

    def get_remaining_required_courses(self):
        remaining_required_courses = [course_name for course_name in self.get_remaining_courses().keys()
                                      if self.get_remaining_courses()[course_name] == 'R']
        return remaining_required_courses

    def get_remaining_elective_courses(self):
        remaining_elective_courses = [course_name for course_name in self.get_remaining_courses().keys()
                                      if self.get_remaining_courses()[course_name] == 'E']
        return remaining_elective_courses

    def get_list(self):
        return [self.cwid, self.name, self.major, self.get_passed_courses(),
                self.get_remaining_required_courses(), self.get_remaining_elective_courses()]


class Instructor:
    pt_fields = ['CWID', 'Name', 'Department', 'Course', 'Student Numbers']

    def __init__(self, cwid, name, dept):
        self.cwid = cwid
        self.name = name
        self.dept = dept
        self.courses = defaultdict(int)

    def add_student(self, course_name):
        self.courses[course_name] += 1

    def get_list(self):
        return[[self.cwid, self.name, self.dept, course_name, student_numbers]
               for course_name, student_numbers in sorted(self.courses.items())]


class Major:
    pt_fields = ['Major', 'Required Courses', 'Elective Courses']

    def __init__(self, name):
        self.name = name
        self.courses = dict()

    def add_course(self, course_name, course_type):
        self.courses[course_name] = course_type

    def get_remaining_courses(self, passed_courses):
        remaining_courses = dict()
        for course_name in self.courses.keys():
            if course_name not in passed_courses.keys():
                remaining_courses[course_name] = self.courses[course_name]
        return remaining_courses

    def get_list(self):
        return [self.name, [course_name for course_name in self.courses.keys() if self.courses[course_name] == 'R'],
                [course_name for course_name in self.courses.keys() if self.courses[course_name] == 'E']]


class Repository:
    def __init__(self, dir_path, pt = True):
        self.students = dict()
        self.instructors = dict()
        self.majors = dict()

        self.students_path = os.path.join(dir_path, 'students.txt')
        self.instructors_path = os.path.join(dir_path, 'instructors.txt')
        self.grades_path = os.path.join(dir_path, 'grades.txt')
        self.majors_path = os.path.join(dir_path, 'majors.txt')

        self.read_students(self.students_path)
        self.read_instructors(self.instructors_path)
        self.read_grades(self.grades_path)
        self.read_majors(self.majors_path)

        if pt:
            print('\nStudent Summary')
            self.get_students_pt()

            print('\nInstructor Summary')
            self.get_instructors_pt()

            print('\nMajors Summary')
            self.get_majors_pt()

    def read_students(self, path):
        for cwid, name, major in file_reader(path, fields=3, sep='\t', header=False):
            self.students[cwid] = Student(cwid, name, major)

    def read_instructors(self, path):
        for cwid, name, dept in file_reader(path, fields=3, sep='\t', header=False):
            self.instructors[cwid] = Instructor(cwid, name, dept)

    def read_grades(self, path):
        for student_cwid, course_name, grade, instructor_cwid in file_reader(path, fields=4, sep='\t', header=False):
            self.students[student_cwid].add_course(course_name, grade)
            self.instructors[instructor_cwid].add_student(course_name)

    def read_majors(self, path):
        for major_name, course_type, course_name in file_reader(path, fields=3, sep='\t', header=False):
            if major_name not in self.majors.keys():
                self.majors[major_name] = Major(major_name)
            self.majors[major_name].add_course(course_name, course_type)

    def get_students_pt(self):
        students_pt = PrettyTable(field_names=Student.pt_fields)
        for student in self.students.values():
            students_pt.add_row(student.get_list())
        print(students_pt)

    def get_instructors_pt(self):
        instructors_pt = PrettyTable(field_names=Instructor.pt_fields)
        for instructor in self.instructors.values():
            for row in instructor.get_list():
                instructors_pt.add_row(row)
        print(instructors_pt)

    def get_majors_pt(self):
        majors_pt = PrettyTable(field_names=Major.pt_fields)
        for major in self.majors.values():
            majors_pt.add_row(major.get_list())
        print(majors_pt)


def file_reader(path, fields, sep=',', header=False):
    try:
        file_hand = open(path, 'r')
        if header:
            next(file_hand)

    except FileNotFoundError:
        print("can't open", path)

    else:
        line = file_hand.readline()
        while line:
            yield(line.strip().split(sep, fields))
            line = file_hand.readline()

        file_hand.close()


def main():
    stevens = Repository('/Users/lawrencewang/Documents/Homework/SSW810/Stevens')

main()