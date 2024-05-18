import { CookieManager } from "./helpers/cookie_manager.js";
import { hash } from "./helpers/crypto.js";
import { showErrorBanner } from "./helpers/error_banner.js";

jQuery(() => {
    $("#pressLogin").on("click",() => {
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
                    window.location = "/forum"
                })
            } else {
                showErrorBanner(r.statusText);
            }
        })
    })

    $("#pressCreate").on("click",() => {
        console.log($("#password").val())
        const body = JSON.stringify({
                username: $("#username").val(),
                password: hash($("#password").val()),
                securityQuestion: +$("#question").val(),
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
})
