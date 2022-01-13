import re
import psycopg2
from psycopg2 import Error
from datetime import date, time, datetime, timedelta

def executeSQL (sql):
    data = None
    connection = psycopg2.connect(user="",
                                  password="",
                                  host="localhost",
                                  port="5432",
                                  database="ScheduledMeetings")
    # Create a cursor to perform database operations
    cursor = connection.cursor()
    # Print PostgreSQL details
    print("PostgreSQL server information")
    print(connection.get_dsn_parameters(), "\n")
    cursor.execute(sql)
    connection.commit()
    if("SELECT" in sql):
        data = cursor.fetchall()
    cursor.close()
    connection.close()
    if(data != None):
        return data


def getCoursesForStudent(stundentEmail):
    sql = "SELECT * FROM scheduled WHERE scheduled.studentemail = '" + stundentEmail + "'"
    data = executeSQL(sql)
    print(data)

    courses = []

    if len(data) != 0:
        
        for i in range (0, len(data)):
            course = []
            course.append(data[i][0])
            course.append(data[i][1].strftime("%d %b, %Y"))
            course.append(data[i][2].strftime("%H:%M"))
            course.append(data[i][3])
            course.append(data[i][4])
            course.append(data[i][5])
            course.append(data[i][6])

            courses.append(course.copy())
            course.clear()
    print(courses)

    return courses

def getCoursesForInstructor(instructorEmail):
    sql = "SELECT * FROM scheduled WHERE scheduled.instructoremail = '" + instructorEmail + "'"
    data = executeSQL(sql)
    print(data)

    courses = []

    if len(data) != 0:
        
        for i in range (0, len(data)):
            course = []
            course.append(data[i][0])
            course.append(data[i][1].strftime("%d %b, %Y"))
            course.append(data[i][2].strftime("%H:%M"))
            course.append(data[i][3])
            course.append(data[i][4])
            course.append(data[i][5])
            course.append(data[i][6])

            courses.append(course.copy())
            course.clear()
    print(courses)

    return courses

def getListOfInstructors():
    sql = "SELECT * FROM instructor"
    data = executeSQL(sql)
    for i in range (0, len(data)):
        data[i] = list(data[i])
    return data

def getCourseHoursOfInstructorForADay(instructorEmail, day):
    sql = "SELECT scheduled.time FROM scheduled WHERE instructoremail = '" + instructorEmail + "' AND date = '" + day + "'"
    data = executeSQL(sql)

    if len(data) !=0:
        for i in range(0, len(data)):
            data[i] = data[i][0]

    return data

def getInstructorNameByMail(email):
    sql = "SELECT name FROM instructor WHERE email = '" + email +"'"
    data = executeSQL(sql)
    return data[0][0]

def getAllUsers():
    sql = "SELECT * FROM student"
    data = executeSQL(sql)

    sql = "SELECT * FROM instructor"
    data += executeSQL(sql)
    for i in range (0, len(data)):
        data[i] = list(data[i])

    return data

def getSchedulesForAPeriod(startday, endday):
    sql = "SELECT * FROM scheduled WHERE date > '" + startday + "' AND date < '" + endday + "'"
    data = executeSQL(sql)

    if len(data) != 0:
        for i in range (0, len(data)):
            data[i] = list(data[i])

    return data


def insertStudent(email, name, surname, password):
    sql = "INSERT INTO student(email, name, surname, password) VALUES ('" + email + "', '" + name + "', '" + surname + "', '" + password + "')"
    executeSQL(sql)

def insertInstructor(email, name, surname, password):
    sql = "INSERT INTO instructor(email, name, surname, password) VALUES ('" + email + "', '" + name + "', '" + surname + "', '" + password + "')"
    executeSQL(sql)

def insertSchedule(date, time, studentEmail, instructorEmail):
    sql = "INSERT INTO scheduled (date, time, studentemail, instructoremail) VALUES ('" + date + "','" + time + "','" + studentEmail + "','" + instructorEmail + "')"
    executeSQL(sql)


def deleteCourse(id):
    sql = "DELETE FROM scheduled WHERE id =" + id
    executeSQL(sql)


def validLogin(selectedRole, email, password):
    
    if selectedRole == "student":
        sql = "SELECT * FROM student WHERE student.email = '" + email + "' AND student.password = '" + password + "'"
    elif selectedRole == "instructor":
        sql = "SELECT * FROM instructor WHERE instructor.email = '" + email + "' AND instructor.password = '" + password + "'"
    elif selectedRole == "admin":
        sql = "SELECT * FROM admin WHERE admin.email = '" + email + "' AND admin.password = '" + password + "'"

    data = executeSQL(sql)

    if len(data) != 0:
        if selectedRole != "admin" and data[0][4] == 0:
            return False
        return True
    else:
        return False

def confirmCourse(courseid):
    sql = "UPDATE scheduled SET isapprovedbyinstructor = 1 WHERE id = " + str(courseid)
    executeSQL(sql)

def approveUser(email):
    sql = "UPDATE student SET isapproved = 1 WHERE email = '" + email + "'"
    executeSQL(sql)

    sql = "UPDATE instructor SET isapproved = 1 WHERE email = '" + email + "'"
    executeSQL(sql)

