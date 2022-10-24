from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import time

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 10)
driver.get('https://carros.tucarro.com.co/#unapplied_filter_id%3DMODEL%26unapplied_filter_name%3DModelo%26unapplied_value_id%3D68141%26unapplied_value_name%3DCaptiva%26unapplied_autoselect%3Dfalse')
# Store the ID of the original window
original_window = driver.current_window_handle
# Check we don't have other windows open already
assert len(driver.window_handles) == 1

# Finding the search box
box = driver.find_elements(By.CLASS_NAME, 'ui-search-result__wrapper')

for idx, element in enumerate(box):
    element.click()
    # Wait for the new window or tab
    wait.until(EC.number_of_windows_to_be(2))

    window_handle = driver.window_handles[1]
    driver.switch_to.window(window_handle)
    time.sleep(4)
    driver.find_element(By.CLASS_NAME, 'ui-pdp-gallery__see-more').click()
    time.sleep(4)
    picture = driver.find_element(By.CLASS_NAME, 'pswp__img')
    src = picture.get_attribute('src')
    for i in range(6):
        driver.find_element(By.CLASS_NAME, 'pswp__button--arrow--left').click()
        time.sleep(1)
    # download the image
    for i in range(11):
        driver.save_screenshot('car_' + str(idx) + 'pic_' + str(i) + '.png')
        driver.find_element(By.CLASS_NAME, 'pswp__button--arrow--right').click()
        time.sleep(1)
    print('Done')
# box.send_keys('front of car tucarro')
# box.send_keys(Keys.ENTER)
#
# driver.find_element('xpath', '//*[@id="hdtb-msb"]/div[1]/div/div[2]/a').click()


# #Will keep scrolling down the webpage until it cannot scroll no more
# last_height = driver.execute_script('return document.body.scrollHeight')
# while True:
#     driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
#     time.sleep(2)
#     new_height = driver.execute_script('return document.body.scrollHeight')
#     try:
#         driver.find_element('xpath', '//*[@id="islmp"]/div/div/div/div/div[5]/input').click()
#         time.sleep(2)
#     except:
#         pass
#     if new_height == last_height:
#         break
#     last_height = new_height


# for i in range(1, 10):
#     try:
#         element = driver.find_element('xpath', '//*[@id="islrg"]/div[1]/div['+str(i)+']/a[1]/div[1]/img')
#         time.sleep(3)
#         element.screenshot('giraffe ('+str(i)+').png')
#     except:
#         pass

print('Done')