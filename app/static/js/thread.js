import {CookieManager} from "./helpers/cookie_manager.js";
import {dateFromPythonTime, timeFromPythonTime} from "./helpers/format_time.js";


$(document).ready(() => {
    const threadId = $("#threadScript").data().threadId;
    fetch(`/api/threads/${threadId}/children`, {
        method: "POST", headers: {
            Authorization: `Bearer ${CookieManager.getCookie("token")}`,
            "Content-type": "application/json; charset=UTF-8"
        }
    }).then(r => {
        if (r.ok) {
            r.json().then(j => {
                for (const i in j) {
                   $("#comments").append(`
                       <li>
                           <div className="timeline-time">
                               <span className="date">${dateFromPythonTime(i.created_at)}</span>
                               <span className="time">${timeFromPythonTime(i.created_at)}</span>
                           </div>
                           <div className="timeline-body">
                               <div className="timeline-content">
                                   <h5 className="comment-username mb-1">${i.username}</h5>
                                   <p>{{i.comment_text}}</p>
                               </div>
                           </div>
                       </li>`
                   )
                }
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
                    //easier to reload the page and let the server deal with adding a new comment...
                    location.reload()
                });
            } else {
                alert(`The server did not return a valid response! HTTP error code is ${r.status} (${r.statusText})`)
            }
        })
    });
})
;