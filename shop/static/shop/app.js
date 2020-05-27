var image = document.querySelectorAll('.image');

image.forEach(elem =>{
    elem.addEventListener("mouseover", swapImage2);
    elem.addEventListener("mouseleave", swapImage);
 });

function swapImage(event){
    var image = event.target;
    var imagehover = event.target.src;
    var jpg = imagehover.substr(imagehover.length-4);
    var beginning = imagehover.slice(0, imagehover.length - 5);
    image.src = beginning + '1' + jpg;
} 
function swapImage2(event){
    var image = event.target;
    var imagehover = event.target.src;
    var jpg = imagehover.substr(imagehover.length-4);
    var beginning = imagehover.slice(0, imagehover.length - 5);
    image.src = beginning + '2' + jpg;
    image.onerror=function(){
        image.src = beginning + '1' + jpg;
    }
} 

document.getElementById('cart').addEventListener('mouseover', function(){
    document.querySelector('.order').classList.add('active');
})

document.querySelector('.order').addEventListener('mouseover', function(){
    document.querySelector('.order').classList.add('active');
})

document.querySelector('.order').addEventListener('mouseleave', function(){
    document.querySelector('.order').classList.remove('active');
})

document.getElementById('cart').addEventListener('mouseleave', function(){
    document.querySelector('.order').classList.remove('active');
})
