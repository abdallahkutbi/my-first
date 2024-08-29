from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from urllib.parse import urlparse
from selenium.common.exceptions import NoSuchElementException
import time

non_full_classes = set()

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

    

def open_website_and_navigate(driver, url):#### FULLY DONE 
    try:
        driver.get(url)
        print("Main page loaded.")

        i = 0
        while True:
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "coursearch-result")))
            courses = driver.find_elements(By.CLASS_NAME, "coursearch-result")

            if i < len(courses):
                print("------------------------------------------------------------")
                courses[i].click()
                print(f"Course {i + 1} clicked.")
                driver.execute_script("arguments[0].scrollIntoView(true);", courses[i])

                try:
                    section_link = courses[i].find_element(By.CLASS_NAME, "coursearch-result-sections-link")
                    section_link.click()
                except NoSuchElementException:
                    print(f"Section link not found for course number {i + 1}")
                    i += 1
                    continue

                check_class_full(driver)
                driver.back()
            else:
                print("No more courses found.")
                break

            i += 1

        return True

    except TimeoutException:
        print("The page did not load as expected or elements were not found.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False






def check_class_full(driver):
    global non_full_classes

    # Wait for the table to be loaded on the page
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "table")))

    # Extract course name parts (h1 and h6)
    course_name_h6 = driver.find_element(By.TAG_NAME, "h6").text
    full_course_name = f"{course_name_h6}"
    print(full_course_name)

    # Find all the data rows in the section table, starting from the second row
    section_rows = driver.find_elements(By.XPATH, "//*[@id='body-tag']/main/div/div/div/table/tbody/tr[position()>1]")

    for row in section_rows:
        try:
            # Extract the section number from the first cell (td[1])
            section_number = row.find_element(By.XPATH, ".//td[1]").text.strip()

            # Extract notes from the eighth cell (td[8]) to check if the class is full
            notes_cell = row.find_element(By.XPATH, ".//td[8]").text

            print(f"Checking section {section_number}: Notes - '{notes_cell}'")

            # Check if the 'Notes' cell does not contain "Class Full" or "Closed"
            if "Class Full" not in notes_cell and "Closed" not in notes_cell and "WebReg" not in notes_cell and "Stamped Approval" not in notes_cell:
                non_full_classes.add(course_name_h6)  # Add only course name
        except NoSuchElementException:
            print("An element was not found in this row, skipping.")
            continue

    print("Non-full classes so far:", non_full_classes)
    return non_full_classes



    

def main():
    print("Welcome to the Course Finder Program!")

    url = ""
    while not is_valid_url(url):
        url = input("Please enter the URL to check: ")
        if not is_valid_url(url):
            print("Invalid URL. Please enter a valid URL.")

    firefox_options = webdriver.FirefoxOptions()
    #firefox_options.add_argument("--headless")
    gecko_driver_path = '/Users/abdullahkutbi/Desktop/Personal/Code/Course finder/geckodriver'
    service = Service(executable_path=gecko_driver_path)
    driver = webdriver.Firefox(service=service, options=firefox_options)

    try:
        open_website_and_navigate(driver, url)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()


