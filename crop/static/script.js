document.addEventListener("DOMContentLoaded", function () {
    // Get the form and input elements
    const form = document.querySelector("form");
    const inputs = form.querySelectorAll("input[type='text']");
    
    // Form submission handler
    form.addEventListener("submit", function (e) {
        let isValid = true;
        
        // Check if all input fields are filled
        inputs.forEach(input => {
            if (input.value === "") {
                isValid = false;
                input.style.border = "2px solid red";  // Highlight empty fields
            } else {
                input.style.border = "1px solid #ccc";  // Reset the border if filled
            }
        });
        
        // If any field is empty, prevent form submission
        if (!isValid) {
            e.preventDefault();
            alert("Please fill out all the fields.");
        }
    });
});
