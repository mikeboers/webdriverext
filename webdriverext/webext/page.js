
var VERBOSITY = 1
var LOCATION = 'page'

function debug(level) {
    if (level <= VERBOSITY) {
        arguments[0] = '[webdriverext/' + LOCATION + ']'
        console.log.apply(null, arguments)
    }
}
debug(0, "init")

function reply(src, msg) {
    msg.src = LOCATION
    msg.dst = msg.dst || src.src
    msg.tid = msg.tid || src.tid
    msg.type = msg.type || src.type
    debug(2, "reply", msg)
    WebDriverExt.post(msg)
}

// === end common ===

WebDriverExt = {};

(function(M) { // scope wrapper

M.handlers = {}
M.callbacks = {}
M.tidCounter = 0

window.addEventListener('message', function(e) {

    if (e.source != window) return // Must be from this window (i.e. main.js or page.js).
    if (!e.data.webdriverext) return // Must be webdriverext.
    if (e.data.webdriverext.dst != LOCATION) return // Must be addressed to us.

    let msg = e.data.webdriverext
    debug(2, "recv:", msg)

    let callback = M.callbacks[msg.tid]
    if (callback) {
        if (--callback.ttl <= 0) {
            delete M.callbacks[msg.tid]
        }
        callback.func(msg)
        return
    }

    let func = M.handlers[msg.type]
    if (func) {
        func(msg)
        return
    }

    debug(0, "unknown message type:", msg)
    
}, false)


M.handlers.downloadCreated = function(msg) {}
M.handlers.downloadChanged = function(msg) {}

M.post = function(msg, callback, callbackCount) {

    msg.src = msg.src || LOCATION
    msg.dst = msg.dst || 'back'
    msg.tid = msg.tid || LOCATION[0] + M.tidCounter++
    debug(2, "send:", msg)

    if (callback) {
        M.callbacks[msg.tid] = {
            func: callback,
            ttl: callbackCount || 1
        }
    }

    window.postMessage({webdriverext: msg}, '*')
    return msg.tid

}

M.getCookies = function(url, callback) {
    M.post({
        type: 'cookies',
        url: url == undefined ? window.location.href : url
    }, callback ? (msg) => callback(msg.cookies) : null)
}

M.download = function(options, callback) {
    M.post({
        type: 'download',
        options: options
    }, callback ? (msg) => callback(msg.id) : null)
}

M.getDownloads = function(query, callback) {
    M.post({
        type: 'getDownloads',
        query: query
    }, callback ? (msg) => callback(msg.downloads) : null)
}

M.setDownloadFilename = function(filename) {
    M.post({
        type: 'setDownloadFilename',
        filename: filename
    })
}


})(WebDriverExt)
