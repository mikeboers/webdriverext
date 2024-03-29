
WebDriverExt = {};

(function(M) { // scope wrapper


M.VERBOSITY = 2
let LOCATION = 'page'

function debug(level) {
    if (level <= M.VERBOSITY) {
        arguments[0] = '[webdriverext/' + LOCATION + ']'
        console.log.apply(null, arguments)
    }
}
debug(0, "init")

// === end common


function reply(src, msg) {
    msg.src = LOCATION
    msg.dst = msg.dst || src.src
    msg.tid = msg.tid || src.tid
    msg.type = msg.type || src.type
    debug(2, "reply", msg)
    WebDriverExt.post(msg)
}


M.messageHandlers = {}
M.eventHandlers = {}
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

    let func = M.messageHandlers[msg.type]
    if (func) {
        func(msg)
        return
    }

    debug(0, "unhandled message:", msg)
    
}, false)


M.messageHandlers.event = function(msg) {
    let func = M.eventHandlers[msg.event]
    if (func) {
        func(msg.data)
        return
    }
    debug(0, "unhandled event:", msg)
}

M.eventHandlers['chrome.webRequest.onHeadersReceived'] = function(msg) {
    console.log(msg)
}


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

M.chrome = function(func) {
    let args = Array.prototype.slice.call(arguments, 1, -1)
    let callback = arguments[arguments.length - 1]
    M.post({
        type: 'chrome',
        func: func,
        args: args
    }, callback)
}

M.chromeBatch = function(batch, callback) {
    var results = []
    let onResult = function(i, data) {
        results[i] = data
        if (results.length == batch.length) {
            callback(results)
        }
    }
    for (let i in batch) {
        let args = batch[i].concat([onResult.bind(null, i)])
        M.chrome.apply(null, args)
    }
}

M.setDownloadFilename = function(filename) {
    M.post({
        type: 'setDownloadFilename',
        filename: filename
    })
}

M.captureRequests = function(pattern) {
    M.post({
        type: 'captureRequests'
    })
}



})(WebDriverExt)
