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
    if (loginBtn) loginBtn.addEventListener("click", openLoginPanel);
    if (closeBtn) closeBtn.addEventListener("click", closeLoginPanel);
});
