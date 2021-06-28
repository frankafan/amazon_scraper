from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json

mobile_emulation = {
    "deviceMetrics": {"width": 640, "height": 1080, "pixelRatio": 1.0},
    "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"}
chrome_options = Options()
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
driver = webdriver.Chrome('chromedriver.exe', options=chrome_options)


def find_filter_items(driver=driver):
    return driver.find_elements(By.XPATH, './/span[@class="a-size-small a-color-base"]')


def find_num_results(elements):
    for i in range(len(elements)):
        if elements[i].text.split(' ')[0] == 'Show':
            return elements[i].text.split(' ')[1]


def click_filter_button(elements):
    for i in range(len(elements)):
        if elements[i].text == 'Filters':
            elements[i].click()
            elements = find_filter_items(driver)


subcategories = [
    'Business Technology',
    'Certification',
    'Computer Science',
    'Databases & Big Data',
    'Digital Audio, Video & Photography',
    'Games & Strategy Guides',
    'Graphics & Design',
    'Hardware & DIY',
    'History & Culture',
    'Internet & Social Media',
    'Mobile Phones, Tablets & E-Readers',
    'Networking & Cloud Computing',
    'Operating Systems',
    'Programming',
    'Programming Languages',
    'Security & Encryption',
    'Software',
    'Web Development & Design',
]

data = []

START_YEAR = 2017
END_YEAR = 2021
CURRENT_DATE = '2021-06'
for year in range(START_YEAR, END_YEAR + 1):
    for month in range(1, 13):
        print(f'Year: {year}')
        print(f'Month: {month}')

        while not (int(CURRENT_DATE.split('-')[0]) < year and int(CURRENT_DATE.split('-')[1]) < month):
            try:
                month_data = {}
                while not ('All' in month_data.keys() and month_data['All'] != None):
                    driver.get(
                        f'https://www.amazon.com/s?i=stripbooks&rh=n%3A5%2Cp_n_condition-type%3A1294423011%2Cp_20%3AEnglish&s=date-desc-rank&Adv-Srch-Books-Submit.x=24&Adv-Srch-Books-Submit.y=12&field-datemod={month}&field-dateop=During&field-dateyear={year}&qid=1623224173&unfiltered=1&ref=aa_sbox_sort')
                    elements = find_filter_items(driver)
                    click_filter_button(elements)
                    elements = find_filter_items(driver)
                    month_data['All'] = find_num_results(elements)
                print(f'All: {month_data["All"]}')

                available_subcategories = []
                while len(available_subcategories) == 0:
                    driver.get(
                        f'https://www.amazon.com/s?i=stripbooks&rh=n%3A5%2Cp_n_condition-type%3A1294423011%2Cp_20%3AEnglish&s=date-desc-rank&Adv-Srch-Books-Submit.x=24&Adv-Srch-Books-Submit.y=12&field-datemod={month}&field-dateop=During&field-dateyear={year}&qid=1623224173&unfiltered=1&ref=aa_sbox_sort')
                    elements = find_filter_items(driver)
                    click_filter_button(elements)
                    elements = find_filter_items(driver)
                    for i in range(len(elements)):
                        if elements[i].text in subcategories:
                            available_subcategories.append(elements[i].text)
                for subcategory in available_subcategories:
                    while not (subcategory in month_data.keys()):
                        driver.get(
                            f'https://www.amazon.com/s?i=stripbooks&rh=n%3A5%2Cp_n_condition-type%3A1294423011%2Cp_20%3AEnglish&s=date-desc-rank&Adv-Srch-Books-Submit.x=24&Adv-Srch-Books-Submit.y=12&field-datemod={month}&field-dateop=During&field-dateyear={year}&qid=1623224173&unfiltered=1&ref=aa_sbox_sort')
                        elements = find_filter_items(driver)
                        click_filter_button(elements)
                        elements = find_filter_items(driver)
                        for i in range(len(elements)):
                            category_index = 0
                            if elements[i].text == 'Computers & Technology':
                                category_index = i
                            if elements[i].text == subcategory:
                                driver.execute_script("arguments[0].scrollIntoView(true);", elements[category_index])
                                elements[i].click()
                                driver.refresh()
                                elements = find_filter_items(driver)
                                break
                        click_filter_button(elements)
                        month_data[subcategory] = find_num_results(elements)
                        available_subcategories.pop(available_subcategories.index(subcategory))
                        print(f'{subcategory}: {month_data[subcategory]}')
                month_data['year'] = year
                month_data['month'] = month
                data.append(month_data)
            except Exception as e:
                print(e)
                continue
            else:
                print(month_data)
                break
print(data)
with open(f'num_results.txt', 'w') as outfile:
    json.dump(data, outfile)
