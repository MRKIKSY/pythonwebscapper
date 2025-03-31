from flask import Flask, request, send_file, send_from_directory
from flask_cors import CORS
from bs4 import BeautifulSoup
import requests
import pandas as pd
from io import BytesIO
import os

# Initialize Flask app and enable CORS
app = Flask(__name__, static_folder="static", static_url_path="/static")
CORS(app)  # Allow all origins by default

@app.route('/')
def index():
    # Serve the index.html file correctly
    return send_from_directory('static', 'index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    website = data['website']
    keywords = data['keywords'].split(',')

    job_listings = []
    
    try:
        response = requests.get(website)
        soup = BeautifulSoup(response.text, 'html.parser')

        for job in soup.find_all('div', class_='job-listing'):  # Update this selector
            title = job.find('h2').text.strip() if job.find('h2') else 'N/A'
            link = job.find('a')['href'] if job.find('a') else 'N/A'
            
            if any(keyword.lower() in title.lower() for keyword in keywords):
                job_listings.append({'Job Title': title, 'Job Link': link})

    except Exception as e:
        return {'error': str(e)}, 500

    df = pd.DataFrame(job_listings)

    output = BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)

    return send_file(output, as_attachment=True, download_name='job_listings.csv', mimetype='text/csv')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use environment variable for port
    app.run(debug=False, host='0.0.0.0', port=port)
