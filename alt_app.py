from flask import Flask, request, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

app = Flask(__name__)
CORS(app)

@app.route('/api/generate_email', methods=['POST'])

def generate_email():
    # Get LinkedIn URL from the request
    data = request.get_json()
    linkedin_url = data.get('linkedin_url')

    if not linkedin_url:
        return jsonify({"error": "LinkedIn URL is required"}), 400

    # Set up Selenium WebDriver
    chrome_service = Service("C:\\Users\\alisa\\OneDrive\\Desktop\\Projects\\AI_Personalized_Email_Marketing\\chromedriver-win64\\chromedriver.exe")  # REPLACE WITH YOUR OWN CHROMEDRIVER PATH !!!
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run browser in headless mode
    driver = webdriver.Chrome(service=chrome_service, options=options)

    try:
        # Open the LinkedIn profile page
        driver.get(linkedin_url)
        wait = WebDriverWait(driver, 10)

        # Scrape data from the page
        try:
            name = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1"))).text
        except TimeoutException:
            name = "Name not found"

        try:
            bio = driver.find_element(By.CSS_SELECTOR, ".text-body-medium.break-words").text
        except NoSuchElementException:
            bio = "Bio not found"

        jobs = []

        try:
            # Wait until job elements are loaded
            job_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".pvs-entity"))
            )

            # Iterate over each job entry
            for job in job_elements:
                job_info = {}

                try:
                    # Scraping job title
                    title = job.find_element(By.CSS_SELECTOR, ".mr1.t-bold span").text
                    job_info["title"] = title
                except NoSuchElementException:
                    job_info["title"] = "Title not found"

                try:
                    # Scraping company name
                    company = job.find_element(By.CSS_SELECTOR, ".t-14.t-normal span").text
                    job_info["company"] = company
                except NoSuchElementException:
                    job_info["company"] = "Company not found"

                try:
                    # Scraping job description
                    description = job.find_element(By.CSS_SELECTOR, ".pv-shared-text-with-see-more span").text
                    job_info["description"] = description
                except NoSuchElementException:
                    job_info["description"] = "Description not found"

                # Append the job info to jobs list
                jobs.append(job_info)

        except Exception as e:
            print("Error while scraping job experiences:", e)

        # Create a response dictionary
        response = {
            "name": name,
            "bio": bio,
            "jobs": jobs
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        driver.quit()


if __name__ == '__main__':
    app.run(debug=True)