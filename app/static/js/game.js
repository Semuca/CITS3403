import {CookieManager} from "./helpers/cookie_manager.js";

let levelTime = Date.now() + Math.random() * 1000 * 1000
let lootTime = Date.now() + Math.random() * 1000 * 1000


$(document).ready(() => {
    setInterval(everySecond, 1000)


    $("#collectLoot").on("click", e => {
        fetch("/api/loot", {
            method: "GET", headers: {
                Authorization: `Bearer ${CookieManager.getCookie("token")}`,
                "Content-type": "application/json; charset=UTF-8"
            }
        }).then(r => {
            if (r.ok) {
                location.reload()
            } else {
                r.json().then(o => {
                    alert(o.errorMessage)
                })
            }
        })
    })

    $("#levelImmediately").on("click", e => {
        fetch("/api/levelup", {
            method: "GET", headers: {
                Authorization: `Bearer ${CookieManager.getCookie("token")}`,
                "Content-type": "application/json; charset=UTF-8"
            }
        }).then(r => {
            if (r.ok) {
                location.reload()
            } else {
                r.json().then(o => {
                    alert(o.errorMessage)
                })
            }
        })
    })



    //TODO: fix to backend (placeholder URLs)
    fetch(`/magic/address/to/level/countdown`, {
        method: "GET", headers: {
            Authorization: `Bearer ${CookieManager.getCookie("token")}`,
            "Content-type": "application/json; charset=UTF-8"
        }
    }).then(r => {
        if (r.ok) {
            r.json().then(j => {
                levelTime = j.timeLeft
            })
        } else {
            // alert("Something has gone horribly wrong...")
        }
    })
    //TODO: fix to backend (placeholder URLs)
    fetch(`/magic/address/to/loot/countdown`, {
        method: "GET", headers: {
            Authorization: `Bearer ${CookieManager.getCookie("token")}`,
            "Content-type": "application/json; charset=UTF-8"
        }
    }).then(r => {
        if (r.ok) {
            r.json().then(j => {
                lootTime = j.timeLeft
            })
        } else {
            // alert("Something has gone horribly wrong...")
        }
    })
});


function everySecond() {
    let diff = (levelTime - Date.now())
    let text = new Date(diff).toISOString().slice(11, -5);
    $("#levelTime").text(text)
    diff = (lootTime - Date.now())
    text = new Date(diff).toISOString().slice(11, -5);
    $("#lootTime").text(text)
}
