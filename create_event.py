import os.path
import tkinter as tk
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_credentials():
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

def create_event1(service, task_name, description, date, start_time, end_time):
    try:
        event = {
            'summary': task_name,
            'description': description,
            'start': {
                'dateTime': f'{date}T{start_time}:00+05:30',
                'timeZone': 'Africa/Johannesburg',
            },
            'end': {
                'dateTime': f'{date}T{end_time}:00+05:30',
                'timeZone': 'Africa/Johannesburg',
            },
            'colorId': 4,
            'recurrence': ['RRULE:FREQ=DAILY;COUNT=1']
        }

        event = service.events().insert(calendarId='primary', body=event).execute()
        print(f'Task "{task_name}" added to calendar: {event.get("htmlLink")}')
        
    except Exception as e:
        print(f"An error occurred: {e}")

def add_task(service, task_input, description_input, date_input, start_time_input, end_time_input):
    task_name = task_input.get()
    description = description_input.get()
    date = date_input.get()
    start_time = start_time_input.get()
    end_time = end_time_input.get()
    
    if task_name and description and date and start_time and end_time:
        create_event1(service, task_name, description, date, start_time, end_time)
        task_input.delete(0, tk.END)
        description_input.delete(0, tk.END)
        date_input.delete(0, tk.END)
        start_time_input.delete(0, tk.END)
        end_time_input.delete(0, tk.END)

def main():
    creds = get_credentials()
    service = build("calendar", "v3", credentials=creds)
    
    # Create the main window
    window = tk.Tk()
    window.title("To-do list")
    window.geometry('300x400')
    window.config(bg="black")

    # Entry fields for task details

    task_label = tk.Label(window, text="Task", bg='black', fg='white')
    task_label.pack(pady=5)
    task_input = tk.Entry(window, width=50,bg='black', fg='white')
    task_input.pack(pady=5)

    description_label = tk.Label(window, text="Description",bg='black', fg='white')
    description_label.pack(pady=5)
    description_input = tk.Entry(window, width=50,bg='black', fg='white')
    description_input.pack(pady=5)

    date_label = tk.Label(window, text="Date (YYYY-MM-DD)",bg='black', fg='white')
    date_label.pack(pady=5)
    date_input = tk.Entry(window, width=50,bg='black', fg='white')
    date_input.pack(pady=5)

    start_time_label = tk.Label(window, text="Start Time (HH:MM)",bg='black', fg='white')
    start_time_label.pack(pady=5)
    start_time_input = tk.Entry(window, width=50,bg='black', fg='white')
    start_time_input.pack(pady=5)

    end_time_label = tk.Label(window, text="End Time (HH:MM)",bg='black', fg='white')
    end_time_label.pack(pady=5)
    end_time_input = tk.Entry(window, width=50,bg='black', fg='white')
    end_time_input.pack(pady=5)
    

    # Enter task button
    add_button = tk.Button(window, text="Enter task", command=lambda: add_task(service, task_input, description_input, date_input, start_time_input, end_time_input),bg='black', fg='white')
    add_button.pack(pady=10)

    window.mainloop()

if __name__ == "__main__":
    main()
