from fastapi_utilities import repeat_every
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from events.events import load_data_test,load_data_into_supabase,load_data_cron
from dotenv import load_dotenv
import json
import logging
from supabase import create_client,Client
import os
import sentry_sdk

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    await load_data_test()
    # await load_data_into_supabase(supabase=supabase)
    # logging.info("Starting up cron JOB")
    load_data_cron(supabase=supabase)
    try:
        yield
    finally:
        logging.info("Shutting down")

sentry_sdk.init(
    dsn="https://7d07b1ccb68154f1c4ff5e92436a1b66@o4506914333458432.ingest.us.sentry.io/4506914370355200",
# formance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
    # Enable performance monitoring
    enable_tracing=True,
)
app = FastAPI(
    title="Shloka-Test API",
    lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/v1/health")
async def health_check():
    return {"status": "ok"}

# @app.get("/v1/test")
# async def test():
#     try:
#         superbase_response=supabase.table('test_table').select("*").execute()
#         return superbase_response