$(document).ready(function () {

    // ------------------------
    // Utility: Collect Filters + Sort
    // ------------------------
    function getFilterSortData() {
        return {
            model: $("input[name='model']:checked").val(),
            year: $("input[name='year']:checked").val(),
            location: $("input[name='location']:checked").val(),
            price: $("#priceRange").val(),
            sort: $("#current-sort").val()
        };
    }

    // ------------------------
    // Spinner + Fetch Products (AJAX)
    // ------------------------
    function fetchProducts() {
        const data = getFilterSortData();

        $("#product-list").hide();
        $("#product-loading").show();

        $.ajax({
            url: "/buy-used-rv/ajax/filter-sort-products/",
            type: "GET",
            data: data,
            cache: false,
            success: function (response) {
                setTimeout(function () {
                    $("#product-loading").hide();
                    $("#product-grid").html(response);
                    $("#product-list").fadeIn(600);

                    //restting icon visibilty
                    $("#product-list .material-symbols-outlined").css({'width': 'auto', 'opacity': '1'});
                    $(document).trigger("productsUpdated"); // rebind wishlist icons
                }, 1500);
            },
            error: function (xhr, status, error) {
                $("#product-loading").hide();
                $("#product-list").show();

                //restting icon visibilty
                $("#product-list .material-symbols-outlined").css({'width': 'auto', 'opacity': '1'});
                console.error("Error fetching products:", error);
            }
        });
    }

    // ------------------------
    // Sorting Dropdown
    // ------------------------
    $(".sort-dropdown .drop-input").on("click", function (e) {
        e.stopPropagation();
        const root = $(this).closest(".sort-dropdown");
        root.find(".dropdown-list").toggleClass("open");
        root.find(".drop-icon").toggleClass("rotated");
    });

    $(document).on("click", function () {
        $(".dropdown-list").removeClass("open");
        $(".drop-icon").removeClass("rotated");
    });

    $(".dropdown-item").on("click", function (e) {
        e.stopPropagation();
        const sortKey = $(this).data("value");
        const label = $(this).text();
        $("#sort-value").text(label);
        $("#current-sort").val(sortKey);
        $(this).closest(".sort-dropdown").find(".dropdown-list").removeClass("open");
        $(this).closest(".sort-dropdown").find(".drop-icon").removeClass("rotated");
        $("#reset-sort").removeClass("d-none");
        fetchProducts();
    });

    $("#reset-sort").on("click", function (e) {
        e.stopPropagation();
        $("#current-sort").val("all");
        $("#sort-value").text("Sort:");
        $(this).addClass("d-none");
        fetchProducts();
    });

    // ------------------------
    // Filters (Radio Buttons & Price)
    // ------------------------
    $(".filter-input[type='radio']").on("change", function () {
        const name = $(this).attr("name");
        $(`input[name='${name}']`).closest("label").removeClass("selected");
        $(this).closest("label").addClass("selected");
        fetchProducts();
    });

    $("#priceRange").on("input", function () {
        const value = parseInt($(this).val()).toLocaleString();
        $("#priceValue").text(value);
        fetchProducts();
    });

    // Reset Filters Button
    $("#resetFilters").on("click", function () {
        $(".filter-input[type='radio']").each(function () {
            if ($(this).val().includes("all_")) {
                $(this).prop("checked", true).closest("label").addClass("selected");
            } else {
                $(this).prop("checked", false).closest("label").removeClass("selected");
            }
        });
        const maxPrice = $("#priceRange").attr("max");
        $("#priceRange").val(maxPrice);
        $("#priceValue").text(maxPrice);
        $("#current-sort").val("all");
        $("#sort-value").text("Sort:");
        $("#reset-sort").addClass("d-none");
        fetchProducts();
    });

    // ------------------------
    // Mobile Filter Slide In/Out
    // ------------------------
    const filter = $("#filter");
    $("#openFilter").click(function (e) {
        e.preventDefault();
        filter.css("left", "0");
    });
    $("#closeFilter").click(function (e) {
        e.preventDefault();
        filter.css("left", "-101%");
    });

    // ------------------------
    // Initial Page Load Spinner
    // ------------------------
    $("#product-loading").show();
    $("#product-list").hide();
    setTimeout(function () {
        $("#product-loading").fadeOut(300, function () {
            $("#product-list").fadeIn(800);
        });
    }, 3000);

});
