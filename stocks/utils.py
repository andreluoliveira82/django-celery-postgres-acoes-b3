import pytz
from datetime import datetime
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from stocks.models import Stock


def search_stock_price(stock_name):
    """
    Search stock price in Google and save to database
    """
    options = Options()
    options.add_argument("--headless")
    
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        url = "https://www.google.com"

        driver.get(url)

        search_input = driver.find_element(By.XPATH, '//textarea[@aria-label="Pesquisar"]')

        search_input.send_keys(f"{stock_name} stock price")
        search_input.send_keys(Keys.RETURN)

        sleep(2)

        price_div = driver.find_element(By.XPATH, '//div[@data-attrid="Price"]')
        price = price_div.find_elements(By.TAG_NAME, "span")[2].text.replace(",", ".")

        driver.quit()

        print(f"Stock {stock_name} -  price {price}")

        # Save stock price to database
        _save_stock_price(stock_name, price)

        return price
    except Exception as e:
        print(f"Error searching stock price for {stock_name}: {e}")
        return None
    

def _save_stock_price(stock_name, price):
    """
    Save stock price to database using django orm
    """

    # Obter o horário atual no fuso horário de São Paulo 
    tz = pytz.timezone("America/Sao_Paulo")
    current_time = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

    Stock.objects.create(
        name=stock_name,
        price=price,
        moment=current_time # datetime.now(tz)
    )