// Function to validate form example
function validateForm() {
    var location = document.getElementById("location").value;
    if (location.trim() === "") {
        alert("Please fill in location field.");
        return false;
    }
    return true;
}

