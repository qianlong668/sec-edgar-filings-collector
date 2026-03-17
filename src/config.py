from pathlib import Path

TICKERS = ['AAPL','MSFT','NVDA']
# TICKERS = ["AAPL", "FAKE123", "MSFT"]

HEADERS = {
    "User-Agent": "Lisen Li a3081787338@gmail.com",
    "Accept-Encoding": "gzip, deflate",
}

TICKER_MAP_UAL = 'https://www.sec.gov/files/company_tickers.json'
SUBMISSIONS_URL_TEMPLATE = 'https://data.sec.gov/submissions/CIK{cik}.json'

OUTPUT_DIR = Path('outputs')
OUTPUT_FILE = OUTPUT_DIR / 'sec_filings.csv'

REQUEST_SLEEP_SECONDS = 0.3

# TARGET_FORMS =None
TARGET_FORMS = {"10-K", "10-Q", "8-K"}

MAX_FILINGS_PER_TICKER = 20

LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "app.log"