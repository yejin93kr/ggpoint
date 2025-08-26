import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

LOGIN_URL = "https://www.library.kr/ggl/merge-user/login?target=ggpoint"
CHALLENGE_URL = "https://www.library.kr/bookpoint/challenge/challenge"

def fail(msg: str):
    print(msg, file=sys.stderr)
    sys.exit(1)

def main():
    gg_id = os.getenv("GGPOINT_ID")
    gg_pw = os.getenv("GGPOINT_PASSWORD")
    if not gg_id or not gg_pw:
        fail("환경변수 GGPOINT_ID / GGPOINT_PASSWORD 가 비어 있습니다.")
    
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(chrome_options)
    wait = WebDriverWait(driver, 15)

    try:
        driver.get(LOGIN_URL)

        id_input = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='아이디']"))
        )
        pw_input = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='비밀번호']"))
        )

        id_input.clear(); id_input.send_keys(gg_id)
        pw_input.clear(); pw_input.send_keys(gg_pw)
        pw_input.send_keys(Keys.RETURN)
        time.sleep(5)

        try:
            wait.until(lambda d: "login" not in d.current_url)
        except TimeoutException:
            fail("로그인 실패: 로그인 페이지에서 벗어나지 못했습니다.")

        driver.get(CHALLENGE_URL)
        time.sleep(5)

        try:
            btn = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//button[span[normalize-space(text())="출석하기"]]'))
            )
        except TimeoutException:
            fail("버튼 클릭 실패: '출석하기' 버튼을 찾지 못했습니다. (이미 출석 완료 상태일 수도 있음)")

        btn.click()
        time.sleep(5)
        print("✅ 완료: 로그인 및 출석 버튼 클릭 성공")

    except Exception as e:
        print("An error occurred:", e)

    finally:
        driver.quit()

if __name__ == '__main__':
    main()
