from flask import Flask, request, jsonify
from flask_cors import CORS
from linkedin_scraper import Person, actions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from linkedin_scraper import Person

app = Flask(__name__)
CORS(app)
driver = webdriver.Chrome()

#Stupid hackathon making me do things that are deadass illegal
def serialize_person(person):
    # Convert the Person object to a string representation of its __dict__
    return str(person.__dict__)

#Getting email from frontend

@app.route('/api/generate_email', methods=['POST'])
def generate_email():
    try: 
        # Get LinkedIn URL from the request
        data = request.get_json()
        linkedin_link = data.get('linkedin_url', '')
        #return jsonify({"linkedin_url": linkedin_link}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    # LinkedIn credentials
    email = "johndoADear@proton.me"  # Replace with your LinkedIn email
    password = "Hackathon123"        # Replace with your LinkedIn password
    actions.login(driver, email, password)

    #Trying to scrape
    person = Person(linkedin_link, driver=driver, scrape=False)
    returnVal = person.scrape()
    print(returnVal)
    return jsonify({"person_data": serialize_person(returnVal)}), 200




if __name__ == '__main__':
    app.run(debug=True)
