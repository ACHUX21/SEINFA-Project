// Function to fetch categories from the API
function fetchCategories() {
    fetch('/api/categories')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Call function to update the datalist with categories
            populateDatalist(data);
        })
        .catch(error => {
            console.error('Error fetching categories:', error);
        });
}

// Populate datalist with categories
function populateDatalist(categories) {
    const datalist = document.getElementById('autocomplete-list-cat');
    datalist.innerHTML = ''; // Clear existing options
    categories.forEach(category => {
        const option = document.createElement('option');
        option.value = category;
        option.dataset.category = encodeURIComponent(category); // Store category as a data attribute
        datalist.appendChild(option);
    });
}

// Redirect to category page when an option is selected
function redirectToCategory() {
    const selectedCategory = document.getElementById('SearchCategories').value;
    const datalist = document.getElementById('autocomplete-list-cat');
    const selectedOption = [...datalist.options].find(option => option.value === selectedCategory);
    
    if (selectedOption) {
        const category = encodeURIComponent(selectedOption.dataset.category);
        window.location.href = `/commandes?cat=${category}`;
    }
}

// Event listener for input change to trigger category selection
document.getElementById('SearchCategories').addEventListener('input', redirectToCategory);

// Fetch categories and populate datalist when the page loads
window.onload = fetchCategories;
