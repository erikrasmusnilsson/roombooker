import requests
import time
import datetime
import sys
from twilio.rest import Client

account_sid = ""
auth_token = ""

client = Client(account_sid, auth_token)

minute = 16
seconds = 2
STARTING_HOUR = 8

currentTime = time.localtime(time.time())
if currentTime.tm_min < minute:
    hour = currentTime.tm_hour
else:
    hour = currentTime.tm_hour + 1

interval = hour - STARTING_HOUR

headers = {
    "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0",
    "referer": "https://kronox.hkr.se/ajax/ajax_resursbokning.jsp?op=boka&datum=19-06-07&id=07-320A&typ=RESURSER_LOKALER&intervall=0&moment=&flik=FLIK_0000",
}

credentials = open("credentials.secret", "r")
username = credentials.readline().rstrip()
password = credentials.readline().rstrip()
credentials.close()

data = {
    "username": username,
    "password": password
}

def sendBookingRequest(session):
    rooms = ["07-320A", "07-320B",
             "07-320C", "07-320D",
             "07-320E", "07-320F",
             "07-320G", "07-320H",
             "07-320J", "07-320K",
             "07-320L", "07-320M",
             "07-320N", "07-320O"]
    today = datetime.date.today()
    todayString = today.strftime("%y-%m-%d")
    for room in rooms:
        print "Trying to book %s..." % room
        url = "https://kronox.hkr.se/ajax/ajax_resursbokning.jsp?op=boka&datum=%s&id=%s&typ=RESURSER_LOKALER&intervall=%d&moment=&flik=FLIK_0000" % (todayString, room, interval)
        response = session.get(url, headers = headers)
        if response.text == "OK":
            message = client.messages.create(
                    body="Some %s was booked for you, sir." % room,
                    from_="",
                    to=""
                )
            break
        else:
            print response.text

def book():
    #   Create a new session to stay logged in
    with requests.Session() as session:
        url = "https://kronox.hkr.se/login_do.jsp"
        response = session.get(url, headers = headers)
        status = session.post(url, data = data, headers = headers)
        if status.status_code == 200:
            sendBookingRequest(session)
        else:
            print "Login failed."

print "User: %s" % username
print "Trigger point has been set to %d:%d (interval %d)" % (hour, minute, interval)
print "Waiting..."
while True:
    localTime = time.localtime(time.time())
    if localTime.tm_hour == hour and localTime.tm_min == minute and localTime.tm_sec == seconds:
        book()
        sys.exit()
