let currentIndex = 0;
const totalTime = 30; // Time for each object (in seconds)
const progressBar = document.getElementById("progress-bar");
const indexIndicator = document.getElementById("index-indicator");

fetch('staff.txt')
    .then(response => response.json())
    .then(staff => {

    });


// Fetch the data from 'data.json' file
fetch('website_data.json')
    .then(response => response.json())  // Automatically parses the JSON
    .then(data => {
        // Call cycle function with the fetched data
        cycleThroughObjects(data);
    })
    .catch(error => {
        console.error('Error fetching JSON:', error);
    });

function displayObject(index, data) {
    const obj = data[index];

    // Display the title, abstract, and authors
    document.getElementById("title").textContent = obj.title;
    document.getElementById("abstract").textContent = obj.abstract;
    MathJax.typeset();
    if (obj.authors.length > 1){
        document.getElementById("authors").textContent = "Authors: " + obj.authors.join(", ");
    } else {
        document.getElementById("authors").textContent = "Author: " + obj.authors.join(", ");
    }

    document.getElementById("name").textContent = "ePrint " + obj.name;


    // Add animation for smooth transition between objects
    const contentContainer = document.getElementById("content-container");
    contentContainer.href = "https://eprint.iacr.org/" + obj.pdffile;
    contentContainer.classList.remove("show");  // Hide content
    setTimeout(() => {
        contentContainer.classList.add("show");  // Show new content after fade out
    }, 500);  // Wait for 0.5s before showing new content

    if (obj.radboud == "true") {
        document.body.style.backgroundColor = "#e3000b";  // Make the entire page background red
    } else {
        document.body.style.backgroundColor = "";     // Reset to default background if radboud is false
    }

    // Reset progress bar
    progressBar.style.width = "0%";
    indexIndicator.textContent = `${index + 1} of ${data.length} from recent ePrints`;

    let elapsedTime = 0;
    const interval = setInterval(() => {
        elapsedTime++;
        progressBar.style.width = `${(elapsedTime / totalTime) * 100}%`;

        if (elapsedTime >= totalTime) {
            clearInterval(interval);
            setTimeout(() => {
                // Move to the next object, looping back to the first one if necessary
                currentIndex = (currentIndex + 1) % data.length;
                displayObject(currentIndex, data);
            }, 500);
        }
    }, 1000); // Update every second

}

function cycleThroughObjects(data) {
    displayObject(currentIndex, data);

    // Move to the next object every 5 seconds
    // currentIndex = (currentIndex + 1) % data.length;  // Wrap back to the first object when done

    // setTimeout(() => cycleThroughObjects(data), 20000);  // 5-second interval
}
