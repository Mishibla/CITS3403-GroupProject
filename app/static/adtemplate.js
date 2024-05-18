function openModal() {
    document.getElementById("myModal").style.display = "block";
}

function closeModal() {
    document.getElementById("myModal").style.display = "none";
}

var slideIndex = 1;
showSlides(slideIndex);

function plusSlides(n) {
    showSlides(slideIndex += n);
}

function currentSlide(n) {
    showSlides(slideIndex = n);
}

function showSlides(n) {
    var i;
    var slides = document.getElementsByClassName("mySlides");
    if (n > slides.length) {slideIndex = 1}
    if (n < 1) {slideIndex = slides.length}
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    slides[slideIndex-1].style.display = "block";
}

$(document).ready(function() {
    $('img[data-image="image1"]').attr('src', 'https://oyster.ignimgs.com/mediawiki/apis.ign.com/valorant/e/ec/Phantom.png?width=1280');
    $('img[data-image="image2"]').attr('src', 'https://static1.thegamerimages.com/wordpress/wp-content/uploads/2023/07/onimaru-kunitsuna-valorant.jpg');
    $('img[data-image="image3"]').attr('src', 'https://cdn.thespike.gg/Luke%2Fsoveriegn_guardian_rare_valorant_skins_rifles_1689950159933.jpg');
    $('img[data-image="image4"]').attr('src', 'https://www.cnet.com/a/img/resize/85aa642126780beeeb22809375b4bf2c6509f99e/hub/2021/09/02/1511ef05-2457-4272-918d-6719d4897e65/beta-key-art-valorant.jpg?auto=webp&fit=crop&height=900&width=1200');
});


