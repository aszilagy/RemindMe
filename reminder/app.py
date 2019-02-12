import boto3 from flask import Flask, render_template, request
import send_sns as sn

app = Flask(__name__)

@app.route('/', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/verify_login/', methods=['GET','POST'])
def verify_login():
    '''
    Verify if a user has a login or not.
    If yes, log the user into their username. If no, log the user in as guest. 
    This does NOT for security, it is simply for future account usage

    # TODO: Make this available for multiple users
    # TODO: Add a Database instead of files
    # TODO: file_to_read = username + "_reminders.txt"
    '''
    if 'username' in request.form:
        username = request.form['username']
    else:
        username = 'guest'
    file_to_read = 'reminders.txt'

    # XXX This is probably not good to sort on every login
    sn.sort_reminders(file_to_read)
    daily_list = sn.send_daily(send=False)

    #birthday_file = 'birthday_reminders.txt'
    #sn.sort_reminders(birthday_file)
    #birthday_list = sn.send_daily(send=False)

    return render_template('index.html', daily_list = daily_list)

@app.route('/remind/', methods=['GET','POST'])
def home():
    return render_template('index.html')

@app.route('/send_sns/', methods=['POST'])
def send_sns():
    date_time = request.form['dueDate']
    class_id = request.form['classId']
    assignment_type = request.form['assignmentType']
    reminder = sn.Reminder(date_time, class_id, assignment_type)
    sn.send_message(reminder.date_time, reminder.class_id, reminder.assignment_type)

    print("DEBUG: send_sns() - reminder: ", reminder)

    f = open("reminders.txt", "a")
    save_reminder = reminder.date_time + "," + reminder.class_id + "," + reminder.assignment_type + "\n"
    f.write(save_reminder)

    file_to_read = "reminders.txt"
    sn.sort_reminders(file_to_read)
    daily_list = sn.send_daily(send=False)

    return render_template('index.html', daily_list = daily_list)

@app.route('/daily_sns/', methods=['GET'])
def daily_sns():
    sn.send_daily()

if __name__ == '__main__':
    app.run(debug=True)
