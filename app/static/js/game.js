import {CookieManager} from "./helpers/cookie_manager.js";

let user = null;
let levelTime = Date.now();
let lootTime = Date.now();

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

    // get timer values from the user object
    fetch("/api/users", {
        method: "GET", headers: {
            Authorization: `Bearer ${CookieManager.getCookie("token")}`,
            "Content-type": "application/json; charset=UTF-8"
        }
    }).then(r => {
        if (r.ok) {
            r.json().then(j => {
                console.log("BBBBB", j);
                user = j;
                levelTime = new Date(user.levelExpiry).getTime();
                lootTime = new Date(user.lootDropRefresh).getTime();
                console.log("AAAAA", levelTime, lootTime);
            })
        } else {
            // alert("Something has gone horribly wrong...")
        }
    })
});


function everySecond() {
    // if user object is not yet loaded, do nothing
    if (!user) return;

    // if level is 0, then keep timers at 00:00:00
    let level = parseInt($("#level").text())
    if (level === 0) return;

    let timeLeft = levelExpiryToTimer(levelTime)
    $("#levelTime").text(timeLeft)

    timeLeft = lootCooldownToTimer(lootTime)
    $("#lootTime").text(timeLeft)
}

// converts the expiry time to the amount of time left in the format HH:MM:SS
function levelExpiryToTimer(expiry) {
    // if time is up, reload since auto-levelling happens in the backend
    if (expiry < Date.now()) {
        location.reload()
    }

    // calculate time left
    let diff = new Date(expiry - Date.now());
    return diff.toUTCString().slice(17, 25); // HH:MM:SS
}

// converts the loot cooldown time to the amount of time left in the format HH:MM:SS
function lootCooldownToTimer(cooldown) {
    // if cooldown is up, time left to next collection is 00:00:00
    if (cooldown < Date.now()) {
        return;
    }

    // calculate time left
    let diff = new Date(cooldown - Date.now());
    return diff.toUTCString().slice(17, 25); // HH:MM:SS
}
