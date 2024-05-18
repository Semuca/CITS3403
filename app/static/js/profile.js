import { CookieManager } from "./helpers/cookie_manager.js";
import { hash } from "./helpers/crypto.js";
import { showErrorBanner } from "./helpers/error_banner.js";

jQuery(() => {
    $("#updateProfile").on("click",() => {
        const description = $("#description").val();
        const password = $("#password").val();
        const securityQuestion = $("#securityQuestion").val();
        const securityQuestionAnswer = $("#securityQuestionAnswer").val();

        const body = {};

        if (description) {
            body.description = description;
        }

        if (password) {
            body.password = hash(password);
        }

        if (securityQuestion) {
            body.securityQuestion = securityQuestion;
        }

        if (securityQuestionAnswer) {
            body.securityQuestionAnswer = hash(securityQuestionAnswer);
        }

        fetch("/api/users", {
            method: "PUT", body: JSON.stringify(body), headers: {
                Authorization: `Bearer ${CookieManager.getCookie("token")}`,
                "Content-type": "application/json; charset=UTF-8"
            }
        }).then(r => {
            if (r.ok) {
                window.location.reload();
            } else {
                showErrorBanner(r.statusText);
            }
        })
    })
})
