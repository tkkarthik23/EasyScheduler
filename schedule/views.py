from django.shortcuts import render, redirect
import mysql.connector
import datetime, itertools
from datetime import datetime, date, time, timedelta
from django.db import connections
from django.http import HttpResponseRedirect
from operator import itemgetter
from django.core.mail import EmailMessage, get_connection
from django.conf import settings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import icalendar
# Create your views here.

def index(request):
    context = 0
    return render(request, "html/blank.html")

def sprintPage():
        cursor = connections['default'].cursor()
        cursor.execute('''SELECT COUNT(*) FROM `sprints`''')
        helper1 = str(cursor.fetchone()[0])
        cursor.execute('''SELECT COUNT(*) FROM `tasks`''')
        helper2 = str(cursor.fetchone()[0])
        cursor.execute('''SELECT COUNT(*) FROM `users`''')
        helper4 = str(cursor.fetchone()[0])
        cursor.execute('''SELECT * FROM `sprints` WHERE status="notPlanned"''')
        sprintDeatils = cursor.fetchall()
        cursor.execute('''SELECT * FROM `sprints` WHERE status="Planned"''')
        sprintDeatilsPlanned = cursor.fetchall()
        helper3 = len(sprintDeatilsPlanned)
        return sprintDeatils, helper1, helper2, helper3, helper4, sprintDeatilsPlanned

def sprintsini(request):
    cursor = connections['default'].cursor()
    sprintDeatils, helper1, helper2, helper3, helper4, sprintDeatilsPlanned = sprintPage()
    context = {'sprintDeatils': sprintDeatils, 'helper1': helper1, 'helper2': helper2, 'helper3': helper3, 'helper4': helper4, 'sprintDeatilsPlanned': sprintDeatilsPlanned}
    return render(request, "html/sprintPage.html", context)

def createSprint(request):
    sprint_Name = request.GET.get("sprintName")
    sprint_StartDate = request.GET.get("startDate")
    date_object = datetime.strptime(sprint_StartDate, "%Y-%m-%d")
    end_Date = date_object + timedelta(days = 14)
    processed_EndDate = end_Date.date()
    print(type(end_Date))
    print(end_Date.date())
    cursor = connections['default'].cursor()
    cursor.execute(
        '''INSERT INTO sprints(sprintName, startDate, endDate, status) VALUES(%s, %s, %s, "notPlanned")''',
        [sprint_Name, sprint_StartDate, processed_EndDate])
    return HttpResponseRedirect('../sprintPage')

def renderSprint(request):
    sprintID = request.GET.get("sprintID")
    startDate = request.GET.get("startDate")
    endDate = request.GET.get("endDate")
    if request.GET.get("message") =="" :
        message = ""
    else:
        message = request.GET.get("message")
    if request.GET.get("message1") =="" :
        message1 = ""
    else:
        message1 = request.GET.get("message1")
    cursor = connections['default'].cursor()
    cursor.execute('''SELECT COUNT(*) FROM `users`''')
    no_Users = str(cursor.fetchone()[0])
    cursor.execute('''SELECT * FROM `users` WHERE sprintId= %s''', [sprintID])
    user_Details = cursor.fetchall()
    cursor.execute('''SELECT * FROM `tasks` WHERE sprintId= %s''', [sprintID])
    task_Details = cursor.fetchall()
    context = {'no_Users': no_Users, "user_Details":user_Details, "sprintID":sprintID, 'task_Details':task_Details, 'startDate':startDate, 'endDate':endDate, 'message': message, 'message1': message1}
    return render(request, "html/renderSprint.html", context)

def addUser(request):
    sprintID = request.GET.get("sprintId")
    startDate = parseDate(request.GET.get("startDate"))
    endDate = parseDate(request.GET.get("endDate"))
    cursor = connections['default'].cursor()
    cursor.execute('''SELECT COUNT(*) FROM `users`''')
    no_Users = str(cursor.fetchone()[0])
    context = {'no_Users': no_Users, 'sprintID': sprintID, 'startDate':startDate, 'endDate':endDate}
    return render(request, "html/addUserForm.html", context)

