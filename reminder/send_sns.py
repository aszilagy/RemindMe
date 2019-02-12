import boto3
import csv
import os

client = boto3.client('sns')

def sort_reminders(filename):
    '''
    Sorts the list of reminders in reminders.txt
    '''
    daily_list = []
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            reminder = Reminder(row[0], row[1], row[2])
            daily_list.append(reminder)

        daily_list.sort(key=lambda x: x.date_time)

    with open(filename, "w+") as w_file:
        for x in daily_list:
            w_file.write(x.date_time + "," + x.class_id + "," + x.assignment_type + "\n")

def send_message(date_time, class_id, assignment_type):
    '''
    Publishes a messsage to SNS via boto3 client.
    '''
    message = "Reminder for: " + class_id + "\nDue on: " + date_time + "\nAssignment: " + assignment_type
    print("DEBUG: send_message - Sent text message:",message)
    print("DEBUG: os.environ['PHONE']:",os.environ['PHONE'])
    client.publish(PhoneNumber=os.environ['PHONE'], Message=message)

def send_message_unique(message):
    client.publish(PhoneNumber=os.environ['PHONE'], Message=message)

def daily_message(daily_list):
    '''
    Creates a message that can be sent to remind of upcomming due dates. 
    '''
    message = "Daily:\n"
    to_do_dict = {}

    for reminder in daily_list:
        if reminder.class_id in to_do_dict.keys():
            to_do_dict[reminder.class_id].append(reminder.date_time)
        else:
            to_do_dict[reminder.class_id] = [reminder.date_time]

    for key, val in to_do_dict.items():
        message += key
        for v in val:
            message += " " + v
        message += " | "
    print("DEBUG: send_message - Sent text message:\n" + message)
    client.publish(PhoneNumber=os.environ['PHONE'], Message=message)

def send_daily(send=True):
    '''
    Reads reminders.txt and supplies daily_message with a list of Reminder objects
    '''
    daily_list = []
    with open("reminders.txt") as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            reminder = Reminder(row[0], row[1], row[2])
            daily_list.append(reminder)
    if send:
        daily_message(daily_list)
    else:
        return daily_list

class Reminder:
    def __init__(self, date_time, class_id, assignment_type):
        self.date_time = date_time
        self.class_id = class_id
        self.assignment_type = assignment_type

class Birthday:
    def __init__(self, date_time, person, special_type):
        self.date_time = date_time
        self.person = person
        self.special_type = special_type

class Person:
    def __init__(self, name, phone_num=None):
        self.name = name
        self.phone_num = phone_num
