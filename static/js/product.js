//SWIPPER EVENT HANDLER CODE
// Init after DOM loaded
$(document).ready(()=>{
   const swiper = new Swiper('.myProductCarousel', {
         loop: false,
         spaceBetween: 16,
         // Helpful when content/layout may change
         observer: true,
         observeParents: true,
         watchOverflow: true,
         pagination: { el: '.swiper-pagination', clickable: true },
         navigation: { nextEl: '.swiper-button-next', prevEl: '.swiper-button-prev' },
         breakpoints: {
            0:   { slidesPerView: 2 },   // Mobile
            768: { slidesPerView: 3 },   // Tablet
            992: { slidesPerView: 4 }    // Desktop / large
         },
         on: {
            init() { console.log('Swiper initialized — slides:', this.slides.length); }
         }
   });

   // Expose for debugging in console
   window.__mySwiper = swiper;



   //CHANGNG PRODUCT ON CLICK
   $('.gallery-img').click( function (){
      let newUrl = $(this).attr('src');
      $('.gallery-img').removeAttr('id');

      // Add ID to the clicked image
      $(this).attr('id', 'active');

      //image src change
      $('.main-image .img')
         .fadeOut(200, function() {
            $(this).attr('src', newUrl).fadeIn(200);
         });
   });


   //switching between day plan and night plan of rv
   $('#dayMode').click(function () {
      // Set active class
      $('#nightMode').removeClass('active');
      $(this).addClass('active');

      // Fade out night plan, then fade in day plan
      $('#nightPlan').fadeOut(300, function() {
         $('#dayPlan').fadeIn(300);
      });
   })

   $('#nightMode').click(function () {
      //setting active class
      $('#dayMode').removeClass('active');
      $(this).addClass('active');

      // Fade out night plan, then fade in day plan
      $('#dayPlan').fadeOut(300, function() {
         $('#nightPlan').fadeIn(300);
      });
   })


   //function to calculate sales percent
   function calculate() {
      // Get text content and remove commas if present
      let val1 = $("#sale_price").text().replace(/,/g, '');
      let val2 = $("#price").text().replace(/,/g, '');

      let sale_price = parseFloat(val1);
      let actual_price = parseFloat(val2);

      let discount = (actual_price - sale_price) / actual_price;
      let percentage = Math.round(discount * 100);

      // Display result
      $(".discount-percent").text('- ' + percentage + '%');
   };

   // Call function on page load
   calculate();


});


$(document).ready(function() {
   //code to add #active to image to styling active galerry image image
   // Add 'active' ID to the first one
   $(".gallery-img").first().attr("id", "active");
    
});


