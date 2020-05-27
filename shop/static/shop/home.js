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

function reportCoverSize() {
    var main = document.querySelector(".main");
    var targetPosition = main.getBoundingClientRect().bottom;
    var topmath = targetPosition/7.5;
    var space = document.querySelector(".space");
    space.style.top = String(topmath) + "%";
}
window.onresize = reportCoverSize;
window.onload = reportCoverSize;