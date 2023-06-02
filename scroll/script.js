// Scroll the content horizontally
function autoScroll() {
  const scrollContainer = document.getElementById('scroll-container');
  scrollContainer.scrollLeft += 1; // Adjust scroll speed as needed
}

setInterval(autoScroll, 10); // Adjust scroll speed as needed
