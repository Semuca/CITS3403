import {CookieManager} from "./helpers/cookie_manager.js";

$("#submit").on("click", () => {
    fetch("/api/threads", {
        method: "POST", headers: {
            Authorization: `Bearer ${CookieManager.getCookie("token")}`,
            "Content-type": "application/json; charset=UTF-8"
        }, body: JSON.stringify({
            title: $("#title").val(),
            description: $("#description").val(),
        })
    }).then(r => {
        if (r.ok) {
            location.href = "/forum"
        } else {
            alert(`The server did not return a valid response! HTTP error code is ${r.status} (${r.statusText})`)
        }
    })
});