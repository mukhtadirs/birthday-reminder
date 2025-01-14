import os
import json
from fastapi import FastAPI
from birthday_manager import BirthdayManager
import asyncio
from telegram import Bot

# Load credentials from environment variable
GOOGLE_CREDS = json.loads(os.getenv('GOOGLE_CREDENTIALS', '{}'))
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = 14265302

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Birthday Reminder API is running"}

@app.get("/check-birthdays")
async def check_birthdays():
    reminder = BirthdayManager()
    birthdays = reminder.get_all_birthdays()
    todays_birthdays = [b for b in birthdays if reminder.is_birthday_today(b['date'])]
    
    return {
        "total_birthdays": len(birthdays),
        "todays_birthdays": todays_birthdays
    }
    
@app.get("/send-notifications")
async def send_notifications():
    try:
        print("Starting birthday check for notifications...")
        reminder = BirthdayManager()
        todays_birthdays = reminder.get_todays_birthdays()
        
        if not todays_birthdays:
            print("No birthdays today, skipping notification")
            return {"success": True, "message": "No birthdays today, no notification sent"}
            
        bot = Bot(token=BOT_TOKEN)
        for birthday in todays_birthdays:
            message = f"🎉 Birthday Reminder: Today is {birthday['name']}'s birthday! 🎂"
            await bot.send_message(chat_id=CHAT_ID, text=message)
        
        return {"success": True, "message": f"Sent notifications for {len(todays_birthdays)} birthdays"}
            
    except Exception as e:
        print(f"Error in send_notifications: {e}")
        return {"success": False, "error": str(e)}