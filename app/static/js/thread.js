import {CookieManager} from "./helpers/cookie_manager.js";
import {dateFromPythonTime, timeFromPythonTime} from "./helpers/format_time.js";
import {showErrorBanner} from "./helpers/error_banner.js";

const ITEMS = ["Boar", "Cheese", "Emerald", "Feather", "Horn", "Ink", "Meat", "Mushroom", "Orb", "Scroll"]

const threadId = $("#threadScript").data().threadId;

const threadPosterId = $("#threadScript").data().posterId;
const isThreadOwner = threadPosterId.toString() === CookieManager.getCookie("id");

function acceptTrade(id) {
    fetch(`/api/threads/${threadId}/offers/${id}`, {
        method: "POST", headers: {
            Authorization: `Bearer ${CookieManager.getCookie("token")}`,
            "Content-type": "application/json; charset=UTF-8"
        }
    }).then(o => {
        if (!o.ok) {
            switch (o.status) {
                case 400: {
                    alert("You do not have the correct amount of items for this trade!")
                    break
                }
                default:
                    showErrorBanner(o.statusText);
            }
        }
    })
}


$(document).ready(() => {
    fetch(`/api/threads/${threadId}/children`, {
        method: "GET", headers: {
            Authorization: `Bearer ${CookieManager.getCookie("token")}`,
            "Content-type": "application/json; charset=UTF-8"
        }
    }).then(r => {
        if (r.ok) {
            r.json().then(j => {
                for (const i of j) {
                    if (i.childType === "comment") {
                        $("#comments").append(`
                        <li>
                            <div class="timeline-time">
                                <span class="date">${dateFromPythonTime(i.createdAt)}</span>
                                <span class="time">${timeFromPythonTime(i.createdAt)}</span>
                            </div>
                            <div class="timeline-body">
                                <div class="timeline-content">
                                    <h5 class="comment-username mb-1">${i.user.username}</h5>
                                    <p>${i.commentText}</p>
                                </div>
                            </div>
                        </li>`
                        )
                    } else {
                        const isOfferOwner = i.user.id.toString() === CookieManager.getCookie("id");
                        $("#comments").append(`
                        <li>
                            <div class="timeline-time">
                                <span class="date">${dateFromPythonTime(i.createdAt)}</span>
                                <span class="time">${timeFromPythonTime(i.createdAt)}</span>
                            </div>
                            <div class="timeline-body">
                                <div class="timeline-content">
                                    <h4>Trade Request from ${isOfferOwner ? 'you' : i.user.username}</h4>
                                    <h5>${isOfferOwner ? 'You give' : `${i.user.username} gives`}:</h5>
                                    ${displayItems(i.offering)}
                                    <h5>${isThreadOwner ? 'You give' : 'Thread owner gives'}:</h5>
                                    ${displayItems(i.wanting)}
                                    <br>
                                    ${isThreadOwner ? `<button class="trade btn btn-primary mt-2" id="${i.id}">Accept</button>` : ''}
                                </div>
                            </div>
                        </li>`)
                    }

                }
                $(".trade").on("click", (e) => {
                    acceptTrade(e.target.id)
                })

            })
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
                    location.reload()
                });
            } else {
                alert(`The server did not return a valid response! HTTP error code is ${r.status} (${r.statusText})`)
            }
        })
    });

    $("#newTrade").on("click", () => {
        let offer = []
        let want = []
        for (let i = 0; i < 10; i++) {
            offer.push(+$(`#give${i}`).val())
            want.push(+$(`#get${i}`).val())
        }
        fetch(`/api/threads/${threadId}/offers`, {
            method: "POST", headers: {
                Authorization: `Bearer ${CookieManager.getCookie("token")}`,
                "Content-type": "application/json; charset=UTF-8"
            }, body: JSON.stringify({
                offeringList: offer,
                wantingList: want
            })
        }).then(r => {
            if (r.ok) {
                r.json().then(o => {
                    location.reload()
                });
            } else {
                showErrorBanner(r.statusText);
            }
        })
    });
})



function displayItems(wanting) {
    let out = ""
    for (const i in wanting) {
        if (wanting[i] === 0) {
            continue;
        }
        out += `${wanting[i]} <img src="/static/images/${i}${ITEMS[i]}.png" class="baby-image"> &nbsp&nbsp`
    }
    return out
}