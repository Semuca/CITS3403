function hash(str) {
    /**
     * COPIED DIRECTLY FROM https://stackoverflow.com/a/26057776
     * TODO (Jared): Maybe we should rewrite this ourselves? not sure...
     */
    let hash = 0;
    if (str.length === 0) return hash;
    for (let i = 0; i < str.length; i++) {
        const char = str.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash; // Convert to 32bit integer
    }
    return hash;
}


jQuery(() => {
    //FUTURE (Jared): Remove this button since it's just for testing
    $("#tokenChecker").click(() => {
        if (document.cookie.includes("token")) {
            const token = document.cookie.split("token=")[1].split(";")[0]
            alert("your token is " + token + ". Probably don't share that!!")
        } else {
            alert("You aren't logged in!")
        }
    })
    $("#pressLogin").click(() => {
        let body = JSON.stringify({
                username: $("#username").val(),
                password: (hash($("#password").val())).toString()
            }
        )
        fetch("/api/login", {
            method: "POST", body: body, headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        }).then(r => {
            if (r.ok) {
                r.json().then(
                    o => {
                        const expiry = new Date(Date.now() + (25 * 60 * 60)) //set the cookie to expire in 24 hours
                        document.cookie += `token=${o.token}; expiry=${expiry}; path=/`
                        document.location = "/"
                    }
                )
            } else {
                alert(`The server did not return a valid response! HTTP error code is ${r.status} (${r.statusText})`)
            }
        })

    })

    $("#pressCreate").click(() => {
        fetch("/api/users", {
            method: "POST", body: JSON.stringify({
                username: $("#username").val(),
                password: hash($("#password").val()).toString()
            }), headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        }).then(r => {
            if (r.ok) {
                console.log(r);
                r.json().then(
                    o => {
                        const expiry = new Date(Date.now() + (25 * 60 * 60)) //set the cookie to expire in 24 hours
                        document.cookie += `token=${o.token}; expiry=${expiry}; path=/`
                        document.location = "/"
                    }
                )
            } else {
                alert(`The server did not return a valid response! HTTP error code is ${r.status} (${r.statusText})`)
            }
        })

    })
})
