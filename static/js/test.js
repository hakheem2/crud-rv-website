
// ====================================================================
//             SORTING LIST SECTION FUNTIONS AND AJAX HANDLING
// ====================================================================
$(document).ready(function () {

    // Toggle sort dropdown open/close via class only
    $(".sort-dropdown .drop-input").on("click", function (e) {
        e.stopPropagation();
        const root = $(this).closest(".sort-dropdown");
        root.find(".dropdown-list").toggleClass("open");
        root.find(".drop-icon").toggleClass("rotated");
    });
    // Close dropdown when clicking outside
    $(document).on("click", function () {
        $(".dropdown-list").removeClass("open");
        $(".drop-icon").removeClass("rotated");
    });



    // Fetch products via AJAX with spinner prelude and fade-in
    function fetchSortedProducts(sortKey) {
        $("#product-list").hide();
        $("#product-loading").show();

        $.ajax({
        url: "/buy-used-rv/ajax/sort-products/",
        type: "GET",
        data: { sort: sortKey },
        cache: false,
        success: function (html) {
            setTimeout(function () {
                $("#product-loading").hide();
                $("#product-grid").html(html);
                $("#product-list").fadeIn(600);
                if (sortKey !== "all") {
                    $("#reset-sort").removeClass("d-none");
                } else {
                    $("#reset-sort").addClass("d-none");
                }
                $("#product-grid .material-symbols-outlined").css({'width': 'auto', 'opacity': '1'});
            }, 3000);
        },
        error: function () {
            $("#product-loading").hide();
            $("#product-list").fadeIn(200);
        }
        });
    }



    // Select a sort option
    $(".dropdown-item").on("click", function (e) {
        e.stopPropagation();
        const sortKey = $(this).data("value");
        const label = $(this).text();
        $("#sort-value").text(label);
        $("#current-sort").val(sortKey);
        $(this).closest(".sort-dropdown").find(".dropdown-list").removeClass("open");
        $(this).closest(".sort-dropdown").find(".drop-icon").removeClass("rotated");
        $("#reset-sort").removeClass("d-none");
        fetchSortedProducts(sortKey);
    });


    // Reset sorting
    $("#reset-sort").on("click", function (e) {
        e.stopPropagation();
        $("#current-sort").val("all");
        $("#sort-value").text("Sort:");
        $(this).addClass("d-none");
        fetchSortedProducts("all");
    });

    // Initial prelude spinner on page load
    $("#product-loading").show();
    $("#product-list").hide();
    setTimeout(function () {
        $("#product-loading").fadeOut(300, function () {
        $("#product-list").fadeIn(800);
        });
    }, 3000);
});








// ====================================================================
//              FILTER LIST SECTIOIN AND AJX CALLS HANDLING
// ====================================================================
$(document).ready(function () {

    //MAKING THE FILTER SLIDE IN AND OUT ON CLICK ON MOBILLE
    const filter = $('#filter');
    const openFilter = $('#openFilter').click(function (e) {
        e.preventDefault();
        $(this).fadeOut(100).fadeIn(100);
        filter.css('left', '0');
    })
    const closeFilter = $('#closeFilter').click(function (e) {
        e.preventDefault();
        $(this).fadeOut(100).fadeIn(100);
        filter.css('left', '-101%');
    })    


    // Utility: collect current filter values
    function getFilterData() {
        return {
        model: $("input[name='model']:checked").val(),
        year: $("input[name='year']:checked").val(),
        location: $("input[name='location']:checked").val(),
        price: $("#priceRange").val()
        };
    }

    // Apply .selected class on radio change
    $(".filter-input[type='radio']").on("change", function () {
        const name = $(this).attr("name");
        $(`input[name='${name}']`).closest("label").removeClass("selected");
        $(this).closest("label").addClass("selected");

        // Trigger AJAX fetch
        fetchFilteredProducts();
    });

    // Price range change
    $("#priceRange").on("input", function () {
        const value = parseInt($(this).val()).toLocaleString();
        $("#priceValue").text(value);
        fetchFilteredProducts();
    });

    // Reset filters button
    $("#resetFilters").on("click", function () {
        // Reset radios
        $(".filter-input[type='radio']").each(function () {
        if ($(this).val().includes("all_")) {
            $(this).prop("checked", true);
            $(this).closest("label").addClass("selected");
        } else {
            $(this).prop("checked", false);
            $(this).closest("label").removeClass("selected");
        }
        });

        // Reset price
        const maxPrice = $("#priceRange").attr("max");
        $("#priceRange").val(maxPrice);
        $("#priceValue").text(maxPrice);

        // Trigger AJAX fetch
        fetchFilteredProducts();
    });

    // Fetch products via AJAX
    function fetchFilteredProducts() {
        const filters = getFilterData();

        $("#product-list").hide();
        $("#product-loading").show();

        $.ajax({
        url: "/buy-used-rv/ajax/filter-products/",
        type: "GET",
        data: filters,
        success: function (response) {
            setTimeout(function () {
            $("#product-loading").hide();
            $("#product-grid").html(response);
            $("#product-list").fadeIn(600);
            $(document).trigger("productsUpdated"); // keep wishlist etc working
            }, 1000); 
        },
        error: function (xhr, status, error) {
            $("#product-loading").hide();
            $("#product-list").show();
            console.error("Error fetching filtered products:", error);
        }
        });
    }

});
