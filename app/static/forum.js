import { CookieManager } from "./helpers/cookie_manager.js";

const threads = [];

$(document).ready(() => {
    fetch("/api/threads", {
        method: "GET", headers: {
            Authorization: `Bearer ${CookieManager.getCookie("token")}`,
            "Content-type": "application/json; charset=UTF-8"
        }
    }).then(r => {
        if (r.ok) {
            r.json().then(
                o => {
                    threads.push(o);
                    o.forEach(thread => {
                        $("#threads").append(`<li><a href="/thread/${thread.id}">${thread.title}</a></li>`)
                    });
                }
            )
        } else {
            alert(`The server did not return a valid response! HTTP error code is ${r.status} (${r.statusText})`)
        }
    })

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
                r.json().then(o => {
                    threads.push(o);
                    $("#threads").append(`<li><a href="/thread/${o.id}">${o.title}</a></li>`);
                });
            } else {
                alert(`The server did not return a valid response! HTTP error code is ${r.status} (${r.statusText})`)
            }
        })
    });
});