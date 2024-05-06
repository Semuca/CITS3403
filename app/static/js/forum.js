import { CookieManager } from "./helpers/cookie_manager.js";

const threads = [];
let currentPage = 1

$(document).ready(() => {
    loadPage(1)
    $("#nextPage").on("click", () => {
        loadPage(++currentPage)
    })
    $("#prevPage").on("click", () => {
        loadPage(++currentPage)
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
                r.json().then(thread => {
                    threads.push(thread);
                    $("#threads").append(`
                        <div class="card mb-2">
                            <div class="card-body p-2 p-sm-3">
                                <div class="media forum-item">
                                    <div class="media-body">
                                        <a href="/thread/${thread.id}">${thread.title}</a>
                                        <p class="text-secondary">${thread.description}</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `);
                    $('#threadCreationModal').modal('hide');
                });
            } else {
                alert(`The server did not return a valid response! HTTP error code is ${r.status} (${r.statusText})`)
            }
        })
    });
});

function loadPage(page) {
    while (threads.length) {
        threads.pop()
    }
    $("#threads").empty()
    console.log(page)
    fetch(`/api/threads?perPage=10&page=${page}`, {
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
                        $("#threads").append(`
                            <div class="card mb-2">
                                <div class="card-body p-2 p-sm-3">
                                    <div class="media forum-item">
                                        <div class="media-body">
                                            <a href="/thread/${thread.id}">${thread.title}</a>
                                            <p class="text-secondary">${thread.description}</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        `)
                    });
                }
            )
        } else {
            alert(`The server did not return a valid response! HTTP error code is ${r.status} (${r.statusText})`)
        }
    })
}