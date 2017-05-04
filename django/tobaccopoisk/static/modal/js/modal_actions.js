// Get the modal
var modal1 = document.getElementById('modal1');
var modal2 = document.getElementById('modal2');
var modal3 = document.getElementById('modal3');

// Get the button that opens the modal
var btn1 = document.getElementById("modal_button1");
var btn2 = document.getElementById("modal_button2");
var btn3 = document.getElementById("modal_button3");

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

btn2.onclick = function() {
	if (modal2.classList.contains("out")) {
    	modal2.classList.remove("out");
    }
    modal2.classList.add("in");
    /*modal2.style.display = "block";   */
}

btn3.onclick = function() {
	if (modal3.classList.contains("out")) {
    	modal3.classList.remove("out");
    }
    modal3.classList.add("in");
    /*modal3.style.display = "block";   */
}

// When the user clicks on <span> (x), close the modal
span[0].onclick = function() {
	if (modal1.classList.contains("in")) {
		modal1.classList.remove("in");
	}
	modal1.classList.add('out');
	/*modal1.style.display = "none";*/
}

span[1].onclick = function() {
	if (modal2.classList.contains("in")) {
		modal2.classList.remove("in");
	}
	modal2.classList.add('out');
	/*modal2.style.display = "none";*/
}

span[2].onclick = function() {
	if (modal3.classList.contains("in")) {
		modal3.classList.remove("in");
	}
	modal3.classList.add('out');
	/*modal3.style.display = "none";*/
}


// Outside clicks are processed in animations.js (navbar static)