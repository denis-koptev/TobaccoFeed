// Get the modal
var modal1 = document.getElementById('modal_related');
var modal2 = document.getElementById('modal_mixes');

// Get the button that opens the modal
var btn1 = document.getElementById("modal_button_related");
var btn2 = document.getElementById("modal_button_mixes");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close");

// When the user clicks the button, open the modal 
btn1.onclick = function() {
	if (modal1.classList.contains("out")) {
    	modal1.classList.remove("out");
    }
    modal1.classList.add("in");
}

btn2.onclick = function() {
	if (modal2.classList.contains("out")) {
    	modal2.classList.remove("out");
    }
    modal2.classList.add("in");
}


// When the user clicks on <span> (x), close the modal
span[0].onclick = function() {
	if (modal1.classList.contains("in")) {
		modal1.classList.remove("in");
	}
	modal1.classList.add('out');
}

span[1].onclick = function() {
	if (modal2.classList.contains("in")) {
		modal2.classList.remove("in");
	}
	modal2.classList.add('out');
}

// Outside clicks are processed in animations.js (navbar static)