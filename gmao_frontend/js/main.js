
// highliting
    // Ensure the script runs after the DOM is fully loaded
    document.addEventListener('DOMContentLoaded', () => {
        const links = document.querySelectorAll('.sidebar a'); // Select all sidebar links
        const currentPage = window.location.pathname.split('/').pop(); // Get the current file name

        links.forEach(link => {
            const href = link.getAttribute('href'); // Get the href attribute of the link
            if (href === currentPage) {
                link.classList.add('active'); // Add the 'active' class if href matches currentPage
            }
        });
    });

  // loader
    // Select all links with the "link" class
    const links = document.querySelectorAll('.link');
    const loader = document.getElementById('loader');

    // Add click event to show loader
    links.forEach(link => {
        link.addEventListener('click', (event) => {
            event.preventDefault(); // Stop immediate navigation

            // Show loader
            loader.style.display = 'flex';

            // Redirect after a short delay
            setTimeout(() => {
                window.location.href = event.target.href;
            }, 200); // Adjust delay as needed
        });
    });
