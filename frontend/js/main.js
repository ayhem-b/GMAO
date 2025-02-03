document.addEventListener("DOMContentLoaded", () => {
    // ✅ Sidebar Link Highlighting
    const links = document.querySelectorAll('.sidebar a');
    const currentPage = window.location.pathname.split('/').pop();

    links.forEach(link => {
        if (link.getAttribute('href') === currentPage) {
            link.classList.add('active');
        }
    });

    // ✅ Loader Animation
    const pageLinks = document.querySelectorAll('.link');
    const loader = document.getElementById('loader');

    if (pageLinks.length && loader) {
        pageLinks.forEach(link => {
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
    }

    // ✅ Add & Remove Table Rows
    const addRow = () => {
        const table = document.getElementById("spare-parts-table").getElementsByTagName('tbody')[0];
        const newRow = table.insertRow();

        newRow.innerHTML = `
            <td><input type="text" class="form-control"></td>
            <td><input type="number" class="form-control"></td>
            <td><button type="button" class="btn btn-danger btn-sm" onclick="removeRow(this)">Supprimer</button></td>
        `;
    };

    window.addRow = addRow; // Ensure function is accessible globally

    const removeRow = (button) => {
        button.closest("tr").remove();
    };

    window.removeRow = removeRow;

    // ✅ Date Validation
    const receivedDateInput = document.getElementById("received-date");
    const endDateInput = document.getElementById("end-date");

    if (receivedDateInput && endDateInput) {
        receivedDateInput.addEventListener("change", validateDates);
        endDateInput.addEventListener("change", validateDates);
    }

    function validateDates() {
        const receivedDate = receivedDateInput.value;
        const endDate = endDateInput.value;

        if (receivedDate && endDate && receivedDate > endDate) {
            alert("La date 'Reçu le' ne peut pas être après 'Fin le'. Veuillez corriger.");
            receivedDateInput.value = "";
        }
    }

    // ✅ Fullscreen Feature
    const fullscreenBtn = document.getElementById('fullscreen-btn');
    const fullscreenIcon = document.getElementById('fullscreen-icon');

    if (fullscreenBtn && fullscreenIcon) {
        fullscreenBtn.addEventListener('click', () => {
            const elem = document.documentElement;

            if (!document.fullscreenElement) {
                elem.requestFullscreen()
                    .then(() => fullscreenIcon.classList.replace('fa-expand', 'fa-compress'))
                    .catch(err => console.error("Error entering fullscreen:", err));
            } else {
                document.exitFullscreen()
                    .then(() => fullscreenIcon.classList.replace('fa-compress', 'fa-expand'))
                    .catch(err => console.error("Error exiting fullscreen:", err));
            }
        });
    } else {
        console.error("Fullscreen button or icon not found!");
    }
});
