import { CookieManager } from "./helpers/cookie_manager.js";

$(document).ready(() => {
    $.ajaxSetup({
        headers: {
            "X-CSRFToken": "{{ csrf_token() }}"
        }
    });

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
                alert(`The server did not return a valid response! HTTP error code is ${r.status} (${r.statusText})`)
            }
        })
    });
});