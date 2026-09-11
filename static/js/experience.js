const cards = Array.from(
    document.querySelectorAll(".experience-card")
);

const previousButton = document.querySelector(
    ".experience-arrow--previous"
);

const nextButton = document.querySelector(
    ".experience-arrow--next"
);

let activeIndex = 0;

function updateCarousel() {
    cards.forEach((card, index) => {
        card.classList.remove(
            "is-active",
            "is-previous",
            "is-next"
        );

        if (index === activeIndex) {
            card.classList.add("is-active");
        }

        if (
            index ===
            (activeIndex - 1 + cards.length) % cards.length
        ) {
            card.classList.add("is-previous");
        }

        if (
            index ===
            (activeIndex + 1) % cards.length
        ) {
            card.classList.add("is-next");
        }
    });
}

previousButton.addEventListener("click", () => {
    activeIndex =
        (activeIndex - 1 + cards.length) % cards.length;

    updateCarousel();
});

nextButton.addEventListener("click", () => {
    activeIndex =
        (activeIndex + 1) % cards.length;

    updateCarousel();
});

cards.forEach((card, index) => {
    card.addEventListener("click", () => {
        activeIndex = index;
        updateCarousel();
    });
});

updateCarousel();