def userAddition(request):
    sprintId = request.GET.get("sprintId")
    userName = request.GET.get("userName")
    email = request.GET.get("email")
    startDate = reverseParseDate(request.GET.get("startDate"))
    endDate = reverseParseDate(request.GET.get("endDate"))
    cursor = connections['default'].cursor()
    cursor.execute(
        '''INSERT INTO users(userName, userEmail, sprintId) VALUES(%s, %s, %s)''',
        [userName, email, sprintId])
    return HttpResponseRedirect('../selectedSprint?sprintID=%s&startDate=%s&endDate=%s'%(sprintId, startDate, endDate))

def parseDate(dateToFormat):
    parsed_date = datetime.strptime(dateToFormat, "%b. %d, %Y")
    formattedDate = parsed_date.strftime("%Y-%m-%d")
    return formattedDate

def reverseParseDate(dateToFormat):
    parsed_date = datetime.strptime(dateToFormat, "%Y-%m-%d")
    formattedDate = parsed_date.strftime("%b. %d, %Y")
    return formattedDate

def toggleDisableButton(remainingPoints):
    if remainingPoints >=10:
        return None, None, None, None, None
    elif remainingPoints >= 5:
        return None, None, None, None, "disabled"
    elif remainingPoints >= 3:
        return None, None, None, "disabled", "disabled"
    elif remainingPoints >= 2:
        return None, None, "disabled", "disabled", "disabled"
    elif remainingPoints >= 1:
        return None, "disabled", "disabled", "disabled", "disabled"
    elif remainingPoints <= 0:
        return "disabled", "disabled", "disabled", "disabled", "disabled"


def addTask(request):
    sprintID = request.GET.get("sprintId")
    startDate = parseDate(request.GET.get("startDate"))
    endDate = parseDate(request.GET.get("endDate"))
    cursor = connections['default'].cursor()
    cursor.execute('''SELECT IFNULL( (SELECT SUM(points) FROM `tasks` WHERE sprintId=%s), 0)''', [sprintID])
    totalPlannedPoints = int(cursor.fetchone()[0])
    print(totalPlannedPoints)
    cursor.execute('''SELECT IFNULL( (SELECT COUNT(*) FROM `users` WHERE sprintId=%s), 0)''', [sprintID])
    totalPoints = int(cursor.fetchone()[0]) * 10
    remainingPoints = totalPoints - totalPlannedPoints
    if(remainingPoints <= 0):
        disableButton = "disabled"
    else:
        disableButton = ""
    disable1, disable2, disable3, disable4, disable5 = toggleDisableButton(remainingPoints)
    context = {'sprintID':sprintID, 'startDate': startDate, 'endDate':endDate, 'disable1':disable1, 'disable2':disable2, 'disable3':disable3,
                'disable4':disable4, 'disable5':disable5, 'disableButton': disableButton}
    return render(request, "html/addTaskForm.html", context)

def createTask(request):
    taskName = request.GET.get("taskName")
    taskDesc = request.GET.get("desc")
    taskPoints = request.GET.get("points")
    taskNeedBy = request.GET.get("needBy")
    taskPriority = request.GET.get("priority")
    sprintId = request.GET.get("sprintId")
    startDate = reverseParseDate(request.GET.get("startDate"))
    endDate = reverseParseDate(request.GET.get("endDate"))
    cursor = connections['default'].cursor()
    cursor.execute(
        '''INSERT INTO tasks(taskName, taskDesc, priority, needBy, points, sprintId) VALUES(%s, %s, %s, %s, %s, %s)''',
        [taskName, taskDesc, taskPriority, taskNeedBy, taskPoints, sprintId])
    return HttpResponseRedirect('../selectedSprint?sprintID=%s&startDate=%s&endDate=%s'%(sprintId, startDate, endDate))

