from selenium import webdriver
from selenium.webdriver.support.ui import Select
import pandas as pd
from time import sleep
import numpy as np

TABELOG_URL = "https://tabelog.com/"

STATION_NAME = "板橋駅"
KEY_WORD = "チャーハン"
DATE = "2019/5/8(水)"
NUM_OF_PPL = "3"
TIME = "19:00"

# ブラウザを開く。
driver = webdriver.Chrome()
driver.get(TABELOG_URL)

# フィールドに値をを入力して検索
driver.find_element_by_id("sa").send_keys(STATION_NAME)
driver.find_element_by_id("sk").send_keys(KEY_WORD)
#driver.find_element_by_id("").setAttribute("value", DATE)
# driver.findElement(By.id("js-global-search-date")).setAttribute("value", DATE);
# Select(driver.find_element_by_id("js-svps-header")).select_by_value(NUM_OF_PPL)
# driver.find_element_by_id("js-svt-header").send_keys(TIME)
driver.find_element_by_id("js-global-search-btn").click()

#店舗数とページ数を取得
shop_num = int(driver.find_elements_by_class_name("c-page-count__num")[2].text)
page_num = int(shop_num / 20)
if page_num == 0:
    page_num = 1

# shop情報を格納するpandasを作成
df = pd.DataFrame(columns= ['name', 'star_val','dinner_price','lunch_price','url'])

# 店の情報を取得
shop_num = 1
for page in range(page_num):
    restaurants = driver.find_elements_by_class_name("list-rst")
    for restraunt in restaurants:
        shop_name = restraunt.find_element_by_class_name("cpy-rst-name").text
        shop_url = restraunt.find_element_by_class_name("cpy-rst-name").get_attribute("href")
        is_ranked = restraunt.find_elements_by_class_name("list-rst__rating-val")
        dinner_price = restraunt.find_element_by_class_name("cpy-dinner-budget-val").text
        lunch_price = restraunt.find_element_by_class_name("cpy-lunch-budget-val").text
        shop_star_val = is_ranked[0].text if is_ranked != [] else np.nan
        df.loc[shop_num] = [shop_name,shop_star_val,dinner_price,lunch_price,shop_url]
        shop_num += 1

    if page_num != 1:
        driver.find_elements_by_class_name("c-pagination__arrow--next")[0].location_once_scrolled_into_view
        sleep(1)
        driver.find_elements_by_class_name("c-pagination__arrow--next")[0].click()

# 星の数をもとにソートする
shops = df.sort_values('star_val',ascending=False)

# csvファイルに書き出す
shops.to_csv("restaurant.csv")

# ブラウザを終了する。
driver.close()
