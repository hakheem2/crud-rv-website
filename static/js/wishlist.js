
$(document).on("click", ".wishlist-btn", function(e) {
    e.preventDefault();
    let button = $(this);
    let productId = button.data("product-id");

    $.ajax({
        url: "/buy-used-rv/wishlist/toggle/",
        type: "POST",
        data: { product_id: productId },
        success: function(response) {
            if (response.success) {
                if (response.in_wishlist) {
                    button.addClass("active");
                    animateWishlist(button);
                } else {
                    button.removeClass("active");
                }
            }
        }
    });
});

