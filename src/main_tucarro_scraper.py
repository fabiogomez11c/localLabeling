from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
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

# accept cookies
driver.find_element(By.CLASS_NAME, 'nav-new-cookie-disclaimer__button').click()

for h in range(40):
    box = driver.find_elements(By.CLASS_NAME, 'ui-search-result__wrapper')
    next_button = driver.find_element(By.CLASS_NAME, 'andes-pagination__button--next')
    for idx, element in enumerate(box):
        print(f'Element {idx} in page {h}')
        element.click()
        # Wait for the new window or tab
        wait.until(EC.number_of_windows_to_be(2))

        window_handle = driver.window_handles[1]
        driver.switch_to.window(window_handle)
        try:
            time.sleep(4)
            driver.find_element(By.CLASS_NAME, 'ui-pdp-gallery__see-more').click()
            time.sleep(4)
        except ElementClickInterceptedException or NoSuchElementException:
            driver.close()
            driver.switch_to.window(original_window)
            continue
        picture = driver.find_element(By.CLASS_NAME, 'pswp__img')
        # go back 7 pictures
        for i in range(6):
            driver.find_element(By.CLASS_NAME, 'pswp__button--arrow--left').click()
            time.sleep(1)
        # take screenshots of the next 12 pictures
        for i in range(11):
            driver.save_screenshot('downloads/car_' + str(idx) + 'pic_' + str(i) + '.png')
            driver.find_element(By.CLASS_NAME, 'pswp__button--arrow--right').click()
            time.sleep(1)
        driver.close()
        driver.switch_to.window(original_window)
    next_button.click()
    time.sleep(5)

print('Done')
