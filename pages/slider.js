// JavaScript para controlar el desplazamiento del slider
const newsSlider = document.querySelector('.news-slider');
const slides = document.querySelectorAll('.slide');

let currentIndex = 0;
const slideWidth = slides[0].offsetWidth;

function showSlide(index) {
    if (index < 0) {
        index = slides.length - 1;
    } else if (index >= slides.length) {
        index = 0;
    }

    const offset = -index * slideWidth;
    newsSlider.style.transform = `translateX(${offset}px)`;
    currentIndex = index;
}

// Controladores para desplazarse a la siguiente y anterior noticia
document.querySelector('.next-button').addEventListener('click', () => {
    showSlide(currentIndex + 1);
});

document.querySelector('.prev-button').addEventListener('click', () => {
    showSlide(currentIndex - 1);
});

// Inicialmente, muestra el primer slide
showSlide(currentIndex);
