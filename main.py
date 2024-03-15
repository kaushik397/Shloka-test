from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import datetime
import logging
from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
test_table = os.getenv("TEST_TABLE")

if not url or not key:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in the environment")

supabase: Client = create_client(supabase_url=url, supabase_key=key)

app = FastAPI(title="Nifty Shloka Test Timing platform")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def your_background_task():
    logging.info("Background task running at %s", datetime.datetime.now())
    try:
        supabase_insert = supabase.table(test_table).insert({"message": f"Background Task is running at server time {datetime.datetime.now()}"})
        supabase_insert.execute()
    except Exception as e:
        logging.error("Error inserting into Supabase: %s", str(e))

scheduler = AsyncIOScheduler()
trigger = CronTrigger(day_of_week='mon,tue,wed,thu,fri', hour='9-16', minute='0')
scheduler.add_job(your_background_task, trigger)

async def schedule_startup():
    scheduler.start()

app.add_event_handler("startup", schedule_startup)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/results")
async def get_results():
    try:
        results = supabase.table(test_table).select("*").execute()
        return results
    except Exception as e:
        logging.error("Error fetching results from Supabase: %s", str(e))
        raise HTTPException(status_code=500, detail="Internal server error")
