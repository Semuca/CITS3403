function hash(str) {
    /**
     * COPIED DIRECTLY FROM https://stackoverflow.com/a/26057776
     * TODO (James): Possibly do hashing on the backend side- need to check with lecturer if it's allowed.
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
