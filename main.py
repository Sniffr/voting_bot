import time
import pandas as pd

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random


def generate_sa_phone_number():
    return "0" + str(random.randint(60, 69)) + str(random.randint(1000000, 9999999))


def fill_text_field_by_id(driver, field_id, text, timeout=30):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.ID, field_id))
        )
        element.send_keys(text)
    except TimeoutException:
        print(f"Timed out waiting for the field with ID {field_id} to become visible")


def click_element_by_id(driver, element_id, timeout=30, use_js=False):
    if use_js:
        try:
            entrepreneur_of_year_button = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.ID, "input_3_3"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", entrepreneur_of_year_button)
            driver.execute_script("arguments[0].click();", entrepreneur_of_year_button)

            print("print wassup")
            return
        except TimeoutException:
            print("Timed out waiting for the 'Entrepreneur of the Year' radio button to become clickable")

    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.ID, element_id))
        )
        element.click()

    except TimeoutException:
        print(f"Timed out waiting for the element with ID {element_id} to become clickable")


def main_func(first_name, last_name, email, phone_area_code, phone_number):
    # Setup WebDriver
    driver = webdriver.Chrome()  # Replace with the path to your WebDriver if necessary
    driver.get("https://form.jotform.com/232885931513259")

    # Filling out the form
    fill_text_field_by_id(driver, "first_45", first_name)
    fill_text_field_by_id(driver, "last_45", last_name)
    fill_text_field_by_id(driver, "input_12", email)
    fill_text_field_by_id(driver, "input_46_area", phone_area_code)
    fill_text_field_by_id(driver, "input_46_phone", phone_number)
    fill_text_field_by_id(driver, "input_4", "Stella Ogema")

    # Selecting the "Entrepreneur of the Year" radio button
    click_element_by_id(driver, "input_3_3", use_js=True)

    # Clicking the "VOTE" button
    click_element_by_id(driver, "input_2")

    time.sleep(5)  # Wait for the page to load
    driver.quit()


def get_progress():
    try:
        with open("progress.txt", "r") as file:
            return int(file.read().strip())
    except FileNotFoundError:
        return 0


def update_progress(progress):
    with open("progress.txt", "w") as file:
        file.write(str(progress))


def main():
    progress = get_progress()
    contacts = pd.read_csv("processed_contacts.csv")
    for index, row in contacts.iterrows():
        if index < progress:
            continue  # Skip already processed contacts
        # Extract the contact details from the row FirstName,LastName,Email,CountryCode,LocalNumber
        first_name, last_name, email, phone_area_code, phone_number = row["FirstName"], row["LastName"], row["Email"], \
            row["CountryCode"], row["LocalNumber"]
        main_func(first_name, last_name, email, phone_area_code, phone_number)
        update_progress(index + 1)  # Update progress after each contact is processed


if __name__ == "__main__":
    main()
