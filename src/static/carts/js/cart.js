function getCSRFToken() {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, 10) == ('csrftoken' + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(10));
                break;
            }
        }
    }
    return cookieValue;
}


// change qty
$(document).on("change",".qty-prod",function(e){
    e.preventDefault()
    let product_id = $(this).attr("prod_id")
    $(`#td-actions-${product_id}`).html(`<button type="submit" class=" text-green-700 update-cart" id="save-${product_id}" data-index="${product_id}">ذخیره</button>`)
    

})


// update cart
$(document).on("click", ".update-cart",function(e){
    e.preventDefault()
    let product_id = $(this).data("index")
    $.ajax({
        type: "POST",
        url: "/api/site/cart/update/",
        data: {
            product_id : product_id,
            qty_update: $(`#inp-id-${product_id}`).val(),
            csrfmiddlewaretoken: getCSRFToken(),
            action : "update-cart"
        },
        caches:false,
        success: function (json) {
            window.location.reload()
        },
        error: function(xhr,errmsg,err){
            
        }
    });
})



// remove cart
$(document).on("click", ".remove-cart",function(e){
    e.preventDefault()
    let product_id = $(this).data("index")
    $.ajax({
        type: "POST",
        url: "/api/site/cart/delete/",
        data: {
            product_id : product_id,
            csrfmiddlewaretoken: getCSRFToken(),
            action : "remove-cart"
        },
        caches:false,
        success: function (json) {
            window.location.reload()
        },
        error: function(xhr,errmsg,err){
            
        }
    });
})



