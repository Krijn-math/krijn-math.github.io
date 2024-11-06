let currentIndex = 0;

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

    document.getElementById("name").textContent = obj.name;

    // Add animation for smooth transition between objects
    const contentContainer = document.getElementById("content-container");
    contentContainer.classList.remove("show");  // Hide content
    setTimeout(() => {
        contentContainer.classList.add("show");  // Show new content after fade out
    }, 500);  // Wait for 0.5s before showing new content
}

function cycleThroughObjects(data) {
    displayObject(currentIndex, data);

    // Move to the next object every 5 seconds
    currentIndex = (currentIndex + 1) % data.length;  // Wrap back to the first object when done

    setTimeout(() => cycleThroughObjects(data), 20000);  // 5-second interval
}
