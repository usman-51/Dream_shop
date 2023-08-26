
/* ###################################################################################################
   ###########################################  STICKY BAR  ##########################################
   ################################################################################################### */
   
   (function() {
    window.onscroll = function() {myFunction()};
  
    var navbar = document.getElementById("navbar_fix");
    var dummyNav = document.getElementById("dummy_nav");
    var sticky = navbar.offsetTop;
  
    function myFunction() {
      if (window.pageYOffset >= sticky) {
        navbar.classList.add("sticky");
        dummyNav.style.display = "block";
      } else {
        navbar.classList.remove("sticky");
        dummyNav.style.display = "none";
      }
    }
  })();
   
   
/* ###################################################################################################
   ##########################################  CAROUSEL  ##########################################
   ################################################################################################### */

   (function() {
    function nextSlide() {
      let lists = document.querySelectorAll('.item');
      document.getElementById('slide').appendChild(lists[0]);
    }
  
    function prevSlide() {
      let lists = document.querySelectorAll('.item');
      document.getElementById('slide').prepend(lists[lists.length - 1]);
    }
  
    document.getElementById('next-01').addEventListener('click', nextSlide);
    document.getElementById('prev-01').addEventListener('click', prevSlide);
  
    setInterval(nextSlide, 5000);
  })();
