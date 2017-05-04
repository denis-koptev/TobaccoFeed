window.onclick = function(event) {

  /* 
  modal1,2,3 - variables, created in main_page 
  <script> insertion. It's fucking bad codestyle...
  */

  var modal1 = document.getElementById('modal1');
  var modal2 = document.getElementById('modal2');
  var modal3 = document.getElementById('modal3');

  if (event.target == modal1) {
    /*modal1.style.display = "none";*/
    if (modal1.classList.contains("in")) {
      modal1.classList.remove("in");
    }
    modal1.classList.add('out');
  } 
  else if (event.target == modal2) {
    /*modal2.style.display = "none";*/
    if (modal2.classList.contains("in")) {
      modal2.classList.remove("in");
    }
    modal2.classList.add('out');
  } 
  else if (event.target == modal3) {
    /*modal3.style.display = "none";*/
    if (modal3.classList.contains("in")) {
      modal3.classList.remove("in");
    }
    modal3.classList.add('out');
  } 
  
  if (!event.target.matches('.search_bar')) {
    search_bar = document.getElementById("search_bar");
    search_bar.classList.remove('search_bar_focus');
  } 
  
  if (!event.target.matches('.dropbtn') 
    && !event.target.matches('.user_icon')
    && !event.target.matches('.user_text')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}