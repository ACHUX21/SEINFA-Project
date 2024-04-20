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
															<a href="../../demo1/dist/apps/ecommerce/catalog/edit-product.html" class="symbol symbol-50px">
																<span class="symbol-label" style="background-image:url(assets/media//stock/ecommerce/1.gif);"></span>
															</a>
															<!--end::Thumbnail-->
															<div class="ms-5">
																<!--begin::Title-->
																<a href="../../demo1/dist/apps/ecommerce/catalog/edit-product.html" class="text-gray-800 text-hover-primary fs-5 fw-bolder" data-kt-ecommerce-product-filter="product_name">${product.name}</a>
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
														<span class="fw-bolder text-dark">${product.price}</span>
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
														<a href="#" class="btn btn-sm btn-light btn-active-light-primary" data-kt-menu-trigger="click" data-kt-menu-placement="bottom-end">Actions
														<!--begin::Svg Icon | path: icons/duotune/arrows/arr072.svg-->
														<span class="svg-icon svg-icon-5 m-0">
															<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
																<path d="M11.4343 12.7344L7.25 8.55005C6.83579 8.13583 6.16421 8.13584 5.75 8.55005C5.33579 8.96426 5.33579 9.63583 5.75 10.05L11.2929 15.5929C11.6834 15.9835 12.3166 15.9835 12.7071 15.5929L18.25 10.05C18.6642 9.63584 18.6642 8.96426 18.25 8.55005C17.8358 8.13584 17.1642 8.13584 16.75 8.55005L12.5657 12.7344C12.2533 13.0468 11.7467 13.0468 11.4343 12.7344Z" fill="currentColor" />
															</svg>
														</span>
														<!--end::Svg Icon--></a>
														<!--begin::Menu-->
														<div class="menu menu-sub menu-sub-dropdown menu-column menu-rounded menu-gray-600 menu-state-bg-light-primary fw-bold fs-7 w-125px py-4" data-kt-menu="true">
															<!--begin::Menu item-->
															<div class="menu-item px-3">
																<a href="/api/edit/${product.ref}" class="menu-link px-3" data-kt-ecommerce-product-filter="delete_row">Edit</a>
															</div>
															<!--end::Menu item-->
															<!--begin::Menu item-->
															<div class="menu-item px-3">
																<a href="#" class="menu-link px-3" data-kt-ecommerce-product-filter="delete_row">Delete</a>
															</div>
															<!--end::Menu item-->
														</div>
														<!--end::Menu-->
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

