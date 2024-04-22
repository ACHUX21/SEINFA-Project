function autocomplete(input, products) {
    var currentFocus;

    
    input.addEventListener("input", function(e) {
        var val = this.value;
        closeAllLists();
        if (!val || val.length < 4) { return false;}
        currentFocus = -1;

        
        var a = document.createElement("div");
        a.setAttribute("id", this.id + "autocomplete-list");
        a.setAttribute("class", "autocomplete-items");
        
        this.parentNode.appendChild(a);

        
        for (var i = 0; i < products.length; i++) {
            if (products[i].AR_Ref.substr(0, val.length).toUpperCase() == val.toUpperCase() ||
                products[i].AR_Design.substr(0, val.length).toUpperCase() == val.toUpperCase()) {
                var b = document.createElement("div");
                b.innerHTML = "<strong>" + products[i].AR_Design.substr(0, val.length) + "</strong>";
                b.innerHTML += products[i].AR_Design.substr(val.length);
                b.innerHTML += "<input type='hidden' value='" + products[i].AR_Design + "'>";
                
                
                (function(index) {
                    b.addEventListener("click", function(e) {
                        input.value = this.getElementsByTagName("input")[0].value;
                        removeAndreplace(products[index].AR_Ref);
                        closeAllLists();
                    });
                })(i);
                
                a.appendChild(b);
            }
        }
    });

    
    input.addEventListener("keydown", function(e) {
        var x = document.getElementById(this.id + "autocomplete-list");
        if (x) x = x.getElementsByTagName("div");
        if (e.keyCode == 40) {
            
            currentFocus++;
            
            addActive(x);
        } else if (e.keyCode == 38) { //up
            
            currentFocus--;
            
            addActive(x);
        } else if (e.keyCode == 13) {
            
            e.preventDefault();
            if (currentFocus > -1) {
                
                if (x) x[currentFocus].click();
            }
        }
    });

    function addActive(x) {
        
        if (!x) return false;
        
        removeActive(x);
        if (currentFocus >= x.length) currentFocus = 0;
        if (currentFocus < 0) currentFocus = (x.length - 1);
        
        x[currentFocus].classList.add("autocomplete-active");
    }

    function removeActive(x) {
        
        for (var i = 0; i < x.length; i++) {
            x[i].classList.remove("autocomplete-active");
        }
    }

    function closeAllLists(elmnt) {
        
        var x = document.getElementsByClassName("autocomplete-items");
        for (var i = 0; i < x.length; i++) {
            if (elmnt != x[i] && elmnt != input) {
                x[i].parentNode.removeChild(x[i]);
            }
        }
    }

    
    document.addEventListener("click", function (e) {
        closeAllLists(e.target);
    });
}

function fetchDataFromAPI() {
    fetch('/api/search')
        .then(response => response.json())
        .then(data => {
            
            var apiProducts = data.map(item => ({
                AR_Ref: item.AR_Ref,
                AR_Design: item.AR_Design
            }));
            var allProducts = products.concat(apiProducts);

            
            autocomplete(document.getElementById("searchNOW"), allProducts);


        })
        .catch(error => console.error('Error fetching data:', error));
}


var products = [];

function removeAndreplace(AR_Ref) {
    var table = document.getElementById("kt_ecommerce_edit_order_product_table");

    fetch(`/api/search?q=${AR_Ref}`)
        .then(response => response.json())
        .then(data => {
            const product = data[0];
            const imageUrl = product.img
            ? product.img
            : ["GOBLET", "EMBALLAGE", "ELASTIQUE", "TAPIS", "PRODUITSFINIS"].includes(product.category) 
                ? `static/images_seinfa_app/${product.category.toLowerCase()}.jpg`
                : 'static/images_seinfa_app/noimageavailable.jpg';

            table.innerHTML = `
                <form id="form${product.ref}" method="POST" action="/addToCart">
                    <tbody id="ppp" class="fw-bold text-gray-600">
                        <tr>
                            <td>
                                <div class="form-check form-check-sm form-check-custom form-check-solid">
                                    <button type="button" class="btn btn-primary btn-sm" onclick="submitForm('${product.name}', '${product.price}', '${product.ref}');" id="productButton${product.ref}">
                                        <i class="fas fa-plus"></i>
                                        <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true" style="display: none;"></span>
                                    </button>
                                </div>
                            </td>
                            <td>
                                <div class="d-flex align-items-center">
                                    <div class="me-3">
                                        <input type="number" id="quantity${product.id}" name="quantity${product.id}" min="1" value="1" class="form-control form-control-sm" style="width: 60px;">
                                    </div>
                                    <a class="symbol symbol-50px me-3">
                                        <span class="symbol-label" style="background-image:url(${imageUrl});"></span>
                                    </a>
                                    <div>
                                        <a class="text-gray-800 text-hover-primary fs-5 fw-bolder">${product.name}</a>
                                        <div class="fw-bold fs-7">Prix: DH <span>${product.price}</span></div>
                                        <div class="text-muted fs-7">Ref: ${product.ref}</div>
                                    </div>
                                </div>
                            </td>
                            <td class="text-end pe-5">
                                ${product.qte > 0 && product.qte < 10 ? `<span class="badge badge-light-danger" style="color: orange;">Presque épuisé ${product.qte}</span>` : (product.qte == 0 ? `<span class="badge badge-light-danger" style="color: red;">Épuisé ${product.qte}</span>` : `<span class="badge badge-light-danger" style="color: green;">Disponible ${product.qte}</span>`)}
                            </td>
                        </tr>
                    </tbody>
                </form>`;
        })
        .catch(error => console.error('Error fetching data:', error));
}



fetchDataFromAPI();

autocomplete(document.getElementById("searchNOW"), products);

