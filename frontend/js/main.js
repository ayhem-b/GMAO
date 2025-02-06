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



document.addEventListener("DOMContentLoaded", function () {
    // 1️⃣ Interventions par type de panne
    new Chart(document.getElementById("interventionChart"), {
        type: "bar",
        data: {
            labels: ["Mécanique", "Électrique", "Logiciel", "Hydraulique", "Pneumatique"],
            datasets: [{
                label: "Nombre d'interventions",
                data: [12, 19, 7, 5, 9],
                backgroundColor: "rgba(220, 53, 69, 0.7)",
                borderColor: "rgba(220, 53, 69, 1)",
                borderWidth: 1
            }]
        },
        options: { responsive: true, scales: { y: { beginAtZero: true } } }
    });

    // 2️⃣ État des machines
    new Chart(document.getElementById("machineStatusChart"), {
        type: "pie",
        data: {
            labels: ["En marche", "En panne", "Maintenance"],
            datasets: [{
                data: [60, 25, 15],
                backgroundColor: ["#28a745", "#dc3545", "#ffc107"]
            }]
        },
        options: { responsive: true }
    });

    // 3️⃣ Nombre d’interventions par mois
    new Chart(document.getElementById("monthlyInterventionChart"), {
        type: "line",
        data: {
            labels: ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin", "Juil", "Août", "Sept", "Oct", "Nov", "Déc"],
            datasets: [{
                label: "Interventions",
                data: [5, 10, 8, 12, 15, 10, 14, 18, 16, 20, 22, 25],
                borderColor: "#dc3545",
                fill: false
            }]
        },
        options: { responsive: true }
    });

    // 4️⃣ Répartition des interventions par technicien
    new Chart(document.getElementById("technicianInterventionChart"), {
        type: "doughnut",
        data: {
            labels: ["Jean", "Luc", "Marie", "Sophie"],
            datasets: [{
                data: [10, 15, 12, 8],
                backgroundColor: ["#dc3545", "#28a745", "#ffc107", "#007bff"]
            }]
        },
        options: { responsive: true }
    });

    // 5️⃣ Durée moyenne des interventions
    new Chart(document.getElementById("avgDurationChart"), {
        type: "radar",
        data: {
            labels: ["Mécanique", "Électrique", "Logiciel", "Hydraulique", "Pneumatique"],
            datasets: [{
                label: "Durée (min)",
                data: [45, 30, 60, 40, 35],
                backgroundColor: "rgba(220, 53, 69, 0.5)",
                borderColor: "#dc3545"
            }]
        },
        options: { responsive: true }
    });

    // 6️⃣ Demandes en attente vs résolues
    new Chart(document.getElementById("pendingVsResolvedChart"), {
        type: "bar",
        data: {
            labels: ["En attente", "Résolues"],
            datasets: [{
                label: "Demandes",
                data: [20, 45],
                backgroundColor: ["#ffc107", "#28a745"]
            }]
        },
        options: { responsive: true, scales: { y: { beginAtZero: true } } }
    });
});


