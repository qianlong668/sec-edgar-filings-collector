\# SEC EDGAR Filings Collector



一个使用 Python 编写的项目，用于采集指定上市公司的 SEC EDGAR 最新申报文件信息，筛选关键表单类型，并将结果导出为 CSV 文件。



\## 项目概述



这个项目通过 SEC EDGAR 的公开数据接口，获取指定股票代码对应公司的最新申报信息。



整体流程如下：



1\. 从 SEC 获取 ticker 和 CIK 的映射关系

2\. 根据 CIK 获取公司的 recent submissions 数据

3\. 筛选目标申报类型

4\. 限制每家公司保留的 filing 数量

5\. 将结构化结果导出为 CSV



\## 数据来源



本项目使用 SEC 官方公开数据：



\- Ticker 映射文件：`https://www.sec.gov/files/company\_tickers.json`

\- 公司申报数据：`https://data.sec.gov/submissions/CIK##########.json`



\## 项目功能



\- 采集指定 ticker 对应公司的 recent filings

\- 自动将 ticker 转换为 CIK

\- 筛选重要申报类型，例如 `10-K`、`10-Q` 和 `8-K`

\- 限制每个 ticker 的最大保留记录数

\- 将结果导出为结构化 CSV 文件

\- 使用模块化项目结构，便于维护和扩展



\## 项目结构



```text

sec\_edgar\_filings\_collector/

├─ src/

│  ├─ config.py

│  ├─ client.py

│  ├─ parser.py

│  ├─ exporter.py

│  └─ main.py

├─ outputs/

├─ requirements.txt

└─ README.md



模块职责说明



config.py：存放项目配置和常量



client.py：负责向 SEC 接口发起请求



parser.py：负责数据清洗和 JSON 解析



exporter.py：负责导出 CSV 文件



main.py：负责主流程控制



输出字段说明



导出的 CSV 包含以下字段：



ticker：股票代码



company\_name：公司名称



cik：10 位 SEC 公司标识符



form：申报表单类型



filing\_date：申报日期



accession\_number：SEC accession number



primary\_document：主要申报文件名



filing\_url：申报文件链接



如何运行

1\. 安装依赖

pip install -r requirements.txt

2\. 修改配置



打开 src/config.py，根据需要修改以下内容：



TICKERS



TARGET\_FORMS



MAX\_FILINGS\_PER\_TICKER



HEADERS\["User-Agent"]



3\. 运行程序

python src/main.py

注意事项



本项目只使用 SEC 官方公开数据



自动化访问时应使用清晰的 User-Agent



请求频率应保持合理和礼貌



适用场景



本项目可以用于：



金融研究



公司申报监控



公开披露信息跟踪



面向分析任务的结构化数据采集


---

# 中文版最终可用内容

把下面这段加到你的 **`README_CN.md`** 里，位置也是：

**“输出字段说明”后面**，**“如何运行”前面**

```md
## 示例输出

下面是导出 CSV 的示例数据：

| ticker | company_name | cik | form | filing_date | accession_number | primary_document |
|--------|--------------|-----|------|-------------|------------------|------------------|
| MSFT | MICROSOFT CORP | 0000789019 | 10-Q | 2024-10-30 | 0000950170-24-118967 | msft-20240930.htm |
| MSFT | MICROSOFT CORP | 0000789019 | 8-K | 2024-10-30 | 0000950170-24-118955 | msft-20241030.htm |
| MSFT | MICROSOFT CORP | 0000789019 | 8-K | 2024-08-21 | 0001193125-24-204403 | d846847d8k.htm |
| MSFT | MICROSOFT CORP | 0000789019 | 10-K | 2024-07-30 | 0000950170-24-087843 | msft-20240630.htm |

完整 CSV 中还包含 `filing_url` 字段。

完整结果会导出到：

```text
outputs/sec_filings.csv

---

# 二、英文版 README

这个版本你可以直接作为正式作品集 README 来用。

```md
# SEC EDGAR Filings Collector

A Python project that collects recent SEC EDGAR filings for selected public companies, filters key filing types, and exports the results to CSV.

## Project Overview

This project fetches recent filing data for selected stock tickers from the SEC EDGAR public data interface.

The workflow is:

1. Load ticker-to-CIK mapping from SEC
2. Fetch recent company submissions by CIK
3. Filter target filing forms
4. Limit the number of filings per company
5. Export the final structured data to CSV

## Data Source

This project uses public SEC EDGAR data:

- Ticker mapping: `https://www.sec.gov/files/company_tickers.json`
- Company submissions: `https://data.sec.gov/submissions/CIK##########.json`

## Features

- Collect recent filings for selected tickers
- Convert ticker to CIK automatically
- Filter important filing types such as `10-K`, `10-Q`, and `8-K`
- Limit the number of filings per ticker
- Export clean structured data to CSV
- Use a modular project structure for better maintainability

## Project Structure

```text
sec_edgar_filings_collector/
├─ src/
│  ├─ config.py
│  ├─ client.py
│  ├─ parser.py
│  ├─ exporter.py
│  └─ main.py
├─ outputs/
├─ requirements.txt
└─ README.md

Module Responsibilities

config.py: stores project settings and constants

client.py: handles HTTP requests to SEC endpoints

parser.py: handles data cleaning and JSON parsing

exporter.py: exports data to CSV

main.py: controls the main workflow

Output Fields

The exported CSV contains the following fields:

ticker: stock ticker symbol

company_name: company name from SEC mapping

cik: 10-digit SEC company identifier

form: filing form type

filing_date: filing submission date

accession_number: SEC accession number

primary_document: main filing document filename

filing_url: URL to the filing document

How to Run
1. Install dependencies
pip install -r requirements.txt
2. Update configuration

Open src/config.py and update:

TICKERS

TARGET_FORMS

MAX_FILINGS_PER_TICKER

HEADERS["User-Agent"]

3. Run the script
python src/main.py
Notes

This project uses public SEC data only.

Automated access should use a clear User-Agent.

Request frequency should remain polite and limited.

Use Cases

This project can be used for:

financial research

company filing monitoring

public disclosure tracking

structured data collection for analysis

## Example Output

Below is a sample of the exported CSV data:

| ticker | company_name | cik | form | filing_date | accession_number | primary_document |
|--------|--------------|-----|------|-------------|------------------|------------------|
| MSFT | MICROSOFT CORP | 0000789019 | 10-Q | 2024-10-30 | 0000950170-24-118967 | msft-20240930.htm |
| MSFT | MICROSOFT CORP | 0000789019 | 8-K | 2024-10-30 | 0000950170-24-118955 | msft-20241030.htm |
| MSFT | MICROSOFT CORP | 0000789019 | 8-K | 2024-08-21 | 0001193125-24-204403 | d846847d8k.htm |
| MSFT | MICROSOFT CORP | 0000789019 | 10-K | 2024-07-30 | 0000950170-24-087843 | msft-20240630.htm |

The full CSV also includes the `filing_url` field.

The full dataset is exported to:

```text
outputs/sec_filings.csv
