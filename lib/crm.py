from selenium import webdriver
import platform
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import time
import os
from selenium.webdriver.common.by import By
from lib.BrailleToKor_Python_main.src.BrailleToKorean.BrailleToKor import BrailleToKor
from lib.circle_detection import detect_and_draw_circles

def braille_to_korean(output_file_path):
    start = time.time()
    
    # 크롬 옵션 설정
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    
    try:
        # OS 타입 확인하여 드라이버 경로 설정
        os_name = platform.system()
        
        # chromedriver 자동 설치
        chromedriver_path = chromedriver_autoinstaller.install()
        print(f"Chromedriver 설치됨: {chromedriver_path}")
        
        # 웹드라이버 초기화
        service = Service(chromedriver_path)
        crawler = webdriver.Chrome(service=service, options=options)
        
    except Exception as e:
        print(f"드라이버 초기화 오류: {e}")
        # 수동 방식으로 재시도
        try:
            chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
            
            if os_name == 'Windows':
                driver_path = f'./{chrome_ver}/chromedriver.exe'
            elif os_name == 'Darwin':  # macOS
                driver_path = f'./{chrome_ver}/chromedriver'
            else:  # Linux
                driver_path = f'./{chrome_ver}/chromedriver'
                
            print(f"수동 드라이버 경로: {driver_path}")
            
            # chromedriver 폴더 확인 또는 생성
            driver_dir = f'./{chrome_ver}'
            if not os.path.exists(driver_dir):
                os.makedirs(driver_dir)
                
            # 드라이버 설치 시도
            chromedriver_autoinstaller.install(True)
            
            service = Service(driver_path)
            crawler = webdriver.Chrome(service=service, options=options)
        except Exception as e2:
            print(f"드라이버 재시도 오류: {e2}")
            return ["오류 발생", "브라우저 초기화 실패"]
    
    try:
        # 절대 경로로 변환
        abs_file_path = os.path.abspath(output_file_path)
        print(f"파일 경로: {abs_file_path}")
        
        # 웹사이트 접근 및 파일 제출
        crawler.implicitly_wait(10)
        crawler.get('https://abcbraille.com/')
        crawler.implicitly_wait(10)
        crawler.find_element(By.ID, "file").send_keys(abs_file_path)
        crawler.implicitly_wait(10)
        crawler.find_element('xpath', '//*[@id="rotate_form"]/input[4]').click()
        crawler.implicitly_wait(10)
        
        # 결과 추출
        text_a = crawler.find_element(By.CLASS_NAME, 'col-md-6')
        text_b = text_a.find_element(By.TAG_NAME, 'ol')
        text_c = text_b.find_element(By.TAG_NAME, 'li')
        result = text_c.text
        
        # 점자를 한글로 변환
        b = BrailleToKor()
        korean_text = b.translation(result)
        
        end = time.time()
        print(f"{end - start:.5f} sec")
        a = [result, korean_text]
        
        # 브라우저 종료
        crawler.quit()
        
        return a
        
    except Exception as e:
        print(f"브라우저 처리 오류: {e}")
        try:
            crawler.quit()
        except:
            pass
        return ["오류 발생", "변환 과정에서 실패"]