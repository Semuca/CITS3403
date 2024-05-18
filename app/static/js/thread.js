import { CookieManager } from "./helpers/cookie_manager.js";
import { showErrorBanner } from "./helpers/error_banner.js";


$(document).ready(() => {
    const threadId = $("#threadScript").data().threadId;
    console.log($("#threadScript").data());

    // Submitting comment
    $("#submit").on("click", () => {
        fetch(`/api/threads/${threadId}/comments`, {
            method: "POST", headers: {
                Authorization: `Bearer ${CookieManager.getCookie("token")}`,
                "Content-type": "application/json; charset=UTF-8"
            }, body: JSON.stringify({
                commentText: $("#commentText").val(),
            })
        }).then(r => {
            if (r.ok) {
                r.json().then(o => {
                    //easier to reload the page and let the server deal with adding a new comment...
                    location.reload()
                });
            } else {
                showErrorBanner(r.statusText);
            }
        })
    });
});