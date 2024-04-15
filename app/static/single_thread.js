import {CookieManager} from "./helpers/cookie_manager";

jQuery(() => {
    let split = location.href.split("/")
    let id = split[split.length - 1]
    fetch(`/api/threads/${id}`, {
        method: "GET", headers: {
            Authorization: `Bearer ${CookieManager.getCookie("token")}`,
            "Content-type": "application/json; charset=UTF-8"
        }
    }).then(r => {
        if (r.ok) {
            r.json().then(
                o => {
                    $("#title").textContent = o.title
                    $("#description").textContent = o.description
                }
            )
        } else {
            alert(`The server did not return a valid response! HTTP error code is ${r.status} (${r.statusText})`)
        }
    })
})