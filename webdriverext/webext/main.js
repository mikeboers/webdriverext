
let VERBOSITY = 1
let LOCATION = 'main'

function debug(level) {
    if (level <= VERBOSITY) {
        arguments[0] = '[webdriverext/' + LOCATION + ']'
        console.log.apply(null, arguments)
    }
}
debug(0, "init")

function reply(conn, src, msg) {
    msg.src = LOCATION
    msg.dst = msg.dst || src.src
    msg.tid = msg.tid || src.tid
    msg.type = msg.type || src.type
    debug(2, "reply", msg)
    conn.postMessage(msg)
}

// === end common

let handlers = {}
let port = chrome.runtime.connect()



let routeMessage = function(msg) {

    debug(2, "recv:", msg)
    
    if (msg.dst == 'page') {
        window.postMessage({webdriverext: msg, via_main: true}, '*');

    } else if (msg.dst == 'back') {
        port.postMessage(msg)

    } else if (msg.dst == 'main') {
        let func = handlers[msg.type]
        if (func) {
            func(msg)
        } else {
            debug(0, "unknown message type:", msg)
        }

    } else {
        debug(0, "cannot route message:", msg)
    }

}


port.onMessage.addListener(routeMessage)

window.addEventListener("message", function(e) {
    if (e.source != window) return   // Must be from this page.
    if (!e.data.webdriverext) return // Must be webdriverext.
    if (e.data.via_main) return      // Must not be from us.
    routeMessage(e.data.webdriverext)
})




function getPageURL(url) {
    return chrome.extension.getURL(url)
}

function injectJS(url) {
    let script = document.createElement("script");
    script.type = "text/javascript";
    script.src = url
    document.head.appendChild(script);
}

injectJS(getPageURL("page.js")); // Depends on UI.
