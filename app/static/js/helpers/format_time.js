export function dateFromPythonTime(time) {
    return time.split(" 202")[0]
}

export function timeFromPythonTime(time) {
    return time.split(" 202")[1].substring(1).split(" GMT")[0]
}