import time
from flask import Flask, render_template, Flask, redirect, url_for, request, flash, json
import flask
from flask.helpers import flash


from backendMethods import *
from dbMethods import *

app = Flask(__name__, static_folder='static')
app.secret_key = "ertugrul"



@app.route('/login', methods = ['POST', 'GET'])
def loginPage():
    global selectedRole
    if request.method == 'POST':
        print("POST REQUEST CAME")
        selectedRole = request.form['selectedRole']
        print("Selected Role = ", selectedRole)
        if 'signupButton' in request.form:
            return redirect("/register")
        elif 'loginButton' in request.form:
            global loginEmail
            loginEmail = request.form['inputEmail']
            loginPassword = request.form['inputPassword']
            print("email = %s, password = %s" % (loginEmail, loginPassword))

             

            if selectedRole == "student" and validLogin(selectedRole, loginEmail, loginPassword): 
                return redirect("/student")
            elif selectedRole == "instructor" and validLogin(selectedRole, loginEmail, loginPassword):
                return redirect("/instructor")
            elif selectedRole == "admin" and validLogin(selectedRole, loginEmail, loginPassword):
                return redirect("/admin")
            else:
                flash("EMAİL OR PASSWORD IS NOT CORRECT!\nOR NEED TO BE APPROVED BY ADMIN")
                return redirect("/login")


            
    

    return render_template('loginForm.html')


@app.route('/register', methods = ['POST', 'GET'])
def registerPage():
    global selectedRole
    if request.method == 'POST':
        print("POST REQUEST CAME")
        signupEmail = request.form['inputEmail']
        signupName = request.form['inputName']
        signupSurname = request.form['inputSurname']
        signupPassword = request.form['inputPassword']
        print("email = %s, name = %s, surname= %s, password = %s" % (signupEmail, signupName, signupSurname, signupPassword)) 
        print(selectedRole)
        if selectedRole == "student":
            insertStudent(signupEmail, signupName, signupSurname, signupPassword)
            print("STUDENT INSTERTED")
            flash("ACCOUNT HAS BEEN CREATED")
        elif selectedRole == "instructor":    
            insertInstructor(signupEmail, signupName, signupSurname, signupPassword)
            print("INSTRUCTOR INSTERTED")
            flash("ACCOUNT HAS BEEN CREATED")
        

        
        return redirect("/login")
    

    return render_template('accountForm.html')


@app.route('/student', methods = ['POST', 'GET'])
def studentPage():
    global selectedRole
    global loginEmail
    global instructorEmail
    global selectedDate
    studentCourses = getCoursesForStudent(loginEmail)
    instructors = getListOfInstructors()
    availableHours = []
    instructorName = ""
    if request.method == 'POST':
        print("POST REQUEST CAME")
        if 'showButton' in request.form:
            selectedInstructor = request.form['selectedInstructor']
            selectedDate = request.form['day']
            print("selected instructor = %s, day = %s" % (selectedInstructor, selectedDate))
            availableHours, instructorEmail = availableHoursOfInstructor(selectedInstructor, selectedDate)
            instructorName = getInstructorNameByMail(instructorEmail)
            print(availableHours)
        elif 'courseCancelButton' in request.form:
            canceledCourseId = request.form['courseCancelButton']
            deleteCourse(canceledCourseId)
            print("Canceled Course = ",canceledCourseId)
            return redirect("/student")
        elif 'takeCourseButton' in request.form:
            desiredHour = request.form['takeCourseButton']
            print("%s %s %s %s" %(selectedDate, desiredHour, loginEmail, instructorEmail))
            insertSchedule(selectedDate, desiredHour, loginEmail, instructorEmail)
            return redirect("/student")
        elif 'logout' in request.form:
            return redirect("/login")

            
    

    return render_template('student.html', instructors = instructors, availableHours = availableHours, instructorName = instructorName, studentCourses = studentCourses)


@app.route('/instructor', methods = ['POST', 'GET'])
def instructorPage():
    global selectedRole
    global loginEmail

    confirmedCourses, waitingConfirmCourses = seperateConfirmedCourses(loginEmail)
    print("Confirmed Courses",confirmedCourses)
    print("Waiting Confirm Courses", waitingConfirmCourses)
    if request.method == 'POST':
        print("POST REQUEST CAME")
        if 'confirmCourseButton' in request.form:
            courseid = request.form['confirmCourseButton']
            confirmCourse(courseid)
            return redirect("/instructor")
        elif 'courseCancelButton' in request.form:
            canceledCourseId = request.form['courseCancelButton']
            deleteCourse(canceledCourseId)
            print("Canceled Course = ",canceledCourseId)
            return redirect("/instructor")
        elif 'logout' in request.form:
            return redirect("/login")
        
    

    return render_template('instructor.html', confirmedCourses = confirmedCourses, waitingConfirmCourses = waitingConfirmCourses)

@app.route('/admin', methods = ['POST', 'GET'])
def adminPage():
    global selectedRole
    global loginEmail

    allUsers = getAllUsers()
    specificCourses = []
    if request.method == 'POST':
        print("POST REQUEST CAME")
        if 'ApproveButton' in request.form:
            email = request.form['ApproveButton']
            print(email)
            approveUser(email)
            return redirect("/admin")
        elif 'specificPeriodButton' in request.form:
            startDay = request.form['startDay']
            endDay = request.form['endDay']
            print("start day = %s, end day = %s" % (startDay, endDay))
            specificCourses = getSchedulesForAPeriod(startDay, endDay)
            specificCourses = specificPeriodCourses(specificCourses).copy()
            print(specificCourses)
            print("SPECIFIC COURSES", specificCourses)
        elif 'logout' in request.form:
            return redirect("/login")
            


    return render_template("admin.html", allUsers = allUsers, specificCourses = specificCourses)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')