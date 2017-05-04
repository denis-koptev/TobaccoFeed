
var slideIndex = 0;
switchSlides();

function plusSlides(n) {
switchSlides((n > 0), false);
}

function currentSlide(n) {
switchSlides((n > 0), false);
}

function switchSlides(switchNext = true, isAuto = true) {
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

  if (switchNext) {
    slideIndex++;
  } else {
    slideIndex--;
  }

  if (slideIndex > slides.length) {
    slideIndex = 1
  } else if (slideIndex < 1) {
    slideIndex = slides.length;
  }

  slides[slideIndex-1].style.display = "block"; 
  dots[slideIndex-1].className += " active";
  text_recs[slideIndex-1].className += " rec_active";

  if (isAuto) {
    setTimeout(switchSlides, 4000);
  }
}
