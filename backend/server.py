from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import asyncio

app = FastAPI()

# Enable CORS so your React frontend can access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://stockver-lavansh1306s-projects.vercel.app",
        "http://localhost:8080",
        "http://localhost:8081"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load CSV once at startup
df = pd.read_csv("data.csv")  # Ensure it has OHLC columns
df = df[['date', 'open', 'high', 'low', 'close', 'volume']]  # Keep OHLC columns
df_iterator = df.iterrows()  # Create an iterator for row-by-row access

# Shared state for the last fetched row
current_row = None

@app.get("/next_data")
async def next_data():
    """
    Returns the next row of the CSV as a JSON object.
    If the end of the CSV is reached, it will loop back to the start.
    """
    global df_iterator, current_row

    try:
        index, row = next(df_iterator)
        current_row = {
            "time": row["date"], 
            "value": float(row["open"])  # Use 'open' as the main value
        }
        print(f"Next data: {current_row}")  # Debug log
    except StopIteration:
        # Reset iterator when we reach the end
        df_iterator = df.iterrows()
        index, row = next(df_iterator)
        current_row = {
            "time": row["date"], 
            "value": float(row["open"])  # Use 'open' as the main value
        }
        print(f"Next data (reset): {current_row}")  # Debug log
    
    return current_row

@app.get("/current_data")
async def get_current_data():
    """
    Returns the last fetched row.
    Useful if frontend reconnects and wants the latest data.
    """
    return current_row or {
        "time": None, 
        "value": None
    }

@app.get("/test")
async def test():
    """
    Simple test endpoint to verify server is working.
    """
    return {"status": "Server is running!", "data_points": len(df)}
