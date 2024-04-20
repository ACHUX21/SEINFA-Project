document.getElementById("SubBtn").addEventListener("click", function(event) {
    event.preventDefault(); // Prevent the default form submission

    var userid = document.getElementById("user_id_select").value;
    var checkedDepots = []; // Array to store checked depot values

    // Get all checkboxes with class "depot-checkbox"
    var checkboxes = document.querySelectorAll('.depot-checkbox');

    // Iterate over each checkbox
    checkboxes.forEach(function(checkbox) {
        // If checkbox is checked, add its value to checkedDepots array
        if (checkbox.checked) {
            checkedDepots.push(checkbox.value);
        }
    });

    // Now checkedDepots array contains all the checked checkbox values
    fetch('/api/user_depots/' + userid, { // Corrected endpoint URL
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            depots: checkedDepots
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Handle successful response here
        console.log(data);
        
        // Reload the page after fetch operation is completed
        window.location.reload();
    })
    .catch(error => {
        // Handle errors here
        console.error('There was a problem with the fetch operation:', error);
    });
});
