from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import csv

driver = webdriver.Chrome()
url = "https://steamcommunity.com/app/648800/negativereviews/?browsefilter=toprated&snr=1_5_100010_&filterLanguage=english#scrollTop=0"
driver.get(url)

scroll_count = 5

while True:
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    body = driver.find_element(By.TAG_NAME, 'body')
    body.send_keys(Keys.END)
    time.sleep(4) 
    new_height = driver.execute_script("return document.documentElement.scrollHeight")
    if new_height == last_height:
        break

    last_height = new_height
soup = BeautifulSoup(driver.page_source, "html.parser")
reviews = soup.find_all("div", class_="apphub_Card modalContentLink interactable")


dataset = []

for review in reviews:
    try:
        comment = review.find("div", class_="apphub_CardTextContent").get_text(strip=True)
        rating_element = review.find("div", class_="apphub_CardRating")
        rating = rating_element.get_text(strip=True) if rating_element else "N/A"
        dataset.append([comment, rating])
    except Exception as e:
        print("Hata oluştu:", str(e))
        continue


with open("yorumlar.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Yorum", "Puan"])
    writer.writerows(dataset)

driver.quit()
