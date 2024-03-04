 // Fetch current file size and update the input field
 document.getElementById('file').addEventListener('change', function () {
    var fileInput = document.getElementById('file');
    var fileSizeInput = document.getElementById('currentFileSize');
    if (fileInput.files.length > 0) {
        var fileSizeKB = fileInput.files[0].size / 1024; // Convert bytes to kilobytes
        var fileSizeMB = fileSizeKB / 1024; // Convert kilobytes to megabytes
        if (fileSizeKB < 1024) {
            fileSizeInput.value = fileSizeKB.toFixed(2) + ' KB';
            document.getElementById('unit').innerHTML = '<option value="KB" selected>KB</option>';
        } else {
            fileSizeInput.value = fileSizeMB.toFixed(2) + ' MB';
            document.getElementById('unit').innerHTML = '<option value="KB">KB</option><option value="MB" selected>MB</option>';
        }
    } else {
        fileSizeInput.value = '';
    }
});

// Validate target size input
document.getElementById('targetSize').addEventListener('input', function () {
    var targetSizeInput = document.getElementById('targetSize');
    var currentFileSizeInput = document.getElementById('currentFileSize');
    var targetSizeHelpBlock = document.getElementById('targetSizeHelpBlock');
    
    var targetSize = parseFloat(targetSizeInput.value);
    var currentFileSize = parseFloat(currentFileSizeInput.value);
    
    if (targetSize < 0) {
        targetSizeInput.value = 0;
    }
    
    if (targetSize > currentFileSize) {
        targetSizeHelpBlock.classList.remove('d-none');
    } else {
        targetSizeHelpBlock.classList.add('d-none');
    }
});

// Prevent form submission if target size is invalid
document.querySelector('form').addEventListener('submit', function(event) {
    var targetSizeInput = document.getElementById('targetSize');
    var currentFileSizeInput = document.getElementById('currentFileSize');
    
    var targetSize = parseFloat(targetSizeInput.value);
    var currentFileSize = parseFloat(currentFileSizeInput.value);
    
    if (targetSize > currentFileSize) {
        event.preventDefault(); // Prevent form submission
        var targetSizeHelpBlock = document.getElementById('targetSizeHelpBlock');
        targetSizeHelpBlock.classList.remove('d-none'); // Show error message
    }
});