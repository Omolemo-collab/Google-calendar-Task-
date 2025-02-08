import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_credetials():
    creds = None

    if os.path.exists(r"C:\Python\Calendar_Project 2.0\CREDENTIALS\token.json"):

        creds = Credentials.from_authorized_user_file(r"C:\Python\Calendar_Project 2.0\CREDENTIALS\token.json")
    
    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file(r"C:\Python\Calendar_Project 2.0\CREDENTIALS\credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open(r"C:\Python\Calendar_Project 2.0\CREDENTIALS\token.json", "w") as token:
            token.write(creds.to_json())

    return creds

def create_event(service):
    try:
        event = {"summary": "My Python Event", "location": "Somwhere online", "description":"This is the description", "colourID": 6, 'start':{'dateTime':'2025-02-08T09:00:00+05:30', 'timeZone':"Africa/Johannesburg"}, 'end':{'dateTime': '2025-02-08T17:00:00+05:30', 'timeZone': 'Africa/Johannesburg'},
                 "recurrence": ["RRULE:FREQ=DAILY;COUNT=3"], 'attendees':[{'email':'lpage@example.com'}, {'email':'lpage@example.com'}]}
        
        created_event = service.events().insert(calendarId = "primary", body = event).execute()

        print(f"Event Created: {created_event.get('htmlLink')}")
    
    except HttpError as error:
        print(f"An error has occured: {error}")
        
# added code
def create_event1(service,task_name, description, date, time, end_time):

    try:    
        event = {
            'summary': task_name,
            'start': {
                'dateTime': f'{date}T{time}:00+05:30',
            
                'timeZone': 'Africa/Johannesburg',
            },
            "description":f"{description}",
            "colourID": 4,
            
            'end': {
                'dateTime': f'{date}T{end_time}:00+05:30',
                'timeZone': 'Africa/Johannesburg',
            },
            "recurrence": ["RRULE:FREQ=DAILY;COUNT=1"],
        }

        event = service.events().insert(calendarId='primary', body=event).execute()
        print(f'Task "{task_name}" added to calendar: {event.get("htmlLink")}')
        
      
    except Exception as e:
        print(f"An error occurred: {e}")
# added code

def main():

    creds = get_credetials()

    service= build("calendar", "v3", credentials=creds)
    # added code
    while True:
        task = input("Enter task (or 'done' to exit): ")
        
        if task.lower().replace(" ", "") == 'done':
            break
        description = input("Enter the decription:")
        date = input("Enter the date (YYYY-MM-DD): ").replace(" ", "")
        time = input("Enter time (HH:MM): ").replace(" ", "")
        end_time = input("Enter the end time of the event (HH:MM): ").replace(" ", "")
        create_event1(service,task,description, date, time, end_time)

    #create_event1(service)

if __name__ == "__main__":
    main()

        