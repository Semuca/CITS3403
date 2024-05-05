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
                        $("#threads").append(`
                            <li>
                                <div class="thread-time">
                                    <span class="date">today</span>
                                    <span class="time">04:20</span>
                                </div>
                                <div class="thread-body">
                                    <div class="thread-header">
                                        <span class="thread-name"><a href="/thread/${thread.id}">${thread.title}</a> <small></small></span>
                                        <span class="userimage"><img src="{{ url_for('static', filename='images/jsMug.png') }}" alt=""></span>
                                        <span class="username"><a href="javascript:;">TODO:USERNAME</a> <small></small></span>
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
                r.json().then(thread => {
                    threads.push(thread);
                    $("#threads").append(`
                        <li>
                            <div class="thread-time">
                                <span class="date">today</span>
                                <span class="time">04:20</span>
                            </div>
                            <div class="thread-body">
                                <div class="thread-header">
                                    <span class="thread-name"><a href="/thread/${thread.id}">${thread.title}</a> <small></small></span>
                                    <span class="userimage"><img src="{{ url_for('static', filename='images/jsMug.png') }}" alt=""></span>
                                    <span class="username"><a href="javascript:;">USERNAME</a> <small></small></span>
                                </div>
                                <div class="thread-content">
                                    <p class="text-secondary">${thread.description}</p>
                                </div>
                            </div>
                        </li>
                    `);
                    $('#threadCreationModal').modal('hide');
                });
            } else {
                alert(`The server did not return a valid response! HTTP error code is ${r.status} (${r.statusText})`)
            }
        })
    });
});