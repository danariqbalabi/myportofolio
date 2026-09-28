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

function moveCarousel(step) {
    activeIndex =
        (activeIndex + step + cards.length) % cards.length;

    updateCarousel();
}

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

previousButton?.addEventListener("click", () => moveCarousel(-1));

nextButton?.addEventListener("click", () => moveCarousel(1));

cards.forEach((card, index) => {
    card.addEventListener("click", () => {
        activeIndex = index;
        updateCarousel();
    });
});

const stage = document.querySelector(".experience-stage");
let touchStartX = null;

stage?.addEventListener("touchstart", (event) => {
    touchStartX = event.changedTouches[0].clientX;
}, { passive: true });

stage?.addEventListener("touchend", (event) => {
    if (touchStartX === null) return;

    const distance = event.changedTouches[0].clientX - touchStartX;

    if (Math.abs(distance) >= 50) {
        moveCarousel(distance < 0 ? 1 : -1);
    }

    touchStartX = null;
}, { passive: true });

if (cards.length > 0) {
    updateCarousel();
}
