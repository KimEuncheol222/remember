document.addEventListener("DOMContentLoaded", () => {
    if (window.location.pathname.includes("trade") || window.location.pathname.includes("write") || window.location.pathname.includes("edit")) {
        document.getElementById("trade-button").classList.toggle("orange-text");
    } else if (window.location.pathname == "/location/") {
        document.getElementById("location-button").classList.toggle("orange-text");
    } else if (window.location.pathname == "/wishlist/") { // 관심목록 페이지 URL 추가
        document.getElementById("wishlist-button").classList.toggle("orange-text");
    }
});

// 버튼을 누를 때 마다 창의 활성화, 비활성화를 반복
const searchButton = document.querySelector(".search-button");
const hamburgerButton = document.querySelector(".hamburger-button");
const searchContainer = document.querySelector(".search-container");
const hamburgerContainer = document.querySelector(".hamburger-container");
const logo = document.querySelector(".logo");
const searchExtend = document.querySelector(".search-extend");
const modalBackground = document.querySelector(".modal-background");

let isSearchContainerVisible = false;
let isHamburgerContainerVisible = false;
let isSearchExtendVisible = false;
let isModalBackgroundVisible = false;

searchButton.addEventListener("click", function () {
    if (!isSearchContainerVisible) {
        searchContainer.style.display = "flex";
        isSearchContainerVisible = true;
        logo.style.display = "none";
        searchExtend.style.display = "flex";
        modalBackground.style.display = "flex";

        if (isHamburgerContainerVisible) {
            hamburgerContainer.style.display = "none";
            isHamburgerContainerVisible = false;
        }
    } else {
        searchContainer.style.display = "none";
        isSearchContainerVisible = false;
        logo.style.display = "flex";
        searchExtend.style.display = "none";
        modalBackground.style.display = "none";
    }
});

hamburgerButton.addEventListener("click", function () {
    if (!isHamburgerContainerVisible) {
        hamburgerContainer.style.display = "flex";
        isHamburgerContainerVisible = true;
        modalBackground.style.display = "flex";

        if (isSearchContainerVisible) {
            searchContainer.style.display = "none";
            isSearchContainerVisible = false;
            logo.style.display = "flex";
            searchExtend.style.display = "none";
            modalBackground.style.display = "flex";
        }
    } else {
        hamburgerContainer.style.display = "none";
        isHamburgerContainerVisible = false;
        modalBackground.style.display = "none";
    }
});

// 로그아웃과 로그인 표시

document.addEventListener("DOMContentLoaded", function () {
    const logoutLink = document.getElementById("logout-link");
    const loginLink = document.getElementById("login-link");

    const isAuthenticated = logoutLink.getAttribute("data-authenticated");

    if (isAuthenticated === "True") {
        loginLink.style.display = "none";
        logoutLink.style.display = "flex";
    } else {
        loginLink.style.display = "flex";
        logoutLink.style.display = "none";
    }
});

// li 영역클릭으로 a의 기능 작동

document.addEventListener("DOMContentLoaded", function () {
    let recommendList = document.getElementById("recommendList");

    recommendList.addEventListener("click", function (event) {
        if (event.target.tagName === "LI") {
            let searchText = event.target.textContent;

            window.location.href = "/search/?search=" + searchText;
        }
    });
});
