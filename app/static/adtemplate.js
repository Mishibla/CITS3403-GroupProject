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
    // Replace hardcoded URLs with dynamic URLs based on ad ID
    // Assuming you have a function to fetch image URLs for the ad ID
    // Replace 'getAdImageURLs(ad_id)' with the actual function call
    var ad_id = 16; // This will get the ad ID from the rendered template
    console.log("Ad ID:", ad_id); // Log the ad ID to the console for debugging
    get_image_urls(ad_id).then(function(imageURLs) {
        $('img[data-image="image1"]').attr('src', 'uploads/16/imagetask5_.jpg');
        $('img[data-image="image2"]').attr('src', imageURLs.image2);
        $('img[data-image="image3"]').attr('src', imageURLs.image3);
        $('img[data-image="image4"]').attr('src', imageURLs.image4);
        console.error("Error fetching ad image URLs:", error);
    });
});
