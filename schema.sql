CREATE TABLE stock_data (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    open FLOAT NOT NULL,
    close FLOAT NOT NULL,
    high FLOAT,
    low FLOAT,
    volume BIGINT,
    UNIQUE(symbol, date)
);
