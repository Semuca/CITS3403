import {CookieManager} from "./helpers/cookie_manager.js";
import {hash} from "./helpers/crypto.js";
import {showErrorBanner} from "./helpers/error_banner.js";

let inRecoveryMode = false;
let passwordToken = undefined

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
        const body = JSON.stringify({
                username: $("#username").val(),
                password: hash($("#password").val()),
                securityQuestion: $("#question").val(),
                securityQuestionAnswer: hash($("#answer").val())
            }
        )
        fetch("/api/users", {
            method: "POST", body: body, headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        }).then(r => {
            if (r.ok) {
                r.json().then(o => {
                    CookieManager.setCookie("token", o.token)
                    window.location = "/forum"
                });
            } else {
                showErrorBanner(r.statusText);
            }
        })

    })

    $("#forgot").on("click", () => {
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
    const body = JSON.stringify({
            changePasswordToken: passwordToken,
            password: (hash($("#newPassword").val()))

        }
    )

    fetch("/api/login/password", {
        method: "POST", body: body, headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    }).then(r => {
        if (r.ok) {
            r.json().then(o => {
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
    const body = JSON.stringify({
            username: $("#username").val(),
            securityQuestionAnswer: (hash($("#recoveryQuestion").val()))

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
            showErrorBanner(r.statusText);
        }
    })
}

function handleLogin() {
    const body = JSON.stringify({
            username: $("#username").val(),
            password: (hash($("#password").val()))
        }
    )


    fetch("/api/login", {
        method: "POST", body: body, headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    }).then(r => {
        if (r.ok) {
            r.json().then(o => {
                CookieManager.setCookie("token", o.token)
                location = "/forum"
            })
        } else {
            showErrorBanner(r.statusText);
        }
    })
}