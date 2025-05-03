document.addEventListener("DOMContentLoaded", () => {
        const links = document.querySelectorAll('.sidebar .nav-link');
        const currentPath = window.location.pathname; // Get full path
    
        links.forEach(link => {
            if (link.getAttribute('href') === currentPath) {
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

$(document).ready(function(){
    // Search Functionality
    $("#search").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#userTable tr").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
        });
    });

    // Sorting Functionality
    $(".sort").click(function() {
        var table = $("table tbody");
        var rows = table.find("tr").toArray().sort((a, b) => {
            var textA = $(a).find("td:nth-child(2)").text();
            var textB = $(b).find("td:nth-child(2)").text();
            return textA.localeCompare(textB);
        });
        table.append(rows);
    });

    // Edit User Modal Setup
    $(".edit-user").click(function() {
        let userId = $(this).data("id");
        let first_name = $(this).data("first_name");
        let username = $(this).data("username");
        let email = $(this).data("email");
        let role = $(this).data("role");
        $("#editfirst_name").val(first_name);
        $("#editUserId").val(userId);
        $("#editUsername").val(username);
        $("#editEmail").val(email);
        $("#editRole").val(role);
    });

    // Edit User Form Submission
    $("#editUserForm").submit(function(e) {
        e.preventDefault();
        let formData = $(this).serialize();

        $.ajax({
            type: "POST",
            url: "/edit-user/",
            data: formData,
            success: function(response) {
                location.reload();
            },
            error: function(xhr, status, error) {
                alert("Failed to update user.");
            }
        });
    });

    // Delete User
    $(".delete-user").click(function() {
        let userId = $(this).data("id");
        if (confirm("Are you sure you want to delete this user?")) {
            $.ajax({
                type: "POST",
                url: "/delete-user/",
                data: {
                    "user_id": userId,
                    "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val()
                },
                success: function(response) {
                    location.reload();
                },
                error: function(xhr, status, error) {
                    alert("Failed to delete user.");
                }
            });
        }
    });
});


// charts js

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
                data: [25, 10, 8, 12, 15, 30, 24, 18, 16, 20, 22, 25],
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
            labels: ["Ayhem", "Samar", "Nour", "chiheb"],
            datasets: [{
                data: [30, 15, 12, 8],
                backgroundColor: ["#dc3545", "#007bff", "#28a745", "#ffc107"]
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
                data: [45, 35, 60, 40, 35],
                backgroundColor: "rgba(220, 53, 69, 0.5)",
                borderColor: "#dc3545"
            }]
        },
        options: { responsive: true ,}
    });

    // 6️⃣ Demandes en attente vs résolues
    new Chart(document.getElementById("pendingVsResolvedChart"), {
        type: "bar",
        data: {
            labels: ["En attente", "Résolues"],
            datasets: [{
                label: "Demandes",
                data: [45,41],
                backgroundColor: ["#ffc107", "#28a745"]
            }]
        },
        options: { responsive: true, scales: { y: { beginAtZero: true } } }
    });
});


