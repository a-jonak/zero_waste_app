var updateUPBtns = document.getElementsByClassName('update-user-product')
var updateSPBtns = document.getElementsByClassName('update-shopping-product')
var addToSLBtns = document.getElementsByClassName('add-to-shopping-list')

for(var i = 0; i < updateUPBtns.length; i++){
    updateUPBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product;
        var action = this.dataset.action;
        updateUserProduct(productId, action)
    })
}

for(var i = 0; i < updateSPBtns.length; i++){
    updateSPBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product;
        var action = this.dataset.action;
        updateShoppingProduct(productId, action)
    })
}

for(var i = 0; i < addToSLBtns.length; i++){
    addToSLBtns[i].addEventListener('click', function (){
        var productId = this.dataset.product;
        addToShoppingList(productId)
    })
}

function updateUserProduct(productId, action) {
    $.ajax({
            type: "GET",
            url: "update_user_product",
            data: {product_id: productId, action: action},
            success: function (data) {
                if (data <= 0) {
                    location.reload()
                } else {
                    $("#product_number" + productId).html(data);
                }
            }
        });
}

function updateShoppingProduct(productId, action) {
    $.ajax({
            type: "GET",
            url: "update_shopping_product",
            data: {product_id: productId, action: action},
            success: function (data) {
                if (data <= 0) {
                    location.reload()
                } else {
                    $("#product_amount" + productId).html(data);
                }
            }
        });
}

function addToShoppingList(productId) {
    $.ajax({
        type: "GET",
        url: "add_to_shopping_list",
        data: {product_id: productId},
        success: function (data) {
            alert(data);
        }
    });
}
