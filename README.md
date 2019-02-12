# ReminderApp (v0.1)
This app utilzes boto3 and interacts with AWS SNS to read a file of reminders and send daily text messages. Included in this application is a basic web interface using Flask.

## Takeaways
* This app requires understanding of how AWS SNS works, along with how to interact with it via boto3. You must have an AWS account and understand how to set up SNS and boto3.
* Flask is used to create a (minimal) web interface. Understanding is required of how flask interacts with templates and HTTP Methods.
* OS Environment variables are used to keep my Phone number away from public view so that this repository may be made public. A config file may eventually be added, but knowledge of how to initialize an os enrivonment variable is currently required.

**Note:** This is a personal application not designed for commercial or widespread use. The code needs improvement and this is an initial draft of the application.
