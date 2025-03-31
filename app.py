from flask import Flask, request, send_file, render_template
from bs4 import BeautifulSoup
import requests
import pandas as pd
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    # Serve the static index.html file
    return app.send_static_file('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    website = data['website']
    keywords = data['keywords'].split(',')  # Split keywords by commas

    job_listings = []

    # Start scraping
    response = requests.get(website)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Example of extracting job data (adjust based on the website structure)
    for job in soup.find_all('div', class_='job-listing'):  # Replace with actual class names
        title = job.find('h2').text.strip() if job.find('h2') else 'N/A'
        link = job.find('a')['href'] if job.find('a') else 'N/A'
        
        if any(keyword.lower() in title.lower() for keyword in keywords):
            job_listings.append({
                'Job Title': title,
                'Job Link': link
            })

    # Convert to DataFrame and export as CSV
    df = pd.DataFrame(job_listings)

    # Save to a BytesIO object
    output = BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)

    return send_file(output, as_attachment=True, download_name='job_listings.csv', mimetype='text/csv')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
