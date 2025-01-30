
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

    function addRow() {
        const table = document.getElementById("spare-parts-table").getElementsByTagName('tbody')[0];
        const newRow = table.insertRow();

        const cell1 = newRow.insertCell(0);
        const cell2 = newRow.insertCell(1);
        const cell3 = newRow.insertCell(2);

        cell1.innerHTML = '<input type="text" class="form-control">';
        cell2.innerHTML = '<input type="number" class="form-control">';
        cell3.innerHTML = '<button type="button" class="btn btn-danger btn-sm" onclick="removeRow(this)">Supprimer</button>';
    }

    function removeRow(button) {
        const row = button.parentNode.parentNode;
        row.parentNode.removeChild(row);
    }

    document.getElementById("received-date").addEventListener("change", validateDates);
    document.getElementById("end-date").addEventListener("change", validateDates);

    function validateDates() {
        const receivedDate = document.getElementById("received-date").value;
        const endDate = document.getElementById("end-date").value;

        if (receivedDate && endDate && receivedDate > endDate) {
            alert("La date 'Reçu le' ne peut pas être après 'Fin le'. Veuillez corriger.");
            document.getElementById("received-date").value = "";
        }
    }