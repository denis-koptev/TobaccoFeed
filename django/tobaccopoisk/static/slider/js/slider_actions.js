
var slideIndex = 0;

autoSwitchSlides();

function plusSlides(n) {
  switchSlides(slideIndex + n);
}

function currentSlide(n) {
  switchSlides(n);
}

function switchSlides(numSlide) {
  var i;
  var slides = document.getElementsByClassName("mySlides");
  var dots = document.getElementsByClassName("dot");
  var text_recs = document.getElementsByClassName("news_rec");

  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none"; 
  }

  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }

  for (i = 0; i < text_recs.length; ++i) {
    text_recs[i].className = text_recs[i].className.replace(" rec_active", "");
  }

  slideIndex = numSlide;

  if (slideIndex > slides.length) {
    slideIndex = 1
  } else if (slideIndex < 1) {
    slideIndex = slides.length;
  }

  slides[slideIndex-1].style.display = "block"; 
  dots[slideIndex-1].className += " active";
  text_recs[slideIndex-1].className += " rec_active";
}

function autoSwitchSlides() {
  switchSlides(slideIndex + 1)
  setTimeout(autoSwitchSlides, 4000);
}
