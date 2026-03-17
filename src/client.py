import  requests

from config import HEADERS,TICKER_MAP_UAL,SUBMISSIONS_URL_TEMPLATE

def get_json(url:str) -> dict:#请求 JSON 数据。
    print("请求URL：", url)
    response = requests.get(url, headers=HEADERS,timeout=30)
    response.raise_for_status()
    return response.json()

def fetch_ticker_mapping_json() -> dict:#获取 SEC ticker 映射表原始 JSON
    return get_json(TICKER_MAP_UAL)

def fetch_company_submissions_json(cik:str) -> dict:#根据 10 位 CIK 获取公司 submissions JSON
    url = SUBMISSIONS_URL_TEMPLATE.format(cik=cik)
    return get_json(url)