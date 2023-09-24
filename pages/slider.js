document.addEventListener("DOMContentLoaded", function () {
    const slider = document.querySelector(".news-slider");
    const prevButton = document.querySelector(".prev-button");
    const nextButton = document.querySelector(".next-button");
    const slidesContainer = document.querySelector(".slides-container");

    let currentIndex = 0;

    nextButton.addEventListener("click", () => {
        currentIndex++;
        if (currentIndex >= slidesContainer.children.length) {
            currentIndex = 0;
        }
        updateSlider();
    });

    prevButton.addEventListener("click", () => {
        currentIndex--;
        if (currentIndex < 0) {
            currentIndex = slidesContainer.children.length - 1;
        }
        updateSlider();
    });

    function updateSlider() {
        const offset = -currentIndex * 100;
        slidesContainer.style.transform = `translateX(${offset}%)`;
    }
});
