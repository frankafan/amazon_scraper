from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

mobile_emulation = {
   "deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },
   "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19" }
chrome_options = Options()
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
driver = webdriver.Chrome('chromedriver.exe', options=chrome_options)

START_YEAR = 2017
END_YEAR = 2021


# for year in range(START_YEAR, END_YEAR + 1):
#     for month in range(1, 13):
#         driver.get(f'https://www.amazon.com/s?i=stripbooks&rh=n%3A5%2Cp_n_condition-type%3A1294423011%2Cp_20%3AEnglish&s=daterank&Adv-Srch-Books-Submit.x=24&Adv-Srch-Books-Submit.y=12&field-datemod={month}&field-dateop=During&field-dateyear={year}&unfiltered=1&ref=sr_adv_b')
#
driver.get('https://www.amazon.com/s?i=stripbooks&rh=n%3A5%2Cp_n_condition-type%3A1294423011%2Cp_20%3AEnglish&s=daterank&Adv-Srch-Books-Submit.x=24&Adv-Srch-Books-Submit.y=12&field-datemod=1&field-dateop=During&field-dateyear=2017&unfiltered=1&ref=sr_adv_b')

items = driver.find_elements(By.XPATH, '//div[@class="s-card-container s-overflow-hidden s-include-content-margin s-latency-cf-section s-card-border"]')
for item in items:
    book = {}
    book['title'] = item.find_element(By.XPATH, './/span[@class="a-size-small a-color-base a-text-normal"]').text
    book['author'] = item.find_elements(By.XPATH, './/span[@class="a-size-mini s-light-weight-text"]')[1].text
    book['format'] = item.find_element(By.XPATH, './/span[@class="a-size-mini a-color-base s-medium-weight-text a-text-bold"]').text
    print(book)