from dbMethods import *

def availableHoursOfInstructor(instructorEmail, day):
    data = getCourseHoursOfInstructorForADay(instructorEmail, day)
    availableHours = ['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00']
    for i in range(0, len(data)):
        print(data, availableHours)
        data[i] = data[i].strftime("%H:%M")
        availableHours.remove(data[i])
    print(data)
    
    return availableHours, instructorEmail

def seperateConfirmedCourses(instructorEmail):
    courses = getCoursesForInstructor(instructorEmail)
    confirmedCourses = []
    waitingConfirmCourses = []

    for i in range(0, len(courses)):
        if courses[i][3] == 1:
            confirmedCourses.append(courses[i])
        else:
            waitingConfirmCourses.append(courses[i])

    return confirmedCourses, waitingConfirmCourses

def specificPeriodCourses(courses):
    for i in range (0, len(courses)):
        courses[i][1] = courses[i][1].strftime("%d %b, %Y")
        courses[i][2] = courses[i][2].strftime("%H:%M")

    return courses