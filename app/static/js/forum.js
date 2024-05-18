import { CookieManager } from "./helpers/cookie_manager.js";

import { showErrorBanner } from "./helpers/error_banner.js";
import { dateFromPythonTime, timeFromPythonTime } from "./helpers/format_time.js"

const threads = [];
let pageNumber = 1
const pageBefore = $("#pageBefore")
const currentPage = $("#currentPage")
const pageAfter = $("#pageAfter")
const prevPage = $("#prevPage")
const nextPage = $("#nextPage")
let ascending = false

$(document).ready(() => {
    loadPage(1)
    nextPage.on("click", () => {
        loadPage(pageNumber + 1)
    })
    prevPage.on("click", () => {
        loadPage(pageNumber - 1)
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
                location.reload()
            } else {
                showErrorBanner(r.statusText);
            }
        })
    });

    $("#order").on("click", () => {
        ascending = !ascending
        $("#ascending").text(ascending ? "Ascending" : "Descending")
        loadPage(1)
    })
    $("#sortBy").on("change", e => {
        loadPage(1)
    })

    $("#searchbar").on('keydown', e => {
        if (e.which == 13) {
            loadPage(1, $("#searchbar").val())
        }
    })
});

function loadPage(page, search = "") {
    pageNumber = page
    threads.length = 0 //empty the threads array
    if (page === 1) {
        prevPage.addClass("disabled")
        pageBefore.addClass("active")
        currentPage.removeClass("active")
    } else {
        prevPage.removeClass("disabled")
        pageBefore.removeClass("active")
        currentPage.addClass("active")
    }
    const smallestPageNumber = Math.max(pageNumber - 1, 1)
    pageBefore.text(smallestPageNumber)
    currentPage.text(smallestPageNumber + 1)
    pageAfter.text(smallestPageNumber + 2)
    $("#threads").empty()
    const direction = ascending ? "asc" : "desc"
    const sort = $("#sortBy").val()
    let query = `/api/threads?perPage=10&page=${page}&sortBy=${sort}&sortDir=${direction}`
    if (search) {
        query += `&search=${search}`
    }
    fetch(query, {
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
                            <li>
                                <div class="thread-time">
                                    <span class="date">${dateFromPythonTime(thread.createdAt)}</span>
                                    <span class="time">${timeFromPythonTime(thread.createdAt)}</span>
                                </div>
                                <div class="thread-body">
                                    <div class="thread-header">
                                        <span class="thread-name"><a href="/thread/${thread.id}">${thread.title}</a> <small></small></span>
                                        <br>
                                        <span class="thread-creator username"><a href="javascript:;">${thread.user.username}</a> <small></small></span>
                                    </div>
                                    <div class="thread-content">
                                        <p class="text-secondary">${thread.description}</p>
                                    </div>
                                </div>
                            </li>
                        `)
                    });
                }
            )
        } else {
            showErrorBanner(r.statusText);
        }
    })
}