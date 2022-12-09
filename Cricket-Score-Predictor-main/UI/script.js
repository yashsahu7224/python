var myIndex = 0;
var second_myIndex = 0;
carousel();
second_carousel();

function carousel() {
  var i;
  var x = document.getElementsByClassName("mySlides");
  for (i = 0; i < x.length; i++) {
    x[i].style.display = "none";  
  }
  myIndex++;
  if (myIndex > x.length) {myIndex = 1}    
  x[myIndex-1].style.display = "block";  
  setTimeout(carousel, 2500);    
}

function second_carousel() {
  var i;
  var x = document.getElementsByClassName("Slides");
  for (i = 0; i < x.length; i++) {
    x[i].style.display = "none";  
  }
  second_myIndex++;
  if (second_myIndex > x.length) {second_myIndex = 1}    
  x[second_myIndex-1].style.display = "block";  
  setTimeout(second_carousel, 2500);    
}