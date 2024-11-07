let elapsedTime = 0;
let currentIndex = 0;
let interval = null;
const totalTime = 30; // Time for each object (in seconds)
const progressBar = document.getElementById("progress-bar");
const indexIndicator = document.getElementById("index-indicator");

// Fetch the data from 'data.json' file
fetch('website_data.json')
    .then(response => response.json())  // Automatically parses the JSON
    .then(data => {
        // Call cycle function with the fetched data
        displayObject(currentIndex, data);    

        document.addEventListener("keydown", (event) => {
            if (event.key === "ArrowLeft") {
                progressBar.style.transition = "none"; 

                if (elapsedTime < 1){
                    clearInterval(interval);

                    currentIndex = (currentIndex - 1) % data.length;
                    displayObject(currentIndex, data);
                } else {
                    elapsedTime = Math.max(0, elapsedTime - 5);  // Prevent negative values
                }
        
                progressBar.style.width = `${(elapsedTime / totalTime) * 100}%`;
        
                setTimeout(() => {
                    progressBar.style.transition = "width 1s linear"; 
                }, 10);
        
            } else if (event.key === "ArrowRight") {
        
                clearInterval(interval);

                currentIndex = (currentIndex + 1) % data.length;
                displayObject(currentIndex, data);
        
            }
        });

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
    }, 10);  // Wait for 0.5s before showing new content

    if (obj.radboud == "true") {
        document.body.style.backgroundColor = "#e3000b";  // Make the entire page background red
    } else {
        document.body.style.backgroundColor = "";     // Reset to default background if radboud is false
    }

    // Reset progress bar
    progressBar.style.transition = "none"; 
    progressBar.style.width = "0%";
    setTimeout(() => {
        progressBar.style.transition = "width 1s linear"; 
    }, 10);

    indexIndicator.textContent = `${index + 1} of ${data.length} from recent ePrints`;

    elapsedTime = 0

    interval = setInterval(() => {
        elapsedTime++;
        progressBar.style.width = `${(elapsedTime / totalTime) * 100}%`;

        if (elapsedTime >= totalTime) {
            progressBar.style.transition = "none"; 
            progressBar.style.width = "0%";
            setTimeout(() => {
                progressBar.style.transition = "width 1s linear"; 
            }, 10);
            
            clearInterval(interval);

            setTimeout(() => {
                // Move to the next object, looping back to the first one if necessary
                currentIndex = (currentIndex + 1) % data.length;
                displayObject(currentIndex, data);
            }, 10);
        }
    }, 1000); // Update every second

}

// document.addEventListener("keydown", (event) => {
//     if (event.key === "ArrowLeft") {
//         progressBar.style.transition = "none"; 

//         elapsedTime = Math.max(0, elapsedTime - 5);  // Prevent negative values
//         progressBar.style.width = `${(elapsedTime / totalTime) * 100}%`;

//         setTimeout(() => {
//             progressBar.style.transition = "width 1s linear"; 
//         }, 10);

//     } else if (event.key === "ArrowRight") {

//         progressBar.style.transition = "none"; 

//         elapsedTime = 30;
//         progressBar.style.width = `0%`;

//         setTimeout(() => {
//             progressBar.style.transition = "width 1s linear"; 
//         }, 10);

//     }
// });

