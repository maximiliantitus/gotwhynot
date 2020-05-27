document.addEventListener("DOMContentLoaded", function(event) {
    document.querySelectorAll('img').forEach(function(img){
       img.onerror = function(){this.style.display='none';};
    })
 });

 var images = document.querySelectorAll('.image');

 images.forEach(elem =>{
    elem.addEventListener("click", swapImage);
 });

 function swapImage(event){
    var imageClicked = event.target.src;
    var mainImage = document.getElementById('image');
    mainImage.src = imageClicked;
    var otherimages = document.querySelectorAll('.image');
    otherimages.forEach(elem =>{
        elem.classList.remove('active');
    })
    event.target.classList.add('active');
} 

document.getElementById('cart').addEventListener('mouseover', function(){
   document.querySelector('.order').classList.add('active');
})

document.getElementById('cart').addEventListener('mouseleave', function(){
   document.querySelector('.order').classList.remove('active');
})

document.querySelector('.order').addEventListener('mouseover', function(){
   document.querySelector('.order').classList.add('active');
})

document.querySelector('.order').addEventListener('mouseleave', function(){
   document.querySelector('.order').classList.remove('active');
})

var image = document.querySelector('.mainimage');

image.addEventListener('mousemove', function(e){
   var width = image.offsetWidth;
   var height = image.offsetHeight;
   var mouseX = e.offsetX;
   var mouseY = e.offsetY;

   var bgPosX = (mouseX / width*-70);
   var bgPosY = (mouseY / height*-70);

   image.style.left = String(bgPosX) + "%";
   image.style.top = String(bgPosY) + "%";
   console.log(bgPosX);
});

image.addEventListener('mouseleave', function(e){
   image.style.left = "0%";
   image.style.top = "0%";
});