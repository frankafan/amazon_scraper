from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

mobile_emulation = {
   "deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },
   "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19" }
chrome_options = Options()
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
driver = webdriver.Chrome('chromedriver.exe', options=chrome_options)


def find_filter_items(driver=driver):
    return driver.find_elements(By.XPATH, './/span[@class="a-size-small a-color-base"]')

data = []

START_YEAR = 2017
END_YEAR = 2021
for year in range(START_YEAR, END_YEAR + 1):
    for month in range(1, 13):
        print(f'Year: {year}')
        print(f'Month: {month}')

        month_data = {}
        while not month_data:
            driver.get(
                f'https://www.amazon.com/s?i=stripbooks&rh=n%3A5%2Cp_n_condition-type%3A1294423011%2Cp_20%3AEnglish&s=date-desc-rank&Adv-Srch-Books-Submit.x=24&Adv-Srch-Books-Submit.y=12&field-datemod={month}&field-dateop=During&field-dateyear={year}&qid=1623224173&unfiltered=1&ref=aa_sbox_sort')
            elements = find_filter_items(driver)
            for i in range(len(elements)):
                if elements[i].text == 'Filters':
                    elements[i].click()
                    elements = find_filter_items(driver)
                    break
            for i in range(len(elements)):
                if elements[i].text.split(' ')[0] == 'Show':
                    month_data['result1'] = elements[i].text.split(' ')[1]
                    elements = find_filter_items(driver)
                    break
            for i in range(len(elements)):
                if elements[i].text == 'English':
                    # driver.execute_script("arguments[0].scrollIntoView();", elements[i])
                    driver.execute_script("arguments[0].scrollIntoView();", driver.find_elements(By.XPATH, './/span[@class="a-size-medium a-color-base"]')[-5])
                    elements[i].click()
                    elements = find_filter_items(driver)
                    break
            for i in range(len(elements)):
                if elements[i].text.split(' ')[0] == 'Show':
                    month_data['result2'] = elements[i].text.split(' ')[1]
                    elements = find_filter_items(driver)
                    break
        data.append(month_data)
        print(month_data)
print(data)