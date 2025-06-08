document.addEventListener("DOMContentLoaded", function () {
    const btnLogin = document.getElementById("btn-login");
    const btnRegister = document.getElementById("btn-register");
    const formLogin = document.getElementById("form-login");
    const formRegister = document.getElementById("form-register");

    btnLogin.addEventListener("click", () => {
        formLogin.classList.add("active");
        formRegister.classList.remove("active");
        btnLogin.classList.add("active");
        btnRegister.classList.remove("active");
    });

    btnRegister.addEventListener("click", () => {
        formLogin.classList.remove("active");
        formRegister.classList.add("active");
        btnLogin.classList.remove("active");
        btnRegister.classList.add("active");
    });
});
