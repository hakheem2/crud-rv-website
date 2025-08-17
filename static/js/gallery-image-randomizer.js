$(document).ready( () => {
   
   //OPENING AND CLOSING OF NAVBAR DROPDOWNS
    $('.drop_down_arrow').click(function() {
        $('#drop_menu').fadeToggle(200); // Smooth transition
    });


    // Array of images
    var images = [
        '/static/images/gallery-img-1.jpeg',
        '/static/images/gallery-img-2.jpeg',
        '/static/images/gallery-img-3.jpeg',
        '/static/images/gallery-img-4.jpeg',
        '/static/images/gallery-img-5.jpeg',
        '/static/images/gallery-img-6.jpeg',
        '/static/images/gallery-img-7.jpeg',
        '/static/images/gallery-img-8.jpeg',
        '/static/images/gallery-img-9.jpeg',
        '/static/images/gallery-img-10.jpeg',
        '/static/images/gallery-img-11.jpeg',
        '/static/images/gallery-img-12.jpeg'
    ];

    var $galleryImgs = $(".gallery-img");

    // Function to change an image for a specific index
    function changeImageForBox(index) {
        var currentSrc = $galleryImgs.eq(index).attr("src");
        var availableImages = images.filter(img => img !== currentSrc);
        var newImage = availableImages[Math.floor(Math.random() * availableImages.length)];

        // Change the image instantly
       	$galleryImgs.eq(index).fadeOut(100, function() {
				$(this).attr("src", newImage).fadeIn(300); 
			});

        // Schedule next change with random interval between 3–8 seconds
        var nextInterval = Math.floor(Math.random() * (10000 - 3000 + 1)) + 3000; // 3000–8000 ms
        setTimeout(function(){
            changeImageForBox(index);
        }, nextInterval);
    }

    // Start independent timers for each image box
    $galleryImgs.each(function(i){
        changeImageForBox(i);
    });

});