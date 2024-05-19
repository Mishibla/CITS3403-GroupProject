    // Function to open the modal
    function openModal(id) {
        document.getElementById(id).style.display = "block";
    }

    // Function to close the modal
    function closeModal(id) {
        document.getElementById(id).style.display = "none";
    }

    // Close modal when clicking outside of it
    window.onclick = function(event) {
        var modals = document.getElementsByClassName('modal');
        for (var i = 0; i < modals.length; i++) {
            if (event.target == modals[i]) {
                modals[i].style.display = "none";
            }
        }
    }

    // Toggle dropdown content
    document.getElementById('expandButton').addEventListener('click', function() {
        var content = document.getElementById('dropdownContent');
        if (content.classList.contains('show')) {
            content.classList.remove('show');
        } else {
            content.classList.add('show');
        }
    });