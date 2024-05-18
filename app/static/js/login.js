import { CookieManager } from "./helpers/cookie_manager.js";

const CryptoJS = window.CryptoJS;
const hash = function(text) {
    return CryptoJS.SHA256(text).toString(CryptoJS.enc.Hex);
}

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
                alert(`The server did not return a valid response! HTTP error code is ${r.status} (${r.statusText}) (${r.body.getReader().read()})`)
            }
        })
    })

    $("#pressCreate").on("click",() => {
        const body = JSON.stringify({
                username: $("#username").val(),
                password: (hash($("#password").val())),
                securityQuestion: 1,
                securityQuestionAnswer: "test"
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
                alert(`The server did not return a valid response! HTTP error code is ${r.status} (${r.statusText})`)
            }
        })

    })
})
