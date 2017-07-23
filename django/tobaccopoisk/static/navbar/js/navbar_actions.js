
function userClicked() {
    document.getElementById("myDropdown").classList.toggle("show");
}

function searchClicked() {
    search_bar = document.getElementById("search_bar");
    if (!search_bar.classList.contains('search_bar_focus')) {
        search_bar.classList.toggle("search_bar_focus");
    }
}
