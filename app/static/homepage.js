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
    
        document.addEventListener('DOMContentLoaded', function() {
        const ads = {{ ads|tojson }};
        const fileExtensions = ['jpg', 'jpeg', 'png'];
        
        ads.forEach((ad, index) => {
            const adId = ad.ad_id;
            const imageElement = document.querySelector(`div[data-image="image${index + 1}"]`);
            if (imageElement) {
                for (const extension of fileExtensions) {
                    const imageUrl = `/static/uploads/${adId}/${adId}_1.${extension}`;
                    fetch(imageUrl).then(response => {
                        if (response.ok) {
                            imageElement.style.backgroundImage = `url('${imageUrl}')`;
                        }
                    });
                }
            }
        });
    });

    // Toggle dropdown content
    document.getElementById('expandButton').addEventListener('click', function() {
        var content = document.getElementById('dropdownContent');
        if (content.classList.contains('show')) {
            content.classList.remove('show');
        } else {
            content.classList.add('show');
        }
    });
    