// Get the modal
var modal1 = document.getElementById('modal_related');

// Get the button that opens the modal
var btn1 = document.getElementById("modal_button_related");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close");

// When the user clicks the button, open the modal 
btn1.onclick = function() {
	if (modal1.classList.contains("out")) {
    	modal1.classList.remove("out");
    }
    modal1.classList.add("in");
    /*modal1.style.display = "block";   */
}


// When the user clicks on <span> (x), close the modal
span[0].onclick = function() {
	if (modal1.classList.contains("in")) {
		modal1.classList.remove("in");
	}
	modal1.classList.add('out');
	/*modal1.style.display = "none";*/
}

// Outside clicks are processed in animations.js (navbar static)