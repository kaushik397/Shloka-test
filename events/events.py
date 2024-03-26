#load data into supabase every 15 mins
from fastapi_utilities import repeat_every,repeat_at
import datetime
import logging
from dotenv import load_dotenv
import os
import sentry_sdk
from sentry_sdk.crons import monitor

test_table = os.getenv("TEST_TABLE")
@repeat_every(seconds=900)
async def load_data_into_supabase(supabase):
    logging.info("Data to be loaded into supabase or run compitition")
    logging.info("Background task running at %s", datetime.datetime.now())
    try:
        supabase_insert=supabase.table('test_table').insert({"message": f"Background Task is running at server time {datetime.datetime.now()}"}).execute()
        return supabase_insert
    except Exception as e:
        print("Error is:",e)

@repeat_every(seconds=10)
@monitor(monitor_slug='nifty-stf')
async def load_data_test():
    """Load data into supabase every 15 mins"""
    logging.info("test running")

@repeat_at(cron="* 4-10 * * 1-5")
@monitor(monitor_slug='nifty-stf')
async def load_data_cron(supabase):
    """Load data into supabase every 15 mins"""
    logging.info("testing CRON JOB")
    try:
        supabase_insert=supabase.table('test_table').insert({"message": f"Background Task CRON JOB AT: {datetime.datetime.now()}"}).execute()
        return supabase_insert
    except Exception as e:
        print("Error is:",e)