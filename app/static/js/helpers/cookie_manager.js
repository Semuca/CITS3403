export class CookieManager {
    static getCookie(name) {
        return document.cookie.split("; ").find((row) => row.startsWith(`${name}=`))?.split("=")[1];
    }

    static setCookie(name, value) {
        const expiry = new Date(Date.now() + (25 * 60 * 60));
        document.cookie = `${name}=${value}; expiry=${expiry} Secure`;
    }
}