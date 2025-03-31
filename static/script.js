document.getElementById("scrapeButton").addEventListener("click", async function() {
    const website = document.getElementById("website").value;
    const keywords = document.getElementById("keywords").value;
    const status = document.getElementById("status");

    if (!website || !keywords) {
        status.innerText = "Please enter both website URL and keywords.";
        return;
    }

    status.innerText = "Scraping in progress... Please wait.";

    try {
        const response = await fetch("/scrape", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ website, keywords })
        });

        if (!response.ok) {
            const errorMessage = await response.json();
            status.innerText = "Error: " + errorMessage.error;
            return;
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "job_listings.csv";
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        status.innerText = "Download complete!";
    } catch (error) {
        status.innerText = "Failed to scrape. Please check the website URL.";
    }
});
