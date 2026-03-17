import time
from config import (
    LOG_FILE,
    MAX_FILINGS_PER_TICKER,
    OUTPUT_FILE,
    REQUEST_SLEEP_SECONDS,
    TARGET_FORMS,
    TICKERS,
)
from client import fetch_company_submissions_json,fetch_ticker_mapping_json
from exporter import save_rows_to_csv
from parser import build_ticker_mapping,filing_json_to_rows,normalize_ticker
from logger import setup_logger

def main():
    logger = setup_logger()

    logger.info("Step 1: 获取 ticker 映射表...")
    mapping_json = fetch_ticker_mapping_json()
    ticker_mapping = build_ticker_mapping(mapping_json)
    logger.info(f"映射表加载完成，共 {len(ticker_mapping)} 个 ticker。")

    all_rows =[]

    successful_tickers = []
    failed_tickers = []
    skipped_tickers = []

    print('Step 2：逐个ticker获取filings...')
    for raw_ticker in TICKERS:
        ticker = normalize_ticker(raw_ticker)

        if ticker not in ticker_mapping:
            logger.warning(f"[跳过] 未找到 ticker: {ticker}")
            skipped_tickers.append(ticker)
            continue

        company_info = ticker_mapping[ticker]
        conpany_name = company_info['company_name']
        cik = company_info['cik']
# 这里是一个字典套字典的东西，大概如这种：ticker_mapping = {
#     "AAPL": {
#         "ticker": "AAPL",
#         "company_name": "Apple Inc.",
#         "cik": "0000320193"
#     },
#     "MSFT": {
#         "ticker": "MSFT",
#         "company_name": "Microsoft Corp",
#         "cik": "0000789019"
#     }
# }
        logger.info(f"正在处理: {ticker} | {conpany_name} | CIK={cik}")
        try:
            filing_json = fetch_company_submissions_json(cik)
            rows = filing_json_to_rows(
                ticker= ticker,
                company_name = conpany_name,
                cik =cik,
                filings_json = filing_json,
                target_forms = TARGET_FORMS,
            )

            rows = rows[:MAX_FILINGS_PER_TICKER]

            logger.info(f"{ticker} 获取到 {len(rows)} 条 recent filings")

            all_rows.extend(rows)
            successful_tickers.append(ticker)


        except Exception as e:
            logger.error(f"{ticker} 处理失败: {e}")
            failed_tickers.append(ticker)
            continue

        time.sleep(REQUEST_SLEEP_SECONDS)

    logger.info("Step 3: 保存 CSV...")
    save_rows_to_csv(all_rows,OUTPUT_FILE)


    logger.info(f"完成，已保存到: {OUTPUT_FILE}")
    logger.info(f"总行数: {len(all_rows)}")

    logger.info("===== Run Summary =====")
    logger.info(f"Successful tickers: {len(successful_tickers)}")
    logger.info(f"Failed tickers: {len(failed_tickers)}")
    logger.info(f"Skipped tickers: {len(skipped_tickers)}")
    logger.info(f"Total rows exported: {len(all_rows)}")
    logger.info(f"CSV file: {OUTPUT_FILE}")
    logger.info(f"Log file: {LOG_FILE}")

    if successful_tickers:
        logger.info(f"Successful ticker list: {successful_tickers}")

    if failed_tickers:
        logger.info(f"Failed ticker list: {failed_tickers}")

    if skipped_tickers:
        logger.info(f"Skipped ticker list: {skipped_tickers}")

    if all_rows:
        logger.info("前 5 行预览：")
        for row in all_rows[:5]:
            print(row)

if __name__ == '__main__':
    main()