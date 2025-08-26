import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def main():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(chrome_options)
    driver.implicitly_wait(2)

    try:
        driver.get('https://www.library.kr/ggl/merge-user/login?target=ggpoint')
        time.sleep(5)

        idInput = driver.find_element(By.XPATH, "//input[@placeholder='아이디']")
        pwInput = driver.find_element(By.XPATH, "//input[@placeholder='비밀번호']")

        idInput.send_keys(os.getenv('GGPOINT_ID'))
        pwInput.send_keys(os.getenv('GGPOINT_PASSWORD'))
        pwInput.send_keys(Keys.RETURN)
        time.sleep(5)

        driver.get('https://www.library.kr/bookpoint/challenge/challenge')
        time.sleep(5)

        btn = driver.find_element(By.XPATH, '//button[span[text()="출석하기"]]')
        btn.click()
        time.sleep(5)

    except Exception as e:
        print("An error occurred:", e)

    finally:
        driver.quit()

if __name__ == '__main__':
    main()
