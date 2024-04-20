function uploadImageAndSubmit() {
    // Perform upload image functionality here
    // For example, you can call a function named 'uploadImage()' if needed


    // Show the hidden submit button
    document.getElementById('submitButton').style.display = 'inline-block';

    // Optionally, you can disable the upload button after clicking
    this.disabled = true; // Assuming 'this' refers to the upload button
    uploadImage();
}

function uploadImage() {
    // Get the base64 data from the style attribute
    const imageDiv = document.querySelector('.image-input-wrapper');
    const backgroundImage = imageDiv.style.backgroundImage;

    // Extract base64 data
    const base64Data = backgroundImage.replace(/^url\(["']?/, '').replace(/["']?\)$/, '');

    // Get the value of the input field
    const userName = document.querySelector('input[name="user_name"]').value;

    // Send the base64 data and username to Flask app
    fetch('/upload_pic', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
            image: base64Data,
            username: userName
        })
    })
    .then(response => {
        if (response.ok) {
            console.log('Image uploaded successfully');
        } else {
            console.error('Image upload failed');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}