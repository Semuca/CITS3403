import {CookieManager} from "./helpers/cookie_manager.js";
import { showErrorBanner } from "./helpers/error_banner.js";

let user = undefined;
let levelTime = undefined;
let lootTime = undefined;

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
                showErrorBanner(r.statusText);
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
                showErrorBanner(r.statusText);
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
                user = j;

                levelTime = new Date(user.levelExpiry).getTime();
                lootTime = new Date(user.lootDropRefresh).getTime();

                const level = parseInt($("#level").text());

                if (level != 0 && !user.requiredInventory.find((requiredItem, index) => user.inventory[index] < requiredItem)) {
                    $("#levelImmediately").prop("disabled", false);
                }
            })
        } else {
            showErrorBanner(r.statusText);
        }
    })
});


function everySecond() {
    // if user object is not yet loaded, do nothing
    if (!user) return;

    $("#levelTime").text(levelExpiryToTimer(levelTime));
    $("#lootTime").text(lootCooldownToTimer(lootTime));
}

// converts the expiry time to the amount of time left in the format HH:MM:SS
function levelExpiryToTimer(expiry) {
    const level = parseInt($("#level").text());
    if (level === 0) return "00:00:00";

    // if time is up, reload since auto-levelling happens in the backend
    if (expiry < Date.now()) {
        location.reload()
    }

    // calculate time left
    const diff = new Date(expiry - Date.now());
    return diff.toUTCString().slice(17, 25); // HH:MM:SS
}

// converts the loot cooldown time to the amount of time left in the format HH:MM:SS
function lootCooldownToTimer(cooldown) {
    const level = parseInt($("#level").text());

    // if cooldown is up, time left to next collection is 00:00:00
    if (level === 0 || cooldown < Date.now()) {
        $("#collectLoot").prop("disabled", false);
        return "00:00:00";
    }

    // calculate time left
    const diff = new Date(cooldown - Date.now());
    return diff.toUTCString().slice(17, 25); // HH:MM:SS
}
