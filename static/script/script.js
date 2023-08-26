
/* ###################################################################################################
   ###########################################  STICKY BAR  ##########################################
   ################################################################################################### */

   window.onscroll = function() {myFunction()};

   var navbar = document.getElementById("navbar_fix");
   var sticky = navbar.offsetTop;
   
   // Créez un élément de remplacement pour la barre de navigation
   var navbarPlaceholder = document.createElement('div');
   navbarPlaceholder.style.display = 'none'; // Cachez l'élément de remplacement par défaut
   navbar.parentNode.insertBefore(navbarPlaceholder, navbar); // Insérez l'élément de remplacement avant la navbar
   
   function myFunction() {
     if (window.pageYOffset >= sticky) {
       navbar.classList.add("sticky");
       navbarPlaceholder.style.height = navbar.offsetHeight + 'px'; // Ajustez la hauteur quand la navbar est fixe
       navbarPlaceholder.style.display = 'block'; // Montrez l'élément de remplacement quand la navbar est fixe
     } else {
       navbar.classList.remove("sticky");
       navbarPlaceholder.style.height = '0px'; // Réinitialisez la hauteur quand la navbar n'est pas fixe
       navbarPlaceholder.style.display = 'none'; // Cachez l'élément de remplacement quand la navbar n'est pas fixe
     }
   }
   
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

/* ###################################################################################################
   ###########################################  AUTO HOURS  ##########################################
   ################################################################################################### */

// le jour de la semaine actuel (0 pour dimanche, 1 pour lundi, etc.)
var dayOfWeek = new Date().getDay();
// Sélectionnez l'option correspondante dans le sélecteur "store-hours"
var storeHoursSelector = document.getElementById("store-hours");
storeHoursSelector.selectedIndex = dayOfWeek;
