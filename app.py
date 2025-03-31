from flask import Flask, request, send_file, render_template, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup
import requests
import pandas as pd
from io import BytesIO
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Initialize Flask app
app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)  # Allow all origins

# Function to scrape a website
def get_dynamic_page(url):
    """Loads JavaScript-rendered pages using Selenium"""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    
    page_source = driver.page_source
    driver.quit()
    return page_source

@app.route('/')
def index():
    """Serve the index.html file"""
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    """Handle scraping request"""
    data = request.get_json()
    website = data.get('website')
    keywords = data.get('keywords', "").split(',')

    job_listings = []

    try:
        print(f"Scraping website: {website}")  # Debugging log

        # Use Selenium if the website relies on JavaScript
        html = get_dynamic_page(website) if "remoteok.io" in website else requests.get(
            website, headers={"User-Agent": "Mozilla/5.0"}
        ).text
        
        soup = BeautifulSoup(html, 'html.parser')

        # Debugging: Print first 500 characters of page content
        print(soup.prettify()[:500])

        # Find job listings (Update this selector based on website)
        job_elements = soup.find_all('div', class_='job-listing')  # Modify as needed

        for job in job_elements:
            title = job.find('h2').text.strip() if job.find('h2') else 'N/A'
            link = job.find('a')['href'] if job.find('a') else 'N/A'

            if any(keyword.lower() in title.lower() for keyword in keywords):
                job_listings.append({'Job Title': title, 'Job Link': link})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    if not job_listings:
        return jsonify({'error': 'No job listings found. Check the website structure and selectors.'}), 400

    df = pd.DataFrame(job_listings)

    # Save CSV to memory and return it
    output = BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)

    return send_file(output, as_attachment=True, download_name='job_listings.csv', mimetype='text/csv')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
