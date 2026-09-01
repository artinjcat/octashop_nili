$(document).on("click","#add-cart",function(e){
    e.preventDefault()
    $.ajax({
        type: "POST",
        url: "/api/site/cart/add/",
        data: {
            product_id : $(this).val(),
            "qty-to-cart": $("#qty-to-cart").val(),
            csrfmiddlewaretoken: $(this).attr("csrf"),
            action : "post"
        },
        caches:false,
        success: function (json) {
            
            $("#cart-quantity").html(json.qty)
            alert("محصول مورد نظر شما به سبد خرید اضافه شد.")
        },
        error: function(xhr,errmsg,err){
            
        }
    });
})