from fastapi import FastAPI
from birthday_manager import BirthdayReminder
import asyncio

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Birthday Reminder API is running"}

@app.get("/check-birthdays")
async def check_birthdays():
    reminder = BirthdayReminder()
    birthdays = reminder.get_birthdays()
    todays_birthdays = [b for b in birthdays if reminder.is_birthday_today(b['date'])]
    
    return {
        "total_birthdays": len(birthdays),
        "todays_birthdays": todays_birthdays
    }