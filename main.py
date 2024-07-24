from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_property_data():
    header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/84.0.4147.125 Safari/537.36",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
    }
    response = requests.get("https://appbrewery.github.io/Zillow-Clone/", headers=header)
    soup = BeautifulSoup(response.text, "html.parser")

    all_link_elements = soup.select(".StyledPropertyCardDataWrapper a")
    all_links = [link["href"] for link in all_link_elements]

    all_address_elements = soup.select(".StyledPropertyCardDataWrapper address")
    all_addresses = [address.get_text().replace(" | ", " ").strip() for address in all_address_elements]

    all_price_elements = soup.select(".PropertyCardWrapper span")
    all_prices = [price.get_text().replace("/mo", "").split("+")[0] for price in all_price_elements if
                  "$" in price.text]

    return all_links, all_addresses, all_prices


def fill_google_form(links, addresses, prices):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)

    form_url = ("https://docs.google.com/forms/d/e/1FAIpQLSd_CVLAh4y8GUyBfMYKommF7sS41LP9wijk0RuMpUPna27z0w/viewform"
                "?usp=sf_link")

    for link, address, price in zip(links, addresses, prices):
        driver.get(form_url)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input'))
            )
            address_field = driver.find_element(by=By.XPATH,
                                                value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div['
                                                      '2]/div/div[1]/div/div[1]/input')
            price_field = driver.find_element(by=By.XPATH,
                                              value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div['
                                                    '2]/div/div[1]/div/div[1]/input')
            link_field = driver.find_element(by=By.XPATH,
                                             value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div['
                                                   '2]/div/div[1]/div/div[1]/input')
            submit_button = driver.find_element(by=By.XPATH,
                                                value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')

            address_field.send_keys(address)
            price_field.send_keys(price)
            link_field.send_keys(link)
            submit_button.click()
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    all_links, all_addresses, all_prices = scrape_property_data()
    fill_google_form(all_links, all_addresses, all_prices)
