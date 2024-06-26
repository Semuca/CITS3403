import { CookieManager } from "./helpers/cookie_manager.js";

import { showErrorBanner } from "./helpers/error_banner.js";
import { dateFromPythonTime, timeFromPythonTime } from "./helpers/format_time.js"

const perPage = 5;
let pageNumber = 1
let ascending = false;
let totalPages = 0;

$(document).ready(() => {
    loadPage(1)

    $(".pagination").on("click", "#firstPage", function() {
        loadPage(1);
    });
    $(".pagination").on("click", "#nextPage", function() {
        loadPage(pageNumber + 1);
    });
    $(".pagination").on("click", "#prevPage", function() {
        loadPage(pageNumber - 1);
    });
    $(".pagination").on("click", "#lastPage", function() {
        loadPage(totalPages);
    });

    $(".pagination").on("click", ".page-item:not(.page-nav)", function() {
        const page = $(this).find(".page-link").text();
        loadPage(parseInt(page));
    });

    $("#submit").on("click", () => {
        fetch("/api/threads", {
            method: "POST",
            headers: {
                Authorization: `Bearer ${CookieManager.getCookie("token")}`,
                "Content-type": "application/json; charset=UTF-8"
            },
            body: JSON.stringify({
                title: $("#title").val(),
                description: $("#description").val(),
            })
        }).then(r => {
            if (r.ok) {
                location.reload()
            } else {
                showErrorBanner(r.statusText);
            }
        });
    });

    $("#order").on("click", () => {
        ascending = !ascending;
        $("#order").text(ascending ? "Ascending" : "Descending");
        loadPage(1);
    });

    $("#sortBy").on("change", () => {
        loadPage(1);
    });

    $("#searchbar").on('keydown', e => {
        if (e.which == 13) {
            loadPage(1, $("#searchbar").val());
        }
    });
});

function loadPage(page, search = "") {
    pageNumber = page
    $("#threads").empty();

    const direction = ascending ? "asc" : "desc";
    const sort = $("#sortBy").val();
    let query = `/api/threads?perPage=${perPage}&page=${page}&sortBy=${sort}&sortDir=${direction}`;
    if (search) {
        query += `&search=${search}`;
    }

    fetch(query, {
        method: "GET", headers: {
            Authorization: `Bearer ${CookieManager.getCookie("token")}`,
            "Content-type": "application/json; charset=UTF-8"
        }
    })
    .then(res => {
        if (!res.ok) {
            showErrorBanner(res.statusText);
        }
        return res.json();
    })
    .then(data => {
        updateNavLinks(page, data.total);

        data.threads.forEach(thread => {
            $("#threads").append(`
                <li>
                    <div class="thread-time">
                        <span class="date">${dateFromPythonTime(thread.createdAt)}</span>
                        <span class="time">${timeFromPythonTime(thread.createdAt)}</span>
                    </div>
                    <div class="thread-body">
                        <div class="thread-header">
                            <span class="thread-name"><a id="thread-${thread.id}" href="/thread/${thread.id}">${thread.title}</a> <small></small></span>
                            <br>
                            <span class="thread-creator username"><p class="text-black">${thread.user.username}</p> <small></small></span>
                        </div>
                        <div class="thread-content">
                            <p class="text-secondary">${thread.description}</p>
                        </div>
                    </div>
                </li>
            `);
        });
    });
}

function updateNavLinks(currentPage, lastPage) {
    const pagination = $(".pagination");
    pagination.empty();

    // Calculate page range based on current page and total pages - up to 5 pages currently
    const startPage = Math.max(currentPage - 2, 1);
    const endPage = Math.min(currentPage + 2, lastPage);
    totalPages = lastPage;

    pagination.append(`
        <li class="page-item page-nav"><a id="firstPage" class="page-link" tabindex="-1">\<\<</a></li>
    `);
    if (currentPage > 1) {
        pagination.find("#firstPage").removeClass("disabled");
    } else {
        pagination.find("#firstPage").addClass("disabled");
    }

    pagination.append(`
        <li class="page-item page-nav"><a id="prevPage" class="page-link" tabindex="-1">\<</a></li>
    `);
    if (currentPage > Math.min(startPage, 1)) {
        pagination.find("#prevPage").removeClass("disabled");
    } else {
        pagination.find("#prevPage").addClass("disabled");
    }

    for (let i = startPage; i <= endPage; i++) {
        pagination.append(`
            <li class="page-item">
                <a class="${i === currentPage ? 'active' : ''} page-link">${i}</a>
            </li>
        `);
    }

    pagination.append(`
        <li class="page-item page-nav"><a id="nextPage" class="page-link" tabindex="-1">\></a></li>
    `);
    if (currentPage < lastPage) {
        pagination.find("#nextPage").removeClass("disabled");
    } else {
        pagination.find("#nextPage").addClass("disabled");
    }

    pagination.append(`
        <li class="page-item page-nav"><a id="lastPage" class="page-link" tabindex="-1">\>\></a></li>
    `);
    if (currentPage < Math.min(endPage, lastPage)) {
        pagination.find("#lastPage").removeClass("disabled");
    } else {
        pagination.find("#lastPage").addClass("disabled");
    }
}

