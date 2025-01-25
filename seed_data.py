import requests
import pandas as pd
from sqlalchemy import create_engine

def fetch_stock_data(symbol, api_key):
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/2024-11-01/2024-12-31"
    params = {"adjusted": "true", "sort": "asc", "apiKey": api_key}
    response = requests.get(url, params=params)
    
    # Check for a successful API response
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.json().get('error', 'Unknown error')}")

    data = response.json().get("results", [])
    if not data:
        raise Exception("No data returned by the API.")
    
    # Convert API response to DataFrame
    df = pd.DataFrame(data)

    # Rename and transform columns to match the database schema
    df = df.rename(columns={
        "o": "open",
        "c": "close",
        "h": "high",
        "l": "low",
        "v": "volume",
        "t": "date"  # Convert timestamp to date
    })

    # Convert timestamp to a readable date format
    df["date"] = pd.to_datetime(df["date"], unit="ms").dt.date

    # Add the symbol column
    df["symbol"] = symbol

    # Select only the relevant columns
    df = df[["symbol", "date", "open", "close", "high", "low", "volume"]]

    return df

def seed_database(symbol, api_key, db_uri):
    engine = create_engine(db_uri)
    data = fetch_stock_data(symbol, api_key)

    # Check if the table exists and create it if not
    data.to_sql('stock_data', engine, if_exists='append', index=False)

    print(f"Data for {symbol} successfully added to the database.")

# Replace with your API key and database URI
seed_database("SQ", "T6SHPRVXIASIISDSABOEdfuI4GoCBph6", "sqlite:///stock_data.db")
