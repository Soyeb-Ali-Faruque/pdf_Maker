document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('uploadForm').addEventListener('submit', function(event) {

    // Check if a file is selected
    const fileInput = document.getElementById('file');
    const file = fileInput.files[0];
    if (!file) {
      alert('Please select a file before submitting.');
      event.preventDefault();
      return;
    }

    // Define the acceptable file types
    const acceptableTypes = fileAccept.split(',').map(type => type.trim().toLowerCase());

    // Check the file extension
    const fileExtension = file.name.split('.').pop().toLowerCase();
    const isAcceptable = acceptableTypes.some(type => {
      const typeWithoutDot = type.startsWith('.') ? type.slice(1) : type;
      return fileExtension === typeWithoutDot || file.type === type;
    });

    if (!isAcceptable) {
      // Show the file type mismatch error message
      document.getElementById('fileTypeError').style.display = 'block';
      event.preventDefault();
      return;
    } else {
      // Hide the file type mismatch error message if file type is acceptable
      document.getElementById('fileTypeError').style.display = 'none';
    }

    // Show the loading message
    document.getElementById('loadingMessage').style.display = 'block';

    // Create a simple loading animation
    let dots = 0;
    const loadingDots = document.getElementById('loadingDots');
    const interval = setInterval(() => {
      dots = (dots + 1) % 4;
      loadingDots.textContent = '.'.repeat(dots);
    }, 500);

    // Handle the form submission via AJAX
    const xhr = new XMLHttpRequest();
    xhr.open(this.method, this.action, true);
    xhr.responseType = 'blob';
    xhr.onload = function() {
      if (xhr.status === 200 || xhr.status === 204) {
        document.getElementById('loadingMessage').style.display = 'none';
        document.getElementById('downloadingMessage').style.display = 'block';

        const contentDisposition = xhr.getResponseHeader('Content-Disposition');
        if (contentDisposition) {
          const fileName = contentDisposition
            .split(';')[1]
            .trim()
            .split('=')[1]
            .replace(/"/g, '');

          const link = document.createElement('a');
          link.href = URL.createObjectURL(xhr.response);
          link.download = fileName;  // Set the file name
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);

          // Hide the downloading message
          document.getElementById('downloadingMessage').style.display = 'none';

          clearInterval(interval);

          // Optionally show the generated message after a few seconds
          setTimeout(() => {
            document.getElementById('generatedMessage').style.display = 'block';
            setTimeout(() => {
              document.getElementById('generatedMessage').style.display = 'none';
            }, 5000);
          }, 0);
        } else {
          // Hide the downloading message and show the generated message
          document.getElementById('downloadingMessage').style.display = 'none';

          // Show the generated message
          document.getElementById('generatedMessage').style.display = 'block';

          clearInterval(interval);

          // Optionally hide the generated message after a few seconds
          setTimeout(() => {
            document.getElementById('generatedMessage').style.display = 'none';
          }, 5000);
        }
      } else {
        // Handle bad request error (file type mismatch)
        document.getElementById('fileTypeError').style.display = 'block';
        // Hide the loading message in case of error
        document.getElementById('loadingMessage').style.display = 'none';
        clearInterval(interval);
      }
    };
    xhr.send(new FormData(this));
    
    // Prevent the default form submission
    event.preventDefault();
  });
});
