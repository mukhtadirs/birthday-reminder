import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, date

class BirthdayManager:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        self.SPREADSHEET_ID = '1uD2_mOmtcNsu-dREu7icgIKCGKg3FWw2QmivHtt8ZK0'
        self.RANGE_NAME = 'Sheet1!A:C'
        
    def get_service(self):
        """Create and return Google Sheets service"""
        credentials_dict = json.loads(os.getenv('GOOGLE_CREDENTIALS', '{}'))
        creds = service_account.Credentials.from_info(
        credentials_dict, 
        scopes=self.SCOPES
    )
        return build('sheets', 'v4', credentials=creds)
    
    def get_all_birthdays(self):
        """Fetch all birthdays from Google Sheet"""
        try:
            service = self.get_service()
            sheet = service.spreadsheets()
            result = sheet.values().get(
                spreadsheetId=self.SPREADSHEET_ID,
                range=self.RANGE_NAME
            ).execute()
            
            values = result.get('values', [])
            if not values:
                print('No data found in sheet')
                return []
            
            # Skip header row and format data
            birthdays = []
            for row in values[1:]:  # Skip header row
                if len(row) >= 2:  # Ensure row has name and date
                    birthdays.append({
                        'name': row[0],
                        'date': row[1]
                    })
            return birthdays
            
        except Exception as e:
            print(f'Error fetching birthdays: {e}')
            return []
    
    def is_birthday_today(self, birthday_date):
        """Check if given date matches today (ignoring year)"""
        try:
            # Convert birthday string (DD-MM-YYYY) to date object
            birth_date = datetime.strptime(birthday_date, '%d-%m-%Y')
            today = date.today()
            
            # Compare month and day only
            return (birth_date.month == today.month and 
                   birth_date.day == today.day)
        except Exception as e:
            print(f'Error checking date: {e}')
            return False
    
    def get_todays_birthdays(self):
        """Get list of people who have birthdays today"""
        all_birthdays = self.get_all_birthdays()
        return [birthday for birthday in all_birthdays 
                if self.is_birthday_today(birthday['date'])]

# Test the class
if __name__ == '__main__':
    manager = BirthdayManager()
    print("\nFetching all birthdays:")
    all_birthdays = manager.get_all_birthdays()
    print(all_birthdays)
    
    print("\nChecking today's birthdays:")
    todays_birthdays = manager.get_todays_birthdays()
    print(todays_birthdays)