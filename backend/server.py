from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import asyncio
import httpx

app = FastAPI()

# Enable CORS so your React frontend can access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://stockver-lavansh1306s-projects.vercel.app",
        "https://stockver.vercel.app",
        "https://stock-mg294db-lavansh1306s-projects.vercel.app",
        "https://stock-verse-lavansh1306s-projects.vercel.app"
        "http://localhost:8080",
        "http://localhost:8081",
        "http://localhost:3000",
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "HEAD"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600
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

from fastapi import HTTPException
from fastapi.responses import JSONResponse

@app.get("/proxy/yahoo/{symbol}")
async def proxy_yahoo_finance(symbol: str):
    """
    Proxy endpoint for Yahoo Finance data
    """
    try:
        # Extract symbol and parameters
        actual_symbol = symbol
        params = {
            "interval": "1m",
            "range": "1d"
        }
        
        if "?range=" in symbol:
            actual_symbol, range_val = symbol.split("?range=")
            params["range"] = range_val
            
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{actual_symbol}"
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Accept": "application/json"
            }
            
            response = await client.get(url, headers=headers, params=params)
            
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Failed to fetch data from Yahoo Finance")
                
            return JSONResponse(
                content=response.json(),
                headers={
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, OPTIONS",
                    "Access-Control-Allow-Headers": "*"
                }
            )
            
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Request to Yahoo Finance timed out")
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Failed to fetch data: {str(e)}")
    except Exception as e:
        print(f"Error in proxy: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
