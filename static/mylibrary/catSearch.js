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
        const slider = document.getElementById('categoryButtons');
        slider.innerHTML = `<a href="/commandes" class="btn btn-active-light-primary category-btn">
        <i class="fas fa-envelope-open-text fs-4 me-2"></i>Tous les familles
    </a>
    <a href="/commandes?cat=${category}" class="btn btn-success category-btn">
                                                                <i class="fas fa-envelope-open-text fs-4 me-2"></i>${category}
                                                            </a>
    `;
    }
}

// Event listener for input change to trigger category selection
document.getElementById('SearchCategories').addEventListener('input', redirectToCategory);

// Fetch categories and populate datalist when the page loads
window.onload = fetchCategories;



// add

function populateCart() {
    fetch('/api/tmpcart')
        .then(response => response.json())
        .then(data => {
            const tmpCart = data; // Assuming data is an array of products

            const container = document.getElementById('tempproduct');
            container.innerHTML = ''; // Clear previous content

            tmpCart.forEach((panier, index) => {
                const div = document.createElement('div');
                div.id = `div${index + 1}`;
                div.className = 'd-flex align-items-center border border-dashed rounded p-3 bg-white';

                // Set image URL based on product category
                const categoriesWithImages = ["GOBLET", "EMBALLAGE", "ELASTIQUE", "TAPIS","PRODUITSFINIS"];
                const imageUrl = panier.img ? panier.img 
                                : categoriesWithImages.includes(panier.famille) 
                                 ? `static/images_seinfa_app/${panier.famille.toLowerCase()}.jpg`
                                 : 'static/images_seinfa_app/noimageavailable.jpg';

                const thumbnail = document.createElement('a');
                thumbnail.className = 'symbol symbol-50px me-3';
                thumbnail.innerHTML = `<span class="symbol-label" style="background-image:url(${imageUrl});"></span>`;

                const details = document.createElement('div');
                details.className = 'ms-5';

                details.innerHTML = `
                    <a class="text-gray-800 text-hover-primary fs-5 fw-bolder">${panier.name}</a>
                    <div class="fw-bold fs-7"><b>Prix: <span data-kt-ecommerce-edit-order-filter="price">${panier.price} DH</b></span></div>
                    <div class="text-muted fs-7">Ref: ${panier.ref}</div>
                    <div class="text-muted fs-7">Ref: ${panier.famille}</div>
                    <div class="mt-2 d-flex align-items-center">
                        <label class="me-2">Quantité:</label>
                        <span class="me-2">${panier.qte}</span>
                        <button type="button" class="btn btn-danger btn-sm" onclick="removeProduct('${index + 1}', '${panier.name}');">
                            <i class="fas fa-trash-alt"></i>
                        </button>
                    </div>
                `;

                div.appendChild(thumbnail);
                div.appendChild(details);
                container.appendChild(div);
            });
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}


populateCart();