document.addEventListener("DOMContentLoaded", function() {
    const fileInput = document.getElementById("fileInput");
    const uploadButton = document.getElementById("uploadButton");

    // Event listener for file selection
    fileInput.addEventListener("change", function(event) {
        const file = event.target.files[0];
        if (file) {
            displayCsvPreview(file);
        }
    });

    // Event listener for file upload
    uploadButton.addEventListener("click", function() {
        const file = fileInput.files[0];
        if (!file) {
            alert("Please select a CSV file.");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        fetch("http://localhost:8000/upload", {
            method: "POST",
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.message.includes("Error")) {
                alert(data.message);  // Display the error message
            } else {
                alert("File uploaded and processed successfully.");
                
                // Display the prediction
                const predictionText = data.prediction === 1 ? "Yes" : "No";
                document.getElementById("prediction").innerHTML = `<h2>Prediction: ${predictionText}</h2>`;
        
                // Display the probabilities
                let probabilitiesHtml = "<h2>Probabilities</h2>";
                probabilitiesHtml += "<table class='probabilities-table'>";
                probabilitiesHtml += "<tr><th>Yes</th><th>No</th></tr>";
                probabilitiesHtml += `<tr><td>${data.probabilities[0][1].toFixed(7)}</td><td>${data.probabilities[0][0].toFixed(7)}</td></tr>`;
                probabilitiesHtml += "</table>";
                document.getElementById("probabilities").innerHTML = probabilitiesHtml;

                const explanationHtml = `<h2>Explanation</h2><a href="${data.link}" target="_blank">View Explanation</a>`;
                document.getElementById("explanation").innerHTML = explanationHtml;

            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An error occurred while uploading the file.");
        });
    });
});

// Function to display CSV preview
function displayCsvPreview(csvFile) {
    const reader = new FileReader();
    reader.onload = function(event) {
        const text = event.target.result;
        const lines = text.split("\n").map(line => line.split(";"));
        const headers = lines[0];
        const rows = lines.slice(1, 6); // Display first 5 rows for preview

        let previewHtml = "<h2>Data Preview</h2><div class='scrollable'><table>";
        previewHtml += "<tr>" + headers.map(header => `<th>${header}</th>`).join("") + "</tr>";
        rows.forEach(row => {
            previewHtml += "<tr>" + row.map(cell => `<td>${cell}</td>`).join("") + "</tr>";
        });
        previewHtml += "</table></div>";
        document.getElementById("dataPreview").innerHTML = previewHtml;
    };
    reader.readAsText(csvFile);
}
