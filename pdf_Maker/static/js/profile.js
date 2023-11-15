function chooseProfilePicture() {
    document.getElementById('profile-picture-input').click();
}

function displayFileName(input) {
    var fileName = input.value.split('\\').pop();  // Display the selected file name, adjust as needed
    alert('Selected file: ' + fileName);
    
    // Optionally, you can submit the form programmatically after choosing the file
    document.getElementById('profile-picture-form').submit();
}