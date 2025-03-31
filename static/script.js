document.getElementById('scrapeButton').addEventListener('click', async function() {
    const website = document.getElementById('website').value;
    const keywords = document.getElementById('keywords').value;

    if (!website || !keywords) {
        alert('Please enter both website and keywords.');
        return;
    }

    try {
        const response = await fetch('/scrape', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                website: website,
                keywords: keywords
            })
        });

        if (!response.ok) {
            throw new Error('Failed to fetch job listings');
        }

        const blob = await response.blob();
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = 'job_listings.csv';
        link.click();

    } catch (error) {
        alert('Error: ' + error.message);
    }
});
