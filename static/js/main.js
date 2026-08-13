/* ==========================================================================
   Rate My Teacher — Main JavaScript
   ========================================================================== */

document.addEventListener("DOMContentLoaded", function () {

    /* ----------------------------------------------------------------------
       Confirm that JavaScript is working
       ---------------------------------------------------------------------- */

    document.body.classList.add("js-loaded");


    /* ----------------------------------------------------------------------
       Search form
       Prevent empty searches
       ---------------------------------------------------------------------- */

    const searchForm = document.querySelector(".search-form");

    if (searchForm) {
        searchForm.addEventListener("submit", function (event) {

            const input = searchForm.querySelector("input[name='q']");

            if (!input) {
                return;
            }

            const value = input.value.trim();

            if (value === "") {
                event.preventDefault();
                input.focus();
            }
        });
    }


    /* ----------------------------------------------------------------------
       Rating buttons
       Gives the selected rating a visual state
       ---------------------------------------------------------------------- */

    const ratingOptions = document.querySelectorAll(".rating-option");

    ratingOptions.forEach(function (option) {

        const input = option.querySelector("input");
        const span = option.querySelector("span");

        if (!input || !span) {
            return;
        }

        input.addEventListener("change", function () {

            const group = option.closest(".rating-scale");

            if (!group) {
                return;
            }

            group.querySelectorAll(".rating-option span").forEach(function (item) {
                item.classList.remove("selected");
            });

            if (input.checked) {
                span.classList.add("selected");
            }
        });
    });


    /* ----------------------------------------------------------------------
       Sort dropdown
       Automatically submit when changed
       ---------------------------------------------------------------------- */

    const sortForm = document.querySelector(".sort-form");
    const sortSelect = document.querySelector(".sort-form select");

    if (sortForm && sortSelect) {
        sortSelect.addEventListener("change", function () {
            sortForm.submit();
        });
    }


    /* ----------------------------------------------------------------------
       Review form
       Prevent submitting while the form is being processed
       ---------------------------------------------------------------------- */

    const reviewForm = document.querySelector(".review-form");

    if (reviewForm) {

        reviewForm.addEventListener("submit", function () {

            const submitButton = reviewForm.querySelector(
                "button[type='submit']"
            );

            if (submitButton) {
                submitButton.disabled = true;
                submitButton.textContent = "Submitting...";
            }

        });

    }


    /* ----------------------------------------------------------------------
       Add teacher form
       Prevent accidental empty submissions
       ---------------------------------------------------------------------- */

    const teacherForm = document.querySelector(".teacher-form");

    if (teacherForm) {

        teacherForm.addEventListener("submit", function (event) {

            const nameInput = teacherForm.querySelector(
                "input[name='name']"
            );

            const subjectInput = teacherForm.querySelector(
                "input[name='subject']"
            );

            if (!nameInput || !subjectInput) {
                return;
            }

            if (
                nameInput.value.trim() === "" ||
                subjectInput.value.trim() === ""
            ) {
                event.preventDefault();

                if (nameInput.value.trim() === "") {
                    nameInput.focus();
                } else {
                    subjectInput.focus();
                }
            }

        });

    }


    /* ----------------------------------------------------------------------
       Flash messages
       Automatically fade them after a few seconds
       ---------------------------------------------------------------------- */

    const flashMessages = document.querySelectorAll(".flash");

    flashMessages.forEach(function (message) {

        setTimeout(function () {

            message.style.transition = "opacity 0.4s ease";
            message.style.opacity = "0";

            setTimeout(function () {
                message.remove();
            }, 400);

        }, 4500);

    });


    /* ----------------------------------------------------------------------
       Teacher cards
       Keyboard accessibility
       ---------------------------------------------------------------------- */

    const teacherCards = document.querySelectorAll(".teacher-card");

    teacherCards.forEach(function (card) {

        card.addEventListener("keydown", function (event) {

            if (event.key === "Enter" || event.key === " ") {

                event.preventDefault();

                card.click();

            }

        });

    });


    /* ----------------------------------------------------------------------
       Small confirmation before leaving a review with unsaved text
       ---------------------------------------------------------------------- */

    const commentBox = document.querySelector(
        ".paper-form textarea[name='comment']"
    );

    let reviewChanged = false;

    if (commentBox) {

        commentBox.addEventListener("input", function () {
            reviewChanged = commentBox.value.trim() !== "";
        });

    }


    /* ----------------------------------------------------------------------
       Console message
       ---------------------------------------------------------------------- */

    console.log("Rate My Teacher loaded successfully.");

});