def sortTasks(allTasks):
    highPriority, mediumPriority, lowPriority = [], [], []
    for task in allTasks:
        if task[3] == 3:
            highPriority.append(task)
        elif task[3] == 2:
            mediumPriority.append(task)
        elif task[3] == 1:
            lowPriority.append(task)
    highPriority = sorted(highPriority, key=itemgetter(4))
    mediumPriority = sorted(mediumPriority, key=itemgetter(4))
    lowPriority = sorted(lowPriority, key=itemgetter(4))
    return highPriority, mediumPriority, lowPriority

def updateAssignedTable(taskId, userId, sprintId, projectedDate):
    cursor = connections['default'].cursor()
    cursor.execute('''INSERT INTO assinedtable(taskId, userId, sprintId, projectedDate) VALUES(%s, %s, %s, %s)''',
    [taskId, userId, sprintId, projectedDate])
    updateAssignedTable

def dateChecker(currentDate, endDate, projectedDate, allUsers, nextCycle):
    date_format = "%m/%d/%Y"
    date_format1 = '%Y-%m-%d'
    a = datetime.strptime(currentDate, date_format1)
    b = datetime.strptime(endDate, date_format1)
    c = datetime.strptime(str(projectedDate), date_format1)
    deltaThrown = b - a
    requiredDelta = b - c
    if(deltaThrown >= requiredDelta):
        allUsers[nextCycle][4] = str(c.strftime('%Y-%m-%d'))
        return allUsers, True
    else:
        return False



def assignTasks(highPriority,  mediumPriority, lowPriority, allUsers, sprintId,  startDate, endDate):
    cycle = itertools.cycle(itertools.chain(range(0,len(allUsers)), reversed(range(0,len(allUsers)))))
    finalList = []
    if len(highPriority) == 0:
        print("Do nothing")
    else:
        for x in range(0, len(highPriority)):
            nextCycle = next(cycle)
            taskId, points, currentDate, userId = highPriority[x][0], int(highPriority[x][5]), allUsers[nextCycle][4], allUsers[nextCycle][0]
            projectedDate = datetime.strptime(currentDate, '%Y-%m-%d') + timedelta(days=int(points))
            projectedDate = projectedDate.strftime('%Y-%m-%d')
            while dateChecker(currentDate, endDate, projectedDate, allUsers, nextCycle) is False:
                nextCycle = next(cycle)
                userId, currentDate = allUsers[nextCycle][0], allUsers[nextCycle][4]
                projectedDate = datetime.strptime(currentDate, '%Y-%m-%d') + timedelta(days=int(points))
                projectedDate = projectedDate.strftime('%Y-%m-%d')
            sqlCall = updateAssignedTable(taskId, userId, int(sprintId), projectedDate)
            finalList.append([taskId, userId, int(sprintId), projectedDate, currentDate])

    if len(mediumPriority) == 0:
        print("Do nothing")
    else:
        for x in range(0, len(mediumPriority)):
            nextCycle = next(cycle)
            taskId, points, currentDate, userId = mediumPriority[x][0], int(mediumPriority[x][5]), allUsers[nextCycle][4], allUsers[nextCycle][0]
            projectedDate = datetime.strptime(currentDate, '%Y-%m-%d') + timedelta(days=int(points))
            projectedDate = projectedDate.strftime('%Y-%m-%d')
            while dateChecker(currentDate, endDate, projectedDate, allUsers, nextCycle) is False:
                nextCycle = next(cycle)
                userId, currentDate = allUsers[nextCycle][0], allUsers[nextCycle][4]
                projectedDate = datetime.strptime(currentDate, '%Y-%m-%d') + timedelta(days=int(points))
                projectedDate = projectedDate.strftime('%Y-%m-%d')
            sqlCall = updateAssignedTable(taskId, userId, int(sprintId), projectedDate)
            finalList.append([taskId, userId, int(sprintId), projectedDate, currentDate])

    if len(lowPriority) == 0:
        print("Do nothing")
    else:
        for x in range(0, len(lowPriority)):
            nextCycle = next(cycle)
            taskId, points, currentDate, userId = lowPriority[x][0], int(lowPriority[x][5]), allUsers[nextCycle][4], allUsers[nextCycle][0]
            projectedDate = datetime.strptime(currentDate, '%Y-%m-%d') + timedelta(days=int(points))
            projectedDate = projectedDate.strftime('%Y-%m-%d')
            while dateChecker(currentDate, endDate, projectedDate, allUsers, nextCycle) is False:
                nextCycle = next(cycle)
                userId, currentDate = allUsers[nextCycle][0], allUsers[nextCycle][4]
                projectedDate = datetime.strptime(currentDate, '%Y-%m-%d') + timedelta(days=int(points))
                projectedDate = projectedDate.strftime('%Y-%m-%d')
            sqlCall = updateAssignedTable(taskId, userId, int(sprintId), projectedDate)
            finalList.append([taskId, userId, int(sprintId), projectedDate, currentDate])
    return finalList

