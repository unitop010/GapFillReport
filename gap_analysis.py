import pandas as pd
from sqlalchemy import create_engine

def calculate_gaps(db_uri, symbol):
    # Connect to the database
    engine = create_engine(db_uri)
    query = f"""
    SELECT symbol, date, open, close, LAG(close) OVER (PARTITION BY symbol ORDER BY date) AS prev_close
    FROM stock_data
    WHERE symbol = '{symbol}'
    """
    data = pd.read_sql(query, engine)

    # Calculate gaps
    data['gap_up'] = (data['open'] > data['prev_close'])
    data['gap_down'] = (data['open'] < data['prev_close'])
    data['gap_filled'] = (
        (data['gap_up'] & (data['close'] <= data['prev_close'])) |
        (data['gap_down'] & (data['close'] >= data['prev_close']))
    )
    return data.dropna()

def generate_gap_fill_report(data):
    # Insights for gap up
    total_gap_up = len(data[data['gap_up']])
    gap_up_filled = len(data[(data['gap_up']) & (data['gap_filled'])])
    gap_up_not_filled = total_gap_up - gap_up_filled

    # Insights for gap down
    total_gap_down = len(data[data['gap_down']])
    gap_down_filled = len(data[(data['gap_down']) & (data['gap_filled'])])
    gap_down_not_filled = total_gap_down - gap_down_filled

    # Calculate percentages
    gap_up_filled_percentage = (gap_up_filled / total_gap_up) * 100 if total_gap_up > 0 else 0
    gap_up_not_filled_percentage = 100 - gap_up_filled_percentage

    gap_down_filled_percentage = (gap_down_filled / total_gap_down) * 100 if total_gap_down > 0 else 0
    gap_down_not_filled_percentage = 100 - gap_down_filled_percentage

    # Compile insights
    insights = {
        "gap_up": {
            "frequency": total_gap_up,
            "percentage": f"{(total_gap_up / len(data)) * 100:.2f}%" if len(data) > 0 else "0%"
        },
        "gap_up_filled": {
            "frequency": gap_up_filled,
            "percentage": f"{gap_up_filled_percentage:.2f}%"
        },
        "gap_up_not_filled": {
            "frequency": gap_up_not_filled,
            "percentage": f"{gap_up_not_filled_percentage:.2f}%"
        },
        "gap_down": {
            "frequency": total_gap_down,
            "percentage": f"{(total_gap_down / len(data)) * 100:.2f}%" if len(data) > 0 else "0%"
        },
        "gap_down_filled": {
            "frequency": gap_down_filled,
            "percentage": f"{gap_down_filled_percentage:.2f}%"
        },
        "gap_down_not_filled": {
            "frequency": gap_down_not_filled,
            "percentage": f"{gap_down_not_filled_percentage:.2f}%"
        }
    }

    return insights

if __name__ == "__main__":
    # Connect to the database and fetch data for a symbol
    data = calculate_gaps("sqlite:///stock_data.db", "SPY")
    
    # Generate insights
    insights = generate_gap_fill_report(data)
    for category, stats in insights.items():
        print(f"{category}: {stats}")
