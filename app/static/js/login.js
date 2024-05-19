import {CookieManager} from "./helpers/cookie_manager.js";
import {hash} from "./helpers/crypto.js";
import {showErrorBanner} from "./helpers/error_banner.js";

let inRecoveryMode = false;
let passwordToken = undefined

const loginErrorMessage = $("#loginErrorMessage")
const loginButton = $("#pressLogin")
const box = $("#passwordBox")

const QUESTIONS = [
    "What was the name of your first pet?",
    "In which city were you born?",
    "In what city or town did your parents meet?",
    "What is your favourite book?",
    "What is the name of the street you grew up on?"
]

jQuery(() => {
    loginButton.on("click", () => {
        if (passwordToken !== undefined) {
            handleNewPassword()
        } else if (inRecoveryMode) {
            handleRecovery()
        } else {
            handleLogin()
        }
    })

    $("#pressCreate").on("click", () => {

        const username = $("#username").val();
        const password = $("#password").val();
        const question = $("#question").val();
        const answer = $("#answer").val();

        if (!username) {
            loginErrorMessage.text("Username cannot be empty");
            return;
        }

        if (!password) {
            loginErrorMessage.text("Password cannot be empty");
            return;
        }

        if (!answer) {
            loginErrorMessage.text("Answer cannot be empty");
            return;
        }

        const body = JSON.stringify({
                username: username,
                password: hash(password),
                securityQuestion: question,
                securityQuestionAnswer: hash(answer)
            }
        )
        fetch("/api/users", {
            method: "POST", body: body, headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        }).then(r => {
            if (r.ok) {
                r.json().then(o => {
                    CookieManager.setCookie("id", o.id)
                    CookieManager.setCookie("token", o.token)
                    window.location = "/forum"
                });
            } else {
                loginErrorMessage.text("Username already exists");
            }
        })

    })

    $("#forgot").on("click", () => {
        const username = $("#username").val();
        if (!username) {
            loginErrorMessage.text("Please enter a username to recover your account");
            return;
        }

        fetch(`/api/users/${$("#username").val()}/question`, {
            method: "GET", headers: {
                Authorization: `Bearer ${CookieManager.getCookie("token")}`,
                "Content-type": "application/json; charset=UTF-8"
            }
        }).then(r => {
            if (r.ok) {
                r.json().then(j => {
                    inRecoveryMode = true
                    const username = $("#username")
                    username.prop('disabled', true);
                    username.addClass("disabled");
                    box.empty()
                    box.append(`
                        <input type="text" id="recoveryQuestion" class="form-control form-control-lg"/>
                        <label for="recoveryQuestion" class="form-label">${QUESTIONS[j.question - 1]}</label>
                    `)
                    loginButton.text("Answer Security Question")
                })
            } else {
                showErrorBanner(r.statusText);
            }
        })
    })
})


function handleNewPassword() {
    const password = $("#newPassword").val();

    if (!password) {
        loginErrorMessage.text("New password cannot be empty");
        return;
    }

    const body = JSON.stringify({
            changePasswordToken: passwordToken,
            password: hash(password)
        }
    )

    fetch("/api/login/password", {
        method: "POST", body: body, headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    }).then(r => {
        if (r.ok) {
            r.json().then(o => {
                CookieManager.setCookie("id", o.id)
                CookieManager.setCookie("token", o.token)
                CookieManager.deleteCookie("changePasswordToken")
                location = "/forum"
            })
        } else {
            showErrorBanner(r.statusText);
        }
    })
}

function handleRecovery() {
    const securityQuestionAnswer = $("#recoveryQuestion").val();

    if (!securityQuestionAnswer) {
        loginErrorMessage.text("Answer cannot be empty");
        return;
    }

    const body = JSON.stringify({
            username: $("#username").val(),
            securityQuestionAnswer: hash(securityQuestionAnswer)
        }
    )

    fetch("/api/login/questions", {
        method: "POST", body: body, headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    }).then(r => {
        if (r.ok) {
            r.json().then(o => {
                passwordToken = o.token
                box.empty()
                box.append(`
                        <input type="password" id="newPassword" class="form-control form-control-lg"/>
                        <label for="recoveryQuestion" class="form-label">New Password</label>
                    `)
                loginButton.text("Change Password")
            })
        } else {
            loginErrorMessage.text("Incorrect answer");
        }
    })
}

function handleLogin() {
    const username = $("#username").val();
    const password = $("#password").val();

    if (!username) {
        loginErrorMessage.text("Username cannot be empty");
        return;
    }

    if (!password) {
        loginErrorMessage.text("Password cannot be empty");
        return;
    }

    const body = JSON.stringify({
            username: username,
            password: hash(password)
        }
    )


    fetch("/api/login", {
        method: "POST", body: body, headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    }).then(r => {
        if (r.ok) {
            r.json().then(o => {
                CookieManager.setCookie("id", o.id)
                CookieManager.setCookie("token", o.token)
                location = "/forum"
            })
        } else {
            loginErrorMessage.text("Invalid username or password");
        }
    })
}