from typing import Any

def normalize_ticker(ticker:str)->str:
    """统一 ticker 格式。"""
    return ticker.strip().upper()

def pad_cik(cik:int|str) ->str:
    """把 CIK 补成 10 位。"""
    return str(cik).zfill(10)

def build_ticker_mapping(mapping_json:dict) -> dict:
    """
       把 SEC 原始 ticker 映射 JSON 转成更好用的字典。

       返回格式：
       {
           "AAPL": {
               "ticker": "AAPL",
               "company_name": "Apple Inc.",
               "cik": "0000320193"
           }
       }
       """
    result = {}

    for _, item in mapping_json.items():#把 mapping_json 里面的一堆公司数据，一条一条拿出来，整理成一个新的字典 result，并且用 ticker 当键。
#原来的数据格式，不一定是你最想要的,这段代码会把它“重新整理”，后返回一个更方便后面查找的数据结构
#mapping_json.items()会把这个字典里的“键和值”一对一对拿出来。
#_, item意思就是循环出来的：第一个值我不要，第二个值我取出来叫 item.程序员通常用 _ 表示：这个值我接住了，但我不打算用它.
#循环每次拿出来大概是：("0", {"ticker": "aapl", "title": "Apple Inc.", "cik_str": 320193})，0可以代表一个公司啥的，后面是个字典
        ticker = normalize_ticker(item['ticker'])#item['ticker']：按键取字典里的值.normalize_ticker调用刚自己创建好的函数做标准化处理
        result[ticker] = {#给 result 这个字典增加一项,以 ticker 作为键，存入一条整理好的公司信息.
# 比如：result["AAPL"] = {"ticker": "AAPL"}
# 那么 result 就会变成：
# {
#     "AAPL": {"ticker": "AAPL"}
# }
            'ticker': ticker,
            'company_name': item['title'],
            'cik': pad_cik(item['cik_str'])
        }
    return result

#"ticker": ticker 是什么意思
# 左边 "ticker" 是新字典里的键。
# 右边 ticker 是变量的值。
# 比如：
# ticker = "AAPL"
# 那么：
# "ticker": ticker
# 就等于：
# "ticker": "AAPL"
# 4）"company_name": item["title"] 是什么意思
# 还是从原始 item 里取值。
# 如果：
# item["title"]
# 是：
# "Apple Inc."
# 那么这里就会变成：
# "company_name": "Apple Inc."
# 注意这里做了一件事：
# 原始数据里的字段叫 "title"
# 新整理后的字段叫 "company_name"
# 也就是改了字段名，让它更清楚。
# 5）"cik": pad_cik(item["cik_str"]) 是什么意思
# 先看里面：
# item["cik_str"]
# 假设取出来是：
# 320193
# 然后：
# pad_cik(320193)
# 这个函数可能是把 CIK 补成固定长度，比如补成 10 位字符串。
# 例如：
# pad_cik(320193)
# 变成：
# "0000320193"
# 所以最后：
# "cik": pad_cik(item["cik_str"])
# 相当于：
# "cik": "0000320193"
# 六、把这一轮循环完整代入一次给你看
# 假设现在：
# item = {
#     "ticker": "aapl",
#     "title": "Apple Inc.",
#     "cik_str": 320193
# }
# 并且：
# result = {}
# 第一步
# ticker = normalize_ticker(item["ticker"])
# 先取：
# item["ticker"]   -> "aapl"
# 再标准化：
# normalize_ticker("aapl")   -> "AAPL"
# 所以：
# ticker = "AAPL"
# 第二步
# result[ticker] = {
#     "ticker": ticker,
#     "company_name": item["title"],
#     "cik": pad_cik(item["cik_str"]),
# }
# 代入后就是：
# result["AAPL"] = {
#     "ticker": "AAPL",
#     "company_name": "Apple Inc.",
#     "cik": "0000320193",
# }
# 这一步执行后，result 变成：
# {
#     "AAPL": {
#         "ticker": "AAPL",
#         "company_name": "Apple Inc.",
#         "cik": "0000320193"
#     }
# }
def build_filing_rul(cik:str,accession_number:str,primary_document:str) ->str:#build = 构建、拼接,filing = SEC 的申报文件,url = 链接
    """
       拼接 filing 原文链接。
    """
    accession_no_dash = accession_number.replace("-", "")#调用字符串的方法 .replace()。.replace(旧内容, 新内容) 的意思是：把字符串里的某部分替换掉。
    # 意思是：把 - 替换成空字符串 "",等于把横杠删掉了
    cik_as_int = str(int(cik))  # 去掉前导 0,int之后前边的0不会被保留
    return (
        f"https://www.sec.gov/Archives/edgar/data/"#f-string，也就是格式化字符串。作用是：把变量的值塞进字符串里。
        f"{cik_as_int}/{accession_no_dash}/{primary_document}"
    )


def filing_json_to_rows(
    ticker:str,
    company_name:str,
    cik:str,
    filings_json:dict,
    target_forms:set[str] | None = None,
)->list[dict[str, Any]]:
    """
        把 recent filings JSON 解析成表格行。
    """

    rows = []

    recent = filings_json.get('filings',{}).get('recent',{})
    forms = recent.get('form',[])
    filing_datas = recent.get('filingDate',[])
    accession_numbers = recent.get('accessionNumber')
    primary_documents = recent.get('primaryDocument')

    row_count = min(
        len(forms),
        len(filing_datas),
        len(accession_numbers),
        len(primary_documents),
    )

    for i in range(row_count):
        form = forms[i]

        if target_forms is not None and form not in target_forms:
            continue

        accession_number = accession_numbers[i]
        primary_document = primary_documents[i]

        row = {
            'ticker': ticker,
            'company_name': company_name,
            'cik': cik,
            'form': form,
            'filing_date': filing_datas[i],
            'accession_number': accession_number,
            'primary_document': primary_document,
            'filings_url': build_filing_rul(
                cik = cik,
                accession_number = accession_number,
                primary_document = primary_document,
            ),
        }

        rows.append(row)

    return rows