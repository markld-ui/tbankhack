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

document.addEventListener("DOMContentLoaded", function () {
    const registerModal = document.getElementById("register-modal");
    const closeRegisterBtn = document.getElementById("close-register");
    const employerBtn = document.getElementById("employer-btn");
    const traineeBtn = document.getElementById("trainee-btn");
    const employerPanel = document.getElementById("employer-panel");
    const traineePanel = document.getElementById("trainee-panel");

    // Функция для открытия панели работодателя
    function openEmployerPanel() {
        closeTraineePanel();
        employerPanel.classList.add("show");
    }

    // Функция для закрытия панели работодателя
    function closeEmployerPanel() {
        employerPanel.classList.remove("show");
    }

    // Функция для открытия панели стажёра
    function openTraineePanel() {
        closeEmployerPanel();
        traineePanel.classList.add("show");
    }

    // Функция для закрытия панели стажёра
    function closeTraineePanel() {
        traineePanel.classList.remove("show");
    }

    // Функция для закрытия модального окна регистрации
    function closeRegisterModal() {
        registerModal.style.display = "none";
    }

    // Привязываем кнопки к функциям открытия
    if (employerBtn) employerBtn.onclick = openEmployerPanel;
    if (traineeBtn) traineeBtn.onclick = openTraineePanel;

    // Закрываем модальное окно при клике на крестик
    if (closeRegisterBtn) {
        closeRegisterBtn.addEventListener("click", closeRegisterModal);
    }

    // Закрываем модальное окно при клике вне его области
    window.addEventListener("click", function (event) {
        if (event.target === registerModal) {
            closeRegisterModal();
        }
    });
});











document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("resumeModal"); // Получаем модальное окно
    const closeModalButton = document.getElementById("closeModal"); // Кнопка закрытия
    const resumeTextElement = document.getElementById("resumeText"); // Блок с резюме

    // Функция открытия модального окна
    function openModal(resumeModal) {
        resumeTextElement.innerText = resumeModal; // Устанавливаем текст резюме
        modal.style.display = "flex"; // Показываем окно
    }

    // Функция закрытия модального окна
    function closeModal() {
        modal.style.display = "none"; // Скрываем окно
    }

    // Закрытие по клику на крестик
    closeModalButton.addEventListener("click", closeModal);

    // Закрытие по клику вне окна
    window.addEventListener("click", function (event) {
        if (event.target === modal) {
            closeModal();
        }
    });

    // Обработчики клика на кнопки "Подробнее"
    document.querySelectorAll(".additionaly").forEach(button => { // Примечание: класс должен быть ".additional"
        button.addEventListener("click", function () {
            const candidateName = this.closest(".internship-item").querySelector(".company-name").innerText; // Получаем имя
            const resumeText = `Резюме кандидата: ${candidateName}\n\nОпыт работы: 3 года.\nНавыки: JavaScript, React, Node.js.\nОбразование: Высшее, МГУ.`; // Данные
            openModal(resumeText); // Открываем окно
        });
    });
});

