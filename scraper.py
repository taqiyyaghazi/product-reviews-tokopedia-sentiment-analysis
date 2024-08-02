from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time

options = Options()
options.add_argument('-headless')

def scrape_product_urls(product_name):
    driver = webdriver.Firefox(options=options)
    search_url = f"https://www.tokopedia.com/search?q={product_name}"
    results = []
    try:
        driver.get(search_url)
        time.sleep(2)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        has_next = True
        page = 1

        while page <= 20:
            try:
                wait = WebDriverWait(driver, 5)
                wait.until(EC.presence_of_element_located((By.XPATH, "//div[@data-testid='divSRPContentProducts']")))
                content = driver.page_source
                soup = BeautifulSoup(content, 'html.parser')

                print(f'page {page}')
                product_container_element = soup.find(attrs={"data-testid": "divSRPContentProducts"})

                if product_container_element:
                    product_card_element = product_container_element.find_all('a')
                    product_urls = [a.get('href') for a in product_card_element]
                    results.extend(product_urls)
                
                next_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//button[@aria-label="Laman berikutnya"]'))
                )
                next_button.click()
                page += 1
            except:
                has_next = False
        
        return results
    except Exception as e:
        driver.quit()
        print('Error', e)

def scrape_product_review_url(product_url):
    driver = webdriver.Firefox(options=options)
    try:
        driver.get(product_url)

        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 3000);")
        try:
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.XPATH, "//*[@data-testid='btnViewAllFeedback']")))

            content = driver.page_source
            soup = BeautifulSoup(content, 'html.parser')

            see_all_feedback_element = soup.find(attrs={"data-testid": "btnViewAllFeedback"})

            if see_all_feedback_element:
                driver.quit()
                path = see_all_feedback_element.get('href')
                return path
            else:
                raise Exception('Tombol tidak ditemukan')
        except:
            raise Exception('Review tidak ditemukan')    
    except Exception as e:
        driver.quit()
        print('Error', e)

def scrape_product_reviews(product_review_url):
    results = []
    driver = webdriver.Firefox(options=options)

    try:
        driver.get(product_review_url)
        time.sleep(2)

        has_reviews = True
        page = 1

        while has_reviews:
            try:
                wait = WebDriverWait(driver, 10)
                wait.until(EC.presence_of_element_located((By.ID, "review-feed")))


                content = driver.page_source
                soup = BeautifulSoup(content, 'html.parser')

                review_feed = soup.find('section', {"id": "review-feed"})
                reviews = review_feed.find_all('article')

                for index, review in enumerate(reviews):
                    print(f'Mengambil {index + 1}/{len(reviews)} Ulasan, Page {page}')
                    rating = review.find(attrs={"data-testid": "icnStarRating"})
                    text = review.find(attrs={"data-testid": "lblItemUlasan"})
                    results.append({
                        "rating": int(rating.get('aria-label').split(' ')[1]),
                        "review": text.text if text is not None else None
                    })

                next_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//button[@aria-label="Laman berikutnya"]'))
                )
                next_button.click()
                page += 1
            except:
                has_reviews = False
                driver.quit()
                return results
    except Exception as e:
        driver.quit()
        print('Error', e)