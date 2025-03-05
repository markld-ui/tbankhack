// Функция для открытия панели регистрации
function openEmployerPanel() {
    closeTraineePanel();
    document.getElementById("employer-panel").classList.add("show");
}

// Функция для закрытия панели регистрации
function closeEmployerPanel() {
    document.getElementById("employer-panel").classList.remove("show");
}

function openTraineePanel() {
    closeEmployerPanel();
    document.getElementById("trainee-panel").classList.add("show");
}

// Функция для закрытия панели регистрации
function closeTraineePanel() {
    document.getElementById("trainee-panel").classList.remove("show");
}

// Привязываем кнопки к функции открытия панели
document.getElementById("employer-btn").onclick = openEmployerPanel;
document.getElementById("trainee-btn").onclick = openTraineePanel;

document.addEventListener("DOMContentLoaded", function () {
    // Получаем элементы
    const loginModal = document.getElementById("loginModal");
    const loginBtn = document.getElementById("login-btn");
    const closeBtn = document.getElementById("close-login");

    // Функция для открытия окна входа
    function openLoginPanel() {
        loginModal.classList.add("show");
    }

    // Функция для закрытия окна входа
    function closeLoginPanel() {
        loginModal.classList.remove("show");
    }

    // Привязываем кнопки к функциям
    if (loginBtn) loginBtn.addEventListener("click", function() {
        openLoginPanel();
    });
    
    if (closeBtn) closeBtn.addEventListener("click", closeLoginPanel);

    // Функция входа
    document.getElementById("login-form").addEventListener("submit", function(event) {
        event.preventDefault();
        localStorage.setItem("loggedIn", "true");
        updateLoginButton();
        closeLoginPanel();
    });

    // Функция обновления кнопки входа
    function updateLoginButton() {
        if (localStorage.getItem("loggedIn") === "true") {
            loginBtn.textContent = "Выйти"; // Кнопка "Выйти" при успешном входе
        } else {
            loginBtn.textContent = "Вход"; // Кнопка "Вход", если пользователь не вошел
        }
    }

    // Проверяем состояние при загрузке страницы
    updateLoginButton();
});

document.addEventListener("DOMContentLoaded", function() {
    const container = document.querySelector(".container__information2");
    const starRating = document.querySelector(".star-rating");
    const ratingValueSpan = document.querySelector(".rating-value");
    const updateRatingButton = document.querySelector("#updateRatingButton"); // Кнопка для обновления рейтинга

    function updateRating() {
        // Получаем значение рейтинга из атрибута data-rating
        const ratingValue = parseFloat(container.dataset.rating);
        const ratingValueText = ratingValue.toFixed(1) + " / 5";

        if (starRating && ratingValueSpan) {
            const stars = starRating.querySelectorAll("i");

            for (let i = 0; i < stars.length; i++) {
                if (i < ratingValue) {
                    stars[i].classList.add("active");
                } else {
                    stars[i].classList.remove("active");
                }
            }

            ratingValueSpan.textContent = ratingValueText;
        } else {
            console.error("Не найдены элементы рейтинга!");
        }
    }

    // Вызываем функцию updateRating() при загрузке страницы, чтобы установить рейтинг при первой загрузке
    updateRating();

    // Вешаем обработчик события на кнопку
    updateRatingButton.addEventListener("click", function() {
        // Здесь можно изменить значение атрибута data-rating (например, случайным образом)
        const newRating = Math.random() * 5;  // Случайный рейтинг от 0 до 5
        container.dataset.rating = newRating.toFixed(1); // Обновляем значение в HTML
        updateRating(); // Обновляем отображение рейтинга
    });
});


// Функция для отображения помощи (для примера)
function showHelp() {
    alert('Помощь скоро будет доступна');
}

// Функция для обновления кнопки Вход/Выйти в зависимости от состояния авторизации
function updateLoginButton() {
    const loginBtn = document.getElementById("login-btn");
    if (localStorage.getItem("loggedIn") === "true") {
        loginBtn.textContent = "Выйти"; // Кнопка "Выйти", если пользователь авторизован
    } else {
        loginBtn.textContent = "Вход"; // Кнопка "Вход", если пользователь не авторизован
    }
}

// Функция для входа
function loginUser() {
    // Здесь можно добавить дополнительную логику для авторизации (например, запрос к серверу)
    localStorage.setItem("loggedIn", "true"); // Помечаем пользователя как вошедшего
    updateLoginButton();  // Обновляем кнопку
}

// Функция для выхода
function logoutUser() {
    localStorage.removeItem("loggedIn"); // Удаляем статус авторизации
    updateLoginButton();  // Обновляем кнопку
}

// Проверка состояния авторизации при загрузке страницы
document.addEventListener("DOMContentLoaded", function () {
    updateLoginButton();  // Проверяем состояние и обновляем кнопку сразу при загрузке страницы

    const loginBtn = document.getElementById("login-btn");
    loginBtn.addEventListener("click", function () {
        if (localStorage.getItem("loggedIn") === "true") {
            // Если пользователь авторизован, выполняем выход
            logoutUser();
            alert("Вы успешно вышли из аккаунта!");
        } else {
            // Если пользователь не авторизован, открываем модальное окно входа
            openLoginPanel();
        }
    });
});


function logout() {
    // Перенаправляем на главную страницу
    window.location.href = "index.html";
}

