from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def check_nft_owner(nft_link: str) -> str:
    """
    Проверяет владельца NFT по ссылке на NFT.
    Возвращает username владельца NFT.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Запуск браузера в фоновом режиме

    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(nft_link)

        # Ищем элемент <a>, содержащий ссылку на https://t.me/
        link_element = driver.find_element(By.XPATH, "//a[contains(@href, 't.me')]")
        link = link_element.get_attribute("href")
        return link[13:]  # Убираем "https://t.me/" из ссылки
    except Exception as e:
        print(f"Ошибка при проверке владельца NFT: {e}")
        return None
    finally:
        driver.quit()