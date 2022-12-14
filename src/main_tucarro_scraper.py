# from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire import webdriver  # Import from seleniumwire
import urllib.request
import numpy as np
import uuid
import time

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)
# driver.get('https://carros.tucarro.com.co/#unapplied_filter_id%3DMODEL%26unapplied_filter_name%3DModelo%26unapplied_value_id%3D68141%26unapplied_value_name%3DCaptiva%26unapplied_autoselect%3Dfalse')
driver.get('https://carros.tucarro.com.co/')
# Store the ID of the original window
original_window = driver.current_window_handle
# Check we don't have other windows open already
assert len(driver.window_handles) == 1

# accept cookies
name_id = 1
driver.find_element(By.CLASS_NAME, 'nav-new-cookie-disclaimer__button').click()

for h in range(40):
    try:
        driver.find_element(By.CLASS_NAME, 'cookie-consent-banner-opt-out__action').click()
    except:
        pass
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
            time.sleep(5)
            to_include = '-O.webp'
            to_include_2 = 'D_NQ_NP_'
            tic = time.time()
            list_urls = [i.url for i in driver.requests if i.response and to_include in i.url and to_include_2 in i.url and i.response.headers['Content-Type'] == 'image/webp']
            list_urls = np.unique(np.array(list_urls))
            for request in list_urls:
                urllib.request.urlretrieve(request, 'src/downloads/car_' + str(uuid.uuid1()) + '.png')
                time.sleep(1)
                print(f'Downloaded {request}')
        except:
            driver.close()
            driver.switch_to.window(original_window)
            print(f'Error with element {idx} in page {h}')
            continue
        driver.close()
        driver.switch_to.window(original_window)
        del driver.requests
    next_button.click()
    time.sleep(5)

print('Done')
