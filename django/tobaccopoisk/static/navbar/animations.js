
function userClicked() {
    document.getElementById("myDropdown").classList.toggle("show");
}

function searchClicked() {
  search_bar = document.getElementById("search_bar");
  if (!search_bar.classList.contains('search_bar_focus')) {
    search_bar.classList.toggle("search_bar_focus");
  }
}

window.onclick = function(event) {
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
