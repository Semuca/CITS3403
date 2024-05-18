const CryptoJS = window.CryptoJS;

export const hash = function(text) {
    return CryptoJS.SHA256(text).toString(CryptoJS.enc.Hex);
}