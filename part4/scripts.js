/*
 * Login and places functions
 */

const API_URL = "http://127.0.0.1:5000/api/v1";


// Get cookie value
function getCookie(name) {
    const cookies = document.cookie.split(";");

    for (let cookie of cookies) {
        cookie = cookie.trim();

        if (cookie.startsWith(name + "=")) {
            return cookie.substring(name.length + 1);
        }
    }

    return null;
}


// Login user
function setupLogin() {

    const loginForm = document.getElementById("login-form");

    if (!loginForm) {
        return;
    }

    loginForm.addEventListener("submit", async (event) => {

        event.preventDefault();

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;


        try {

            const response = await fetch(
                `${API_URL}/auth/login`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        email,
                        password
                    })
                }
            );


            if (response.ok) {

                const data = await response.json();

                document.cookie =
                `token=${data.access_token}; path=/`;

                window.location.href = "index.html";

            } else {

                alert("Login failed");

            }


        } catch (error) {

            alert("Error connecting to server");

        }

    });

}


// Get places from API
async function fetchPlaces(token) {

    try {

        const response = await fetch(
            `${API_URL}/places/`,
            {
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );


        const places = await response.json();

        displayPlaces(places);


    } catch (error) {

        console.log("Error loading places");

    }

}


// Show places on page
function displayPlaces(places) {

    const list = document.getElementById("places-list");

    if (!list) {
        return;
    }


    list.innerHTML = "";


    places.forEach((place) => {

        const card = document.createElement("article");

        card.className = "place-card";

        card.dataset.price = place.price;


        card.innerHTML = `

            <img src="images/house1.jpg" alt="Place">

            <h2>${place.title}</h2>

            <p>${place.description || ""}</p>

            <p>Price per night: $${place.price}</p>

            <a href="place.html" class="details-button">
                View Details
            </a>

        `;


        list.appendChild(card);

    });


    setupFilter();

}


// Filter places by price
function setupFilter() {

    const filter = document.getElementById("price-filter");


    if (!filter) {
        return;
    }


    filter.addEventListener("change", (event) => {


        const maxPrice = event.target.value;

        const cards = document.querySelectorAll(".place-card");


        cards.forEach((card) => {


            const price = Number(card.dataset.price);


            if (maxPrice === "" || price <= Number(maxPrice)) {

                card.style.display = "block";

            } else {

                card.style.display = "none";

            }

        });

    });

}


// Check login status
function checkAuthentication() {

    const token = getCookie("token");

    const loginButton = document.querySelector(".login-button");


    if (!token) {

        if (loginButton) {
            loginButton.style.display = "block";
        }

    } else {

        if (loginButton) {
            loginButton.style.display = "none";
        }

        fetchPlaces(token);

    }

}


// Run when page loads
document.addEventListener("DOMContentLoaded", () => {

    setupLogin();

    checkAuthentication();

});

// regist an user

const registerForm = document.getElementById("register-form");

if (registerForm) {
    registerForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const response = await fetch(
            "http://127.0.0.1:5000/api/v1/users",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    first_name: document.getElementById("first_name").value,
                    last_name: document.getElementById("last_name").value,
                    email: document.getElementById("email").value,
                    password: document.getElementById("password").value
                })
            }
        );

        if (response.ok) {
            alert("User created");
            window.location.href = "login.html";
        } else {
            alert("Registration failed");
        }
    });
}