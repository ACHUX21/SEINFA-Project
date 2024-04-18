document.addEventListener('DOMContentLoaded', function() {
    fetch("/api/clients")
        .then(response => response.json())
        .then(data => {
            initializeAutocomplete(data);
        });
});

function initializeAutocomplete(clients) {
    const input = document.getElementById('clientInput');
    const autocompleteList = document.getElementById('autocompleteList');

    input.addEventListener('input', function() {
        const value = this.value;
        autocompleteList.innerHTML = '';
        if (!value) { return; }

        clients
            .filter(client => client.CT_INTITULE.toLowerCase().includes(value.toLowerCase()))
            .forEach(client => {
                const item = document.createElement('div');
                item.textContent = client.CT_INTITULE;
                item.classList.add('cursor-pointer', 'p-2');
                item.addEventListener('click', function() {
                    input.value = client.CT_INTITULE;
                    input.setAttribute('data-value', client.CT_NUM);
                    autocompleteList.innerHTML = '';
                });
                autocompleteList.appendChild(item);
            });
    });
}
    function SelectCategory(category) {
        
        const tbody = document.getElementById('ppp');
        if (tbody) {
            tbody.remove();
        }

        
        fetch(`/api/products/20?cat=${category}`)
            .then(response => response.json())
            .then(data => {
                
                const newTbody = document.createElement('tbody');
                newTbody.setAttribute('id', 'ppp');
                newTbody.classList.add('fw-bold', 'text-gray-600');

                
                data.forEach(product => {
                    newTbody.innerHTML += `
                        <tr>
                            <td>
                                <div class="form-check form-check-sm form-check-custom form-check-solid">
                                    <input class="form-check-input" type="checkbox" value="1" />
                                </div>
                            </td>
                            <td>
                                <div class="d-flex align-items-center">
                                    <a class="symbol symbol-50px">
                                        <span class="symbol-label" style="background-image:url(${product.image});"></span>
                                    </a>
                                    <div class="ms-5">
                                        <a class="text-gray-800 text-hover-primary fs-5 fw-bolder">${product.name}</a>
                                        <div class="fw-bold fs-7">Prix: DH
                                            <span>${product.price}</span>
                                        </div>
                                        <div class="text-muted fs-7">Ref: ${product.ref}</div>
                                    </div>
                                </div>
                            </td>
                            <td class="text-end pe-5" data-order="0">
                                ${product.qte > 0 && product.qte < 10 ? `<span class="badge badge-light-danger" style="color: orange;">Presque épuisé ${product.qte}</span>` :
                                    (product.qte == 0 ? `<span class="badge badge-light-danger" style="color: red;">Épuisé ${product.qte}</span>` :
                                        `<span class="badge badge-light-danger" style="color: green;">Disponible ${product.qte}</span>`)}
                            </td>
                        </tr>
                    `;
                });

                
                document.querySelector('table').appendChild(newTbody);
            })
            .catch(error => console.error('Error fetching data:', error));
    }


    

    function submitForm(name, price, ref,category) {
        const buttonId = 'productButton' + ref; // Make sure this ID is correctly generated.
        console.log("Looking for button with ID:", buttonId); // Debug to see the actual ID being generated
    
        const button = document.getElementById(buttonId);
        if (!button) {
            console.error('Button not found with ID:', buttonId);
            return; // Exit the function if the button is not found
        }
    
        const spinner = button.querySelector('.spinner-border');
        if (!spinner) {
            console.error('Spinner not found in button with ID:', buttonId);
            return; // Exit the function if spinner is not found
        }
        
        spinner.style.display = 'inline-block'; // Show the spinner
    
        const qteId = 'qte-' + name;
        console.log("Looking for quantity input with ID:", qteId); // Debug to confirm the ID
        const qte = document.getElementById(qteId) ? document.getElementById(qteId).value : '1'; // Default to '1' if not found
        console.log("Quantity:", qte); // Log the quantity
    
        const formData = {
            name: name,
            price: price,
            ref: ref,
            qte: qte,
            category: category
        };
    
        fetch('/addToCart', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Data successfully sent to /addToCart:', data);
            spinner.style.display = 'none'; // Hide the spinner
        })
        .catch(error => {
            console.error('Error sending data to /addToCart:', error);
            spinner.style.display = 'none'; // Hide the spinner
        });
    
        setTimeout(() => {
            populateCart();
        }, 500);
        
        
        setTimeout(() => {
            fetchTotal();
        }, 500);
        
    }
    
    
function removeProduct(id, name) {
    
    fetch(`/removeFromCart`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({name: name})
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Data successfully sent to /removeFromCart:', data);
        
    })
    .catch(error => {
        console.error('Error sending data to /removeFromCart:', error);
        
    });

    
    document.getElementById("div" + id).remove();

    setTimeout(() => {
        fetchTotal();
    }, 100);
    

}
function saveInputs() { localStorage.setItem("clientInputValue", document.querySelector(".clientInput").value); localStorage.setItem("refInputValue", document.querySelector(".refInput").value); localStorage.setItem("dateInputValue", document.querySelector(".kt_ecommerce_edit_order_date").value); } window.onload = function() { restoreInputs(); }; document.querySelector(".clientInput").addEventListener("input", saveInputs); document.querySelector(".refInput").addEventListener("input", saveInputs); document.querySelector(".kt_ecommerce_edit_order_date").addEventListener("input", saveInputs);
function restoreInputs() { document.querySelector(".clientInput").value = localStorage.getItem("clientInputValue"); document.querySelector(".refInput").value = localStorage.getItem("refInputValue"); document.querySelector(".kt_ecommerce_edit_order_date").value = localStorage.getItem("dateInputValue"); } window.onload = function() { restoreInputs(); }; document.querySelector(".clientInput").addEventListener("input", saveInputs); document.querySelector(".refInput").addEventListener("input", saveInputs); document.querySelector(".kt_ecommerce_edit_order_date").addEventListener("input", saveInputs);




function fetchTotal() {
    // Fetch the total price from the backend API
    fetch('/api/total')
      .then(response => response.json())
      .then(data => {
        console.log('Total price:', data);
        document.getElementById('totalPrice').textContent = data.total;
      })
      .catch(error => {
        console.error('Error fetching total price:', error);
      });
  }

  setTimeout(() => {
    fetchTotal();
}, 500);


