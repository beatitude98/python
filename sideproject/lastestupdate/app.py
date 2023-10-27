from flask import Flask, render_template, request
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    search_product = request.form.get('search_product')

    def web_scrape(search_product):
        url = "https://m.bunjang.co.kr/"

        driver = webdriver.Chrome()
        driver.get(url)
        driver.fullscreen_window()

        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="root"]/div/div/div[2]/div[1]/div[1]/div[1]/div[1]/input'))
        )

        search_box.send_keys(search_product)
        search_box.send_keys(Keys.RETURN)

        product_list = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "sc-cTjmhe"))
        )

        total_price = 0
        products = []

        for i in range(1, 101):
            name_xpath = f'//*[@id="root"]/div/div/div[4]/div/div[4]/div/div[{i}]/a/div[2]/div[1]'
            price_xpath = f'//*[@id="root"]/div/div/div[4]/div/div[4]/div/div[{i}]/a/div[2]/div[2]/div[1]'

            try:
                product_name = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, name_xpath))
                ).text

                product_price = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, price_xpath))
                ).text

                product_price = int(product_price.replace(',', ''))  # 가격에서 , 제거
                total_price += product_price

                products.append((product_name, product_price))

                print(f'{i} : 상품명 : {product_name}, 가격 : {product_price}')
            except Exception as e:
                print(f'상품 정보를 가져오는 데 실패했습니다. 오류 메시지: {e}')

            if len(products) >= 100:
                break

        # 크롤링된 상품 수에 따라 평균 가격을 계산
        if len(products) > 0:
            average_price = total_price / len(products)
        else:
            average_price = 0

        driver.quit()  # 브라우저를 닫습니다.

        return products, average_price

    return render_template('results.html', products=products)

if __name__ == '__main__':




    app.run()