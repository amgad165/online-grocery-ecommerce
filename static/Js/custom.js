$(document).ready(function() {
    $('#signupForm').submit(function(event) {
        event.preventDefault(); // Prevent default form submission
        
        // Collect form data
        var formData = $(this).serialize();
        
        // Send AJAX request
        $.ajax({
            type: 'POST',
            url: '/signup/', 
            data: formData,
            dataType: 'json',
            success: function(response) {
                
                    if (response.waiting_acceptance) {
                        // Create an alert if waiting for acceptance
                        alert(response.waiting_acceptance);
                    }

                    window.location.href = '';
                
            },
            error: function(xhr, status, error) {
                // Handle error if AJAX request fails
                console.error(xhr.responseText);
                
                // Parse the JSON response
                var response = JSON.parse(xhr.responseText);
                
                // Check if the response contains an error message
                if (response.error) {
                    // Extract the error message
                    var errorMessage = response.error;
                    
                    // Display the error message in the error-container div
                    $('#error-container').empty().append('<p class="text-danger">' + errorMessage + '</p>');
                } else {
                    // Display a generic error message if the response does not contain an error
                    $('#error-container').empty().append('<p class="text-danger">An error occurred. Please try again.</p>');
                }
            }
        });
    });
});




$(document).ready(function() {
    $('#loginForm').submit(function(event) {
        event.preventDefault(); // Prevent default form submission
        
        // Collect form data
        var formData = $(this).serialize();
        
        // Send AJAX request
        $.ajax({
            type: 'POST',
            url: '/login/', // Replace '/login/' with your login URL
            data: formData,
            dataType: 'json',
            success: function(response) {
                // Redirect to success page or perform other actions
                window.location.href = '';
            },
            error: function(xhr, status, error) {
                // Handle error if AJAX request fails
                console.error(xhr.responseText);
                
                // Parse the JSON response
                var response = JSON.parse(xhr.responseText);
                
                // Check if the response contains an error message
                if (response.error) {
                    // Extract the error message
                    var errorMessage = response.error;
                    
                    // Display the error message in the error-container div
                    $('#loginErrorContainer').empty().append('<p class="text-danger">' + errorMessage + '</p>');
                } else {
                    // Display a generic error message if the response does not contain an error
                    $('#loginErrorContainer').empty().append('<p class="text-danger">An error occurred. Please try again.</p>');
                }
            }
        });
    });
});


