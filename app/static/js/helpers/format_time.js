export function dateFromPythonTime(time) {
    return new Date(time).toDateString().split(" ").slice(0, 3).join(" ");
}

export function timeFromPythonTime(time) {
    return new Date(time).toTimeString().split(" ").at(0);
}