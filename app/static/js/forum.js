import { CookieManager } from "./helpers/cookie_manager.js";

const threads = [];
let pageNumber = 1
const pageBefore = $("#pageBefore")
const currentPage = $("#currentPage")
const pageAfter = $("#pageAfter")
const prevPage = $("#prevPage")
const nextPage = $("#nextPage")



$(document).ready(() => {
    loadPage(1)
    nextPage.on("click", () => {
        loadPage(pageNumber + 1)
        console.log("#nextPage")
    })
    prevPage.on("click", () => {
        loadPage(pageNumber - 1)
        console.log("#prevPage")
    })
    pageBefore.on("click", () => {
        loadPage(+pageBefore.text())
    })
    currentPage.on("click", () => {
        loadPage(+currentPage.text())
    })
    pageAfter.on("click", () => {
        loadPage(+pageAfter.text())
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
                                    </div>const
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
    pageNumber = page
    while (threads.length) {
        threads.pop()
    }
    if (page === 1) {
        prevPage.addClass("disabled")
        pageBefore.addClass("active")
        currentPage.removeClass("active")
        pageBefore.text("1")
        currentPage.text("2")
        pageAfter.text("3")
    } else {
        prevPage.removeClass("disabled")
        pageBefore.removeClass("active")
        currentPage.addClass("active")
        pageBefore.text(pageNumber - 1)
        currentPage.text(pageNumber)
        pageAfter.text(pageNumber + 1)
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