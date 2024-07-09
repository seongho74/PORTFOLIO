from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
import time
import random


def setup_driver():
    """
    Chrome 옵션 설정, WebDriver 초기화
    """
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument('--window-size=1920x1080')
    chrome_options.add_argument("log-level=3")
    chrome_options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def login(driver, username, password):
    """
    아프리카TV 접속, 로그인
    """
    driver.get('https://www.afreecatv.com/')
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginBtn"]'))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="uid"]'))).send_keys(username)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]'))).send_keys(password)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form[3]/div/fieldset/p[3]/button/span'))).click()

def get_broadcast_links(driver):
    """
    아프리카TV 전체 시청 목록 정렬, 링크 추출
    """
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="all"]/a'))).click()
    
    html = driver.page_source
    soup = bs(html, 'html.parser')
    titles = soup.select('div.cBox-info > h3 > a')
    links = []
    for n in titles:
        links.append(n.get('href'))
    
    return links

def access_broadcast(driver, link):
    """
    방송 접속
    """
    driver.get(link)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="stop_screen"]/dl/dd[2]'))).click()
    time.sleep(5)

def check_bookmark(driver):
    """
    즐찾 여부 확인하여 즐찾 추가
    """
    bookmark = driver.find_element(By.CSS_SELECTOR, 'button[data-target="bookmark_text"]')
    bookmark_attribute = bookmark.get_attribute("class")
    if "on" in bookmark_attribute.split():
        print("이미 즐겨찾기 중입니다.")
    else:
        driver.find_element(By.XPATH, '//*[@id="player_area"]/div[1]/div/div[3]/ul/li[16]/button').click()
        print("즐겨찾기 하였습니다.")

def change_quality(driver):
    """
    방송 화질 변경
    """
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.quality_box'))).click()
    quality_text = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="afreecatv_player"]/div[9]/div[2]/div[1]/button/span'))
    ).text
    print("이전 화질 : ", quality_text)
    
    driver.execute_script(
        "var element = document.querySelector('div.quality_box');"
        "if (element) { element.className = 'quality_box_on'; }"
    )
    
    hidden_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="afreecatv_player"]/div[9]/div[2]/div[1]/ul/li[1]/button'))
    )
    hidden_button.click()

    
    quality2_text = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="afreecatv_player"]/div[9]/div[2]/div[1]/button/span'))
    ).text
    print("변경된 화질 : ", quality2_text)

def get_random_link(links):
    """
    랜덤한 링크 추출
    """
    return random.choice(links)

def log_out(driver):
    """
    로그아웃
    """
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="profileWrapBtn"]/div[1]/button'))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="profileWrapBtn"]/div[2]/div[1]/div[4]/li[2]/a'))).click()
    print("로그아웃")


def main():
    username = 'ID'
    password = 'PW'
    
    with setup_driver() as driver:
        login(driver, username, password)
        links = get_broadcast_links(driver)
        
        if links:
            random_link = get_random_link(links)
            print("랜덤으로 선택된 방송 접속 주소 : ", random_link)
            access_broadcast(driver, random_link)
            check_bookmark(driver)
            change_quality(driver)
            log_out(driver)
        else:
            print("방송 목록을 가져올 수 없습니다.")

if __name__ == "__main__":
    main()