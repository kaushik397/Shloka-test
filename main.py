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

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    await load_data_test()
    await load_data_into_supabase(supabase=supabase)
    load_data_cron()
    try:
        yield
    finally:
        print("Shutting down")

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