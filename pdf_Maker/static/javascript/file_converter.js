document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('uploadForm').addEventListener('submit', function(event) {
    // Check if a file is selected
    const fileInput = document.getElementById('file');
    if (!fileInput.value) {
      alert('Please select a file before submitting.');
      event.preventDefault();
      return;
    }
    
    // Show the loading message
    document.getElementById('loadingMessage').style.display = 'block';
    
    // Show the file type mismatch error message if needed
    document.getElementById('fileTypeError').style.display = 'none';
    
    // Create a simple loading animation
    let dots = 0;
    const loadingDots = document.getElementById('loadingDots');
    const interval = setInterval(() => {
      dots = (dots + 1) % 4;
      loadingDots.textContent = '.'.repeat(dots);
    }, 500);

    // Hide the loading message and show the downloading message when the download starts
    const xhr = new XMLHttpRequest();
    xhr.open(this.method, this.action, true);
    xhr.responseType = 'blob';
    xhr.onload = function() {
      if (xhr.status === 200) {
        document.getElementById('loadingMessage').style.display = 'none';
        document.getElementById('downloadingMessage').style.display = 'block';

        const fileName = xhr.getResponseHeader('Content-Disposition')
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

        // Hide the downloading message and show the completed message
        document.getElementById('downloadingMessage').style.display = 'none';
        document.getElementById('completedMessage').style.display = 'block';

        clearInterval(interval);

        // Hide the completed message after a few seconds
        setTimeout(() => {
          document.getElementById('completedMessage').style.display = 'none';
        }, 5000);
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