def tupleConverter(allUsers, projectedDate, nextCycle):
    tempLst = []
    tempTup = ()
    for x in allUsers:
        tempLst.append(list(x))
    tempLst[nextCycle][4] = projectedDate
    for x in tempTup:
        tempTup.append(tuple(x))
    return tempTup

def addStartDate(allUsers, startDate):
    allUsers = [[item[0], item[1], item[2], item[3], startDate] for item in allUsers]
    return allUsers


def send_email_with_ics(subject, body, startDate, endDate, receiverEmail):
    # Create an event in iCalendar format
    cal = icalendar.Calendar()
    event = icalendar.Event()

    event.add('summary', subject)
    event.add('dtstart', startDate)
    event.add('dtend', endDate)
    cal.add_component(event)

    ics_content = cal.to_ical()

    # Create an email message
    subject = "You have been assigned a new task"+subject
    body = "You have been assigned a new task which is due on" +str(endDate) + "To know more please read the below description </br>" +body
    from_email = 'schedulerultimatetest@gmail.com'  # Replace with your Gmail email address
    to_email = receiverEmail

    # Attach the ICS file
    email = EmailMessage(subject, body, from_email, [to_email])
    email.attach('meeting.ics', ics_content, 'text/calendar')

    # Send the email using Gmail SMTP
    email.send()

    return True



def prepare_calendar_invite(finalList):
    mailContent = []
    for record in finalList:
        startTime = time(9, 00, 0)
        endTime = time(17, 00, 0)
        startDate = datetime.strptime(record[4], '%Y-%m-%d').replace(hour=startTime.hour, minute=startTime.minute, second=startTime.second)
        endDate = datetime.strptime(record[3], '%Y-%m-%d').replace(hour=endTime.hour, minute=endTime.minute, second=endTime.second)
        print(endDate)
        taskId = record[0]
        cursor = connections['default'].cursor()
        cursor.execute('''SELECT * FROM `tasks` WHERE sno=%s''', [taskId])
        task = cursor.fetchall()
        subject = task[0][1]
        body = task[0][2]
        cursor.execute('''SELECT `userEmail` FROM `users` WHERE id=%s''', [record[1]])
        email = str(cursor.fetchone()[0])
        send_email_with_ics(subject, body, startDate, endDate, email)


def planSprint(request):
    sprintId = request.GET.get("sprintId")
    startDate = parseDate(request.GET.get("startDate"))
    endDate = parseDate(request.GET.get("endDate"))
    cursor = connections['default'].cursor()
    cursor.execute('''SELECT * FROM `users` WHERE sprintId=%s''', [sprintId])
    allUsers = cursor.fetchall()
    cursor.execute('''SELECT * FROM `tasks` WHERE sprintId=%s''', [sprintId])
    allTasks = cursor.fetchall()
    highPriority,  mediumPriority, lowPriority = sortTasks(allTasks)
    allUsers = addStartDate(allUsers, startDate)
    finalList = assignTasks(highPriority,  mediumPriority, lowPriority, allUsers, sprintId, startDate, endDate)
    if(finalList):
        cursor = connections['default'].cursor()
        cursor.execute('UPDATE sprints SET status="Planned" WHERE id=%s',[sprintId])
    prepare_calendar_invite(finalList)
    return HttpResponseRedirect('../sprintPage')

