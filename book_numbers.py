from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

mobile_emulation = {
   "deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },
   "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19" }
chrome_options = Options()
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
driver = webdriver.Chrome('chromedriver.exe', options=chrome_options)

data = []

month_data = {}
while not month_data:
    driver.get(
        'https://www.amazon.com/s?i=stripbooks&rh=n%3A5%2Cp_n_condition-type%3A1294423011%2Cp_20%3AEnglish&s=daterank&Adv-Srch-Books-Submit.x=19&Adv-Srch-Books-Submit.y=18&field-datemod=3&field-dateop=During&field-dateyear=2021&unfiltered=1&ref=sr_adv_b')
    elements = driver.find_elements(By.XPATH, './/span[@class="a-size-small a-color-base"]')
    for i in range(len(elements)):
        if elements[i].text == 'Filters':
            elements[i].click()
            elements = driver.find_elements(By.XPATH, './/span[@class="a-size-small a-color-base"]')
            break
    for i in range(len(elements)):
        if elements[i].text.split(' ')[0] == 'Show':
            month_data['result1'] = elements[i].text.split(' ')[1]
            elements = driver.find_elements(By.XPATH, './/span[@class="a-size-small a-color-base"]')
            break
    for i in range(len(elements)):
        if elements[i].text == 'English':
            # driver.execute_script("arguments[0].scrollIntoView();", elements[i])
            driver.execute_script("arguments[0].scrollIntoView();", driver.find_elements(By.XPATH, './/span[@class="a-size-medium a-color-base"]')[-5])
            elements[i].click()
            elements = driver.find_elements(By.XPATH, './/span[@class="a-size-small a-color-base"]')
            break
    for i in range(len(elements)):
        if elements[i].text.split(' ')[0] == 'Show':
            month_data['result2'] = elements[i].text.split(' ')[1]
            elements = driver.find_elements(By.XPATH, './/span[@class="a-size-small a-color-base"]')
            break
data.append(month_data)
print(data)