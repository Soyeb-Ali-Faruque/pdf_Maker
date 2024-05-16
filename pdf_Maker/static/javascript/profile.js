document.addEventListener('DOMContentLoaded', function () {
    // Function to trigger file input click and show the upload button
    function chooseProfilePicture() {
        document.getElementById('profile-picture-input').click();
        document.getElementById('upload-button').style.display = 'block'; // Show the upload button
    }

    // Function to display file name and preview the selected image
    function displayFileName(input) {
        const file = input.files[0];
        if (file) {
            const fileType = file.type.split('/')[0];
            if (fileType === 'image') {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const profilePicture = document.getElementById('profile-picture');
                    profilePicture.style.backgroundImage = `url(${e.target.result})`;
                };
                reader.readAsDataURL(file);
            } else {
                alert('Please select an image file.');
                input.value = ''; // Clear the file input
            }
        }
    }

    // Event listener for the upload button
    document.getElementById('upload-button').addEventListener('click', function() {
        document.getElementById('profile-picture-form').submit();
    });

    // Your other functions and code specific to your functionality can be added here
});