def deleteTask(request):
        taskId = request.GET.get("taskId")
        sprintId = request.GET.get("sprintId")
        startDate = request.GET.get("startDate")
        endDate = request.GET.get("endDate")
        cursor = connections['default'].cursor()
        cursor.execute('''SELECT `status` FROM `sprints` WHERE id=%s''', [sprintId])
        status = str(cursor.fetchone()[0])
        if status == "planned":
            message = "Tasks cant be deleted after starting the sprint"
            return HttpResponseRedirect('../selectedSprint?sprintID=%s&startDate=%s&endDate=%s&message=%s'%(sprintId, startDate, endDate, message))
        else:
            cursor.execute('''DELETE FROM `tasks` WHERE sno = %s''', [taskId])
            message = "Tasks deletion successful"
            return HttpResponseRedirect('../selectedSprint?sprintID=%s&startDate=%s&endDate=%s&message=%s'%(sprintId, startDate, endDate, message))
def deleteUser(request):
        userId = request.GET.get("userId")
        sprintId = request.GET.get("sprintId")
        startDate = request.GET.get("startDate")
        endDate = request.GET.get("endDate")
        cursor = connections['default'].cursor()
        cursor.execute('''SELECT COUNT(*) FROM `users` WHERE sprintId=%s''', [sprintId])
        pointsAvailable = int(cursor.fetchone()[0]) * 10
        cursor.execute('''SELECT SUM(points) FROM `tasks` WHERE sprintId=%s''', [sprintId])
        pointsPlanned = int(cursor.fetchone()[0])
        delta = pointsAvailable - pointsPlanned
        print(delta)
        if delta < 0:
            message1 = "Cant delete user, delete tasks before deleting user"
            return HttpResponseRedirect('../selectedSprint?sprintID=%s&startDate=%s&endDate=%s&message1=%s'%(sprintId, startDate, endDate, message1))
        else:
            cursor.execute('''DELETE FROM `users` WHERE id = %s''', [userId])
            message1 = "User deletion successful"
            return HttpResponseRedirect('../selectedSprint?sprintID=%s&startDate=%s&endDate=%s&message1=%s'%(sprintId, startDate, endDate, message1))

def plannedSprint(request):
    sprintId = request.GET.get("sprintID")
    dataTodisplay = []
    cursor = connections['default'].cursor()
    cursor.execute('''SELECT * FROM `assinedtable` WHERE sprintId=%s''', [int(sprintId)])
    assignedTasks = cursor.fetchall()
    for item in assignedTasks:
        taskId = item[1];
        userId = item[2];
        sprintId = item[3];
        projectedDate = item[4];
        cursor.execute('''SELECT `sprintName` FROM `sprints` WHERE id=%s''', [int(sprintId)])
        sprintName = str(cursor.fetchone()[0])
        cursor.execute('''SELECT * FROM `users` WHERE id=%s''', [int(userId)])
        userDetails = cursor.fetchall()
        userName = userDetails[0][1]
        userEmail = userDetails[0][2]
        cursor.execute('''SELECT * FROM `tasks` WHERE sno=%s''', [int(taskId)])
        taskDetails = cursor.fetchall()
        taskName =  taskDetails[0][1]
        taskPriority = taskDetails[0][3]
        taskNeedBy = taskDetails[0][4]
        dataTodisplay.append([taskName, taskPriority, taskNeedBy, userName, userEmail, sprintName, projectedDate])
    print(dataTodisplay)
    context = {'dataTodisplay':dataTodisplay}
    return render(request, "html/plannedSprintView.html", context)
