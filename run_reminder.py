import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, date
from telegram import Bot
import asyncio

# Configuration
BOT_TOKEN = "7705146266:AAE7ccphcdXt7qxbPDjm29UtmER8ZjlfumU"  # Your Telegram bot token
CHAT_ID = 14265302  # Your chat ID
SPREADSHEET_ID = "1uD2_mOmtcNsu-dREu7icgIKCGKg3FWw2QmivHtt8ZK0"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

class BirthdayReminder:
    def __init__(self):
        self.RANGE_NAME = 'Sheet1!A:C'
        
    def get_service(self):
        """Create and return Google Sheets service"""
        creds = service_account.Credentials.from_service_account_file(
            'credentials.json', scopes=SCOPES)
        return build('sheets', 'v4', credentials=creds)
    
    def get_birthdays(self):
        """Fetch all birthdays from Google Sheet"""
        try:
            service = self.get_service()
            sheet = service.spreadsheets()
            result = sheet.values().get(
                spreadsheetId=SPREADSHEET_ID,
                range=self.RANGE_NAME
            ).execute()
            
            values = result.get('values', [])
            if not values:
                return []
            
            birthdays = []
            for row in values[1:]:  # Skip header row
                if len(row) >= 2:
                    birthdays.append({
                        'name': row[0],
                        'date': row[1]
                    })
            return birthdays
            
        except Exception as e:
            print(f'Error fetching birthdays: {e}')
            return []

    def is_birthday_today(self, birthday_date):
        """Check if given date matches today"""
        try:
            birth_date = datetime.strptime(birthday_date, '%d-%m-%Y')
            today = date.today()
            return (birth_date.month == today.month and 
                   birth_date.day == today.day)
        except Exception as e:
            print(f'Error checking date: {e}')
            return False

async def send_reminders():
    try:
        print(f"Starting birthday check at {datetime.now()}")
        
        reminder = BirthdayReminder()
        bot = Bot(token=BOT_TOKEN)
        
        # Get all birthdays
        birthdays = reminder.get_birthdays()
        
        # Check for today's birthdays
        todays_birthdays = [b for b in birthdays 
                          if reminder.is_birthday_today(b['date'])]
        
        if todays_birthdays:
            for birthday in todays_birthdays:
                message = f"🎉 Today is {birthday['name']}'s birthday! 🎂"
                await bot.send_message(chat_id=CHAT_ID, text=message)
                print(f"Sent reminder for {birthday['name']}")
        else:
            print("No birthdays today!")
            
    except Exception as e:
        print(f"Error in send_reminders: {e}")

def main():
    """Main function to run the reminder"""
    asyncio.run(send_reminders())

if __name__ == "__main__":
    main()