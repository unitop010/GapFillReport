from fastapi import FastAPI
from gap_analysis import calculate_gaps, generate_gap_fill_report

app = FastAPI()

@app.get("/gap_fill/")
def gap_fill(symbol: str):
    data = calculate_gaps("sqlite:///stock_data.db", symbol)
    report = generate_gap_fill_report(data)
    return report
