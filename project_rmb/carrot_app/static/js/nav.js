document.addEventListener("DOMContentLoaded", () => {
    if (window.location.pathname.includes("trade") || window.location.pathname.includes("write") || window.location.pathname.includes("edit")) {
        document.getElementById("trade-button").classList.toggle("orange-text");
    } else if (window.location.pathname == "/location/") {
        document.getElementById("location-button").classList.toggle("orange-text");
    }
});

// var buttonClear = document.querySelector(".button-clear");
// buttonClear.addEventListener("click", function () {
//     buttonClear.parentNode.querySelector("input").value = "";
// });

// 버튼을 누를 때 마다 창의 활성화, 비활성화를 반복
const searchButton = document.querySelector(".search-button");
const hamburgerButton = document.querySelector(".hamburger-button");
const searchContainer = document.querySelector(".search-container");
const hamburgerContainer = document.querySelector(".hamburger-container");
const logo = document.querySelector(".logo");
const searchExtend = document.querySelector(".search-extend");

let isSearchContainerVisible = false;
let isHamburgerContainerVisible = false;
let isSearchExtendVisible = false;

searchButton.addEventListener("click", function () {
    if (!isSearchContainerVisible) {
        searchContainer.style.display = "flex";
        isSearchContainerVisible = true;
        logo.style.display = "none";
        searchExtend.style.display = "flex";

        if (isHamburgerContainerVisible) {
            hamburgerContainer.style.display = "none";
            isHamburgerContainerVisible = false;
        }
    } else {
        searchContainer.style.display = "none";
        isSearchContainerVisible = false;
        logo.style.display = "flex";
        searchExtend.style.display = "none";
    }
});

hamburgerButton.addEventListener("click", function () {
    if (!isHamburgerContainerVisible) {
        hamburgerContainer.style.display = "flex";
        isHamburgerContainerVisible = true;

        if (isSearchContainerVisible) {
            searchContainer.style.display = "none";
            isSearchContainerVisible = false;
            logo.style.display = "flex";
            searchExtend.style.display = "none";
        }
    } else {
        hamburgerContainer.style.display = "none";
        isHamburgerContainerVisible = false;
    }
});
