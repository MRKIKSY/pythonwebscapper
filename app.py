from flask import Flask, render_template, request, send_file
from flask_cors import CORS
from bs4 import BeautifulSoup
import requests
import pandas as pd
from io import BytesIO

# Initialize Flask app and enable CORS
app = Flask(__name__)
CORS(app)  # Allow all origins by default, or configure for specific domains

@app.route('/')
def index():
    # Use render_template() to serve the HTML file from /templates folder
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    # Get JSON data from the frontend
    data = request.get_json()
    website = data['website']
    keywords = data['keywords'].split(',')  # Split keywords by commas

    job_listings = []

    # Start scraping the website
    try:
        response = requests.get(website)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Example scraping logic: Adjust according to the website's structure
        for job in soup.find_all('div', class_='job-listing'):  # Replace with actual class names
            title = job.find('h2').text.strip() if job.find('h2') else 'N/A'
            link = job.find('a')['href'] if job.find('a') else 'N/A'
            
            # Only keep jobs matching the keywords
            if any(keyword.lower() in title.lower() for keyword in keywords):
                job_listings.append({
                    'Job Title': title,
                    'Job Link': link
                })

    except Exception as e:
        return {'error': str(e)}, 500  # Return error if scraping fails

    # Convert the job listings to a DataFrame and save as a CSV file
    df = pd.DataFrame(job_listings)

    # Save the CSV file to a BytesIO object
    output = BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)

    # Return the CSV file as a response (download link)
    return send_file(output, as_attachment=True, download_name='job_listings.csv', mimetype='text/csv')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
