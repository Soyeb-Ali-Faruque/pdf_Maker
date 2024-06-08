document.addEventListener('DOMContentLoaded', function() {
  console.log("DOMContentLoaded event fired");
  document.getElementById('uploadForm').addEventListener('submit', function(event) {
    console.log("Form submission event fired");

    // Check if a file is selected
    const fileInput = document.getElementById('file');
    const file = fileInput.files[0];
    console.log("File selected:", file);
    if (!file) {
      alert('Please select a file before submitting.');
      event.preventDefault();
      return;
    }

    // Define the acceptable file types
    const acceptableTypes = fileAccept.split(',').map(type => type.trim().toLowerCase());
    console.log("Acceptable file types:", acceptableTypes);

    // Check the file extension
    const fileExtension = file.name.split('.').pop().toLowerCase();
    console.log("File extension:", fileExtension);
    const isAcceptable = acceptableTypes.some(type => {
      const typeWithoutDot = type.startsWith('.') ? type.slice(1) : type;
      return fileExtension === typeWithoutDot || file.type === type;
    });
    console.log("Is file type acceptable:", isAcceptable);

    if (!isAcceptable) {
      // Show the file type mismatch error message
      document.getElementById('fileTypeError').style.display = 'block';
      console.log("File type mismatch. Error message displayed.");
      event.preventDefault();
      return;
    } else {
      // Hide the file type mismatch error message if file type is acceptable
      document.getElementById('fileTypeError').style.display = 'none';
      console.log("File type is acceptable. Error message hidden.");
    }

   

    // Show the loading message
    document.getElementById('loadingMessage').style.display = 'block';
    console.log("Loading message displayed.");
    
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
      console.log("Response status:", xhr.status);
      
      if (xhr.status === 200 || xhr.status === 204) {
        document.getElementById('loadingMessage').style.display = 'none';
        console.log("Loading message hidden.");
        document.getElementById('downloadingMessage').style.display = 'block';
        console.log("Downloading message displayed.");

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
          console.log("Downloading message hidden.");
          
          clearInterval(interval);

          // Optionally show the generated message after a few seconds
          setTimeout(() => {
            document.getElementById('generatedMessage').style.display = 'block';
            console.log("Generated message displayed.");
            setTimeout(() => {
              document.getElementById('generatedMessage').style.display = 'none';
              console.log("Generated message hidden.");
            }, 5000);
          }, 0);
        } else {
          console.log("Content-Disposition header is missing.");
          // Hide the downloading message and show the generated message
          document.getElementById('downloadingMessage').style.display = 'none';
          console.log("Downloading message hidden.");

          // Show the generated message
          document.getElementById('generatedMessage').style.display = 'block';
          console.log("Generated message displayed.");
          
          clearInterval(interval);

          // Optionally hide the generated message after a few seconds
          setTimeout(() => {
            document.getElementById('generatedMessage').style.display = 'none';
            console.log("Generated message hidden.");
          }, 5000);
        }
      } else {
        // Handle bad request error (file type mismatch)
        document.getElementById('fileTypeError').style.display = 'block';
        console.log("File type mismatch. Error message displayed.");
        // Hide the loading message in case of error
        document.getElementById('loadingMessage').style.display = 'none';
        console.log("Loading message hidden.");
        clearInterval(interval);
      }
    };
    xhr.send(new FormData(this));
    
    // Prevent the default form submission
    event.preventDefault();
  });
});
