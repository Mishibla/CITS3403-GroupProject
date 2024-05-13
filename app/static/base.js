$(document).ready(function() {
    $('#sellButton').click(function() {
        var url = $(this).data('url');  // Assuming you've set a data-url attribute
        window.location.href = url;
    });
    $('#usersignin').click(function() {
        var url = $(this).data('url');  // Assuming you've set a data-url attribute
        window.location.href = url;
    });
    $('#sign_in').click(function() {
        var url = $(this).data('url');  // Assuming you've set a data-url attribute
        window.location.href = url;
    });
    $('#buy').click(function() {
        var url = $(this).data('url');  // Assuming you've set a data-url attribute
        window.location.href = url;
    });
});

