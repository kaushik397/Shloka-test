from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import datetime
import logging
from fastapi.exceptions import HTTPException
from supabase import create_client,Client
# import pandas as pd
from dotenv import load_dotenv
import os
load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
test_table=os.getenv("TEST_TABLE")
supabase: Client = create_client(url, key)


app = FastAPI(title="Nifty Shloka Test Timing platform")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],  # Update as needed
)

def your_background_task():
    logging.info("Background task running at %s", datetime.datetime.now())
    # message=f"Background task running at %s", datetime.datetime.now()"
    supabase_insert=supabase.table(test_table).insert({"message":"Background Task is running at server time %s".format(datetime.datetime.now())}).execute()
    print(supabase_insert)

scheduler = AsyncIOScheduler()
trigger = CronTrigger(day_of_week='mon,tue,wed,thu,fri', hour='9-16', minute='0')

scheduler.add_job(your_background_task, trigger)  # Corrected method name

async def schedule_startup():
    scheduler.start()

app.add_event_handler("startup", schedule_startup)

# Your FastAPI endpoints here (can be async or sync)
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/results")
async def get_results():
    try:
        results = supabase.table(test_table).select("*").execute()
        return results
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")