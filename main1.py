from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import sys
import time
import requests
from bs4 import BeautifulSoup
def get_currency_symbols():
    url = "https://www.11meigui.com/tools/currency"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        currency_table = soup.find('table', {'class': 'break'})

        currency_dict = {}
        for row in currency_table.find_all('tr')[1:]:  # Skip the header row
            columns = row.find_all('td')
            if len(columns) == 6:
                currency_symbol = columns[4].text.strip()
                currency_abbreviation = columns[1].text.strip()
                currency_dict[currency_symbol] = currency_abbreviation
        return currency_dict

    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None
def fetch_forex_rate(date, currency_code):
    chrome_options = Options()

    chrome_options.add_argument('--no-sandbox')
    driver_path = 'shiyou\chromedriver-win32\chromedriver'
    # 初始化Chrome浏览器
    driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
    
    try:
        driver.get('https://www.boc.cn/sourcedb/whpj/')

        # 等待页面加载
        time.sleep(2)

        # 选择查询日期
        year = date[:4]
        month = date[4:6]
        day = date[6:]

        formatted_date_str = f"{year}-{month}-{day}"
        date_input = driver.find_element(by=By.NAME, value="erectDate")
        date_input.clear()
        date_input.send_keys(formatted_date_str)

        date_input2 = driver.find_element(by=By.NAME, value="nothing")
        date_input2.clear()
        date_input2.send_keys(formatted_date_str)
        currency_symbols_dict = get_currency_symbols()


        # 选择货币代码
        currency_symbol = currency_symbols_dict[currency_code]
        currency_input = driver.find_element(by=By.NAME, value="pjname")
        currency_select = Select(currency_input)
        currency_select.select_by_value(currency_symbol)


        # 提交查询
        search_button = driver.find_element(by=By.XPATH, value='//input[@class="search_btn" and @onclick="executeSearch()"]')
        search_button.click()

        # 等待查询结果加载
        time.sleep(2)

        # 获取现汇卖出价
        forex_rate = driver.find_element(by=By.XPATH, value='//tr[@class="odd"]/td[4]').text

        print(forex_rate)

        # 将结果写入result.txt文件
        with open('result.txt', 'w') as result_file:
            result_file.write(forex_rate)

    except Exception as e:
        print(f"发生异常: {e}")
    finally:
        # 关闭浏览器
        driver.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main1.py <date> <currency_code>")
        sys.exit(1)

    date = sys.argv[1]
    currency_code = sys.argv[2]

    fetch_forex_rate(date, currency_code)
    
