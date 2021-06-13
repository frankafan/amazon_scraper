from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json

mobile_emulation = {
   "deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },
   "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19" }
chrome_options = Options()
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
driver = webdriver.Chrome('chromedriver.exe', options=chrome_options)

SCRAPE_DATE = False
START_YEAR = 2017
END_YEAR = 2021
for year in range(START_YEAR, END_YEAR + 1):
    for month in range(1, 13):
        while True:
            try:
                books = []
                page_num = 1
                page_end = False
                while not page_end:
                    driver.get(f'https://www.amazon.com/s?i=stripbooks&rh=n%3A5%2Cp_n_condition-type%3A1294423011%2Cp_20%3AEnglish&s=date-desc-rank&page={page_num}&Adv-Srch-Books-Submit.x=24&Adv-Srch-Books-Submit.y=12&field-datemod={month}&field-dateop=During&field-dateyear={year}&qid=1623224173&unfiltered=1&ref=aa_sbox_sort')
                    driver.implicitly_wait(1)

                    item_index = 0
                    page_scraped = False
                    while not page_scraped:
                        item = driver.find_elements(By.XPATH, '//div[@class="s-card-container s-overflow-hidden s-include-content-margin s-latency-cf-section s-card-border"]')[item_index]

                        book = {}
                        book['title'] = item.find_element(By.XPATH, './/span[@class="a-size-small a-color-base a-text-normal"]').text
                        book['author'] = item.find_elements(By.XPATH, './/span[@class="a-size-mini s-light-weight-text"]')[1].text
                        book['format'] = item.find_element(By.XPATH, './/span[@class="a-size-mini a-color-base s-medium-weight-text a-text-bold"]').text
                        book['year'] = year
                        book['month'] = month

                        if SCRAPE_DATE:
                            item.find_element(By.XPATH, './/span[@class="a-size-small a-color-base a-text-normal"]').click()

                            book_details = driver.find_elements(By.XPATH, '//div[@class="a-section a-spacing-none a-text-center rpi-attribute-value rpi-iconic-attribute-text"]/span')
                            if len(book_details) != 0:
                                for attribute in book_details:
                                    if str(year) in attribute.text:
                                        book['date'] = attribute.text
                                        driver.execute_script("window.history.go(-1)")
                                        break
                            else:
                                book['date'] = f'{month}, {year}'
                                driver.execute_script("window.history.go(-1)")
                        print(book)
                        books.append(book)

                        item_index += 1

                        if item_index == len(driver.find_elements(By.XPATH, '//div[@class="s-card-container s-overflow-hidden s-include-content-margin s-latency-cf-section s-card-border"]')):
                            page_scraped = True
                    page_num += 1
                    driver.get(
                        f'https://www.amazon.com/s?i=stripbooks&rh=n%3A5%2Cp_n_condition-type%3A1294423011%2Cp_20%3AEnglish&s=date-desc-rank&page={page_num}&Adv-Srch-Books-Submit.x=24&Adv-Srch-Books-Submit.y=12&field-datemod={month}&field-dateop=During&field-dateyear={year}&qid=1623224173&unfiltered=1&ref=aa_sbox_sort')
                    if 'Try checking your spelling or use more general terms' in driver.page_source:
                        page_end = True
                with open(f'{year}-{month}.txt', 'w') as outfile:
                    json.dump(books, outfile)
            except:
                continue
            else:
                break