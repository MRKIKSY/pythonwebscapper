document.getElementById("scrapeForm").addEventListener("submit", function(event) {
    event.preventDefault();
    
    const website = document.getElementById("website").value;
    const keywords = document.getElementById("keywords").value;
    const status = document.getElementById("status");

    // Show loading status
    status.textContent = "Scraping in progress...";

    fetch("/scrape", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            website: website,
            keywords: keywords
        })
    })
    .then(response => response.blob())
    .then(blob => {
        // Create a download link for the file
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = "job_listings.csv";
        link.click();

        status.textContent = "Scraping complete! Downloading CSV...";
    })
    .catch(error => {
        console.error("Error:", error);
        status.textContent = "An error occurred while scraping.";
    });
});
