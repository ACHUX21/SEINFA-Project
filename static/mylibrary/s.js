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
    var table = document.getElementById("kt_ecommerce_products_table");

    fetch(`/api/search?q=${AR_Ref}`)
        .then(response => response.json())
        .then(data => {
            const product = data[0];

        table.innerHTML = `
            <table class="table align-middle table-row-dashed fs-6 gy-5" id="kt_ecommerce_products_table">
											<!--begin::Table head-->
											<thead>
												<!--begin::Table row-->
												<tr class="text-start text-gray-400 fw-bolder fs-7 text-uppercase gs-0">
													<th class="w-10px pe-2">
														<div class="form-check form-check-sm form-check-custom form-check-solid me-3">
															<input class="form-check-input" type="checkbox" data-kt-check="true" data-kt-check-target="#kt_ecommerce_products_table .form-check-input" value="1" />
														</div>
													</th>
													<th class="min-w-200px">Article</th>
													<th class="text-end min-w-100px">Réference</th>
													<th class="text-end min-w-70px">Quantité</th>
													<th class="text-end min-w-100px">Prix de vente</th>
													<th class="text-end min-w-100px">Prix d'Achat</th>
													<th class="text-end min-w-100px">Statut</th>
													<th class="text-end min-w-70px">Actions</th>
												</tr>
												<!--end::Table row-->
											</thead>
											<!--end::Table head-->
											<!--begin::Table body-->
											<tbody class="fw-bold text-gray-600">
												<!--begin::Table row-->
												<tr>
													<!--begin::Checkbox-->
													<td>
														<div class="form-check form-check-sm form-check-custom form-check-solid">
															<input class="form-check-input" type="checkbox" value="1" />
														</div>
													</td>
													<!--end::Checkbox-->
													<!--begin::Category=-->
													<td>
														<div class="d-flex align-items-center">
															<!--begin::Thumbnail-->
															<a href="/product_details/${product.ref.replace('/', '-')}" class="symbol symbol-50px">
																<span class="symbol-label" style="background-image:url(${product.img})"></span>
															</a>
															<!--end::Thumbnail-->
															<div class="ms-5">
																<!--begin::Title-->
																<a href="/product_details/${product.ref.replace('/', '-')}" class="text-gray-800 text-hover-primary fs-5 fw-bolder" data-kt-ecommerce-product-filter="product_name">${product.name}</a>
																<!--end::Title-->
															</div>
														</div>
													</td>
													<!--end::Category=-->
													<!--begin::SKU=-->
													<td class="text-end pe-0">
														<span class="fw-bolder">${product.ref}</span>
													</td>
													<!--end::SKU=-->
													<!--begin::Qty=-->
													<td class="text-end pe-0" data-order="25">
														<span class="fw-bolder ms-3">${product.qte}</span>
													</td>
													<!--end::Qty=-->
													<!--begin::Price=-->
													<td class="text-end pe-0">
														<span class="fw-bolder text-dark">${product.price}</span>
													</td>
													<!--end::Price=-->
													<!--begin::Rating-->
													<td class="text-end pe-0">
														<span class="fw-bolder text-dark">${product.prix_achat}</span>
													</td>
													<!--end::Rating-->
													<!--begin::Status=-->
													<td class="text-end pe-0" data-order="Published">
														<!--begin::Badges-->
														<div class="badge badge-light-success">Statut</div>
														<!--end::Badges-->
													</td>
													<!--end::Status=-->
													<!--begin::Action=-->
													<td class="text-end">
														<!--begin::Update-->
														<a href="/product_details/${product.ref}" class="btn btn-icon btn-active-light-primary w-30px h-30px" data-kt-permissions-table-filter="delete_row">
															<!--begin::Svg Icon | path: icons/duotune/general/gen027.svg-->
															<span class="svg-icon svg-icon-3">
																<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
																	<path d="M17.5 11H6.5C4 11 2 9 2 6.5C2 4 4 2 6.5 2H17.5C20 2 22 4 22 6.5C22 9 20 11 17.5 11ZM15 6.5C15 7.9 16.1 9 17.5 9C18.9 9 20 7.9 20 6.5C20 5.1 18.9 4 17.5 4C16.1 4 15 5.1 15 6.5Z" fill="currentColor" />
																	<path opacity="0.3" d="M17.5 22H6.5C4 22 2 20 2 17.5C2 15 4 13 6.5 13H17.5C20 13 22 15 22 17.5C22 20 20 22 17.5 22ZM4 17.5C4 18.9 5.1 20 6.5 20C7.9 20 9 18.9 9 17.5C9 16.1 7.9 15 6.5 15C5.1 15 4 16.1 4 17.5Z" fill="currentColor" />
																</svg>
															</span>
															<!--end::Svg Icon-->
														</a>
														<!--end::Delete-->
													</td>
													<!--end::Action=-->
												</tr>
												<!--end::Table row-->
												<!--end::Table row-->
											</tbody>
											<!--end::Table body-->
										</table>`;
        })
        .catch(error => console.error('Error fetching data:', error));
}



fetchDataFromAPI();

autocomplete(document.getElementById("searchNOW"), products);

