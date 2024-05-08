import { CookieManager } from "./helpers/cookie_manager.js";


$(document).ready(() => {
    const threadId = $("#threadScript").data().threadId;
    console.log($("#threadScript").data());

    // Loading thread post
    fetch(`/api/threads/${threadId}`, {
        method: "GET", headers: {
            Authorization: `Bearer ${CookieManager.getCookie("token")}`,
            "Content-type": "application/json; charset=UTF-8"
        }
    }).then(r => {
        if (r.ok) {
            r.json().then(
                o => {
                    $("#title").text(o.title);
                    $("#description").text(o.description);
                }
            )
        } else {
            alert(`The server did not return a valid response! HTTP error code is ${r.status} (${r.statusText})`)
        }
    })

    // Loading comments
    fetch(`/api/threads/${threadId}/children`, {
        method: "GET", headers: {
            Authorization: `Bearer ${CookieManager.getCookie("token")}`,
            "Content-type": "application/json; charset=UTF-8"
        }
    }).then(r => {
        if (r.ok) {
            r.json().then(
                o => {
                    o.forEach(child => {
                        $("#children").append(`<li>${child.commentText}</li>`)
                    });
                }
            )
        } else {
            alert(`The server did not return a valid response! HTTP error code is ${r.status} (${r.statusText})`)
        }
    })

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
                    $("#children").append(`<li>${o.commentText}</li>`)
                });
            } else {
                alert(`The server did not return a valid response! HTTP error code is ${r.status} (${r.statusText})`)
            }
        })
    });
});