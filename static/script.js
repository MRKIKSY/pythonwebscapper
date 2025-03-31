document.getElementById("scrapeButton").addEventListener("click", async function() {
    const website = document.getElementById("website").value;
    const keywords = document.getElementById("keywords").value;
    const status = document.getElementById("status");

    // Check if both fields are filled out
    if (!website || !keywords) {
        status.innerText = "Please enter both website URL and keywords.";
        return;
    }

    status.innerText = "Scraping in progress... Please wait.";

    try {
        // Send POST request with website and keywords
        const response = await fetch("/scrape", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ website, keywords })
        });

        // Check for errors in response
        if (!response.ok) {
            const errorMessage = await response.json();
            status.innerText = "Error: " + errorMessage.error || "Something went wrong!";
            return;
        }

        // If the response is okay, download the CSV file
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "job_listings.csv";  // Set file name for download
        document.body.appendChild(a);
        a.click();  // Programmatically click the link to trigger download
        document.body.removeChild(a);  // Remove the element after download

        status.innerText = "Download complete!";
    } catch (error) {
        // Error handling if something goes wrong during fetch
        status.innerText = "Failed to scrape. Please check the website URL.";
        console.error("Error during scraping:", error);  // Log error for debugging
    }
});
