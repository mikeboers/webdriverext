
let VERBOSITY = 2
let LOCATION = 'back'

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


let connections = {}
let handlers = {}
var downloadFilename = null // must be var!
let tidCount = 0

function broadcast(msg) {
    msg.src = msg.src || LOCATION
    msg.dst = msg.dst || 'page'
    msg.tid = msg.tid || LOCATION[0] + tidCount++
    for (tab in connections) {
        let conn = connections[tab]
        if (conn != undefined) {
            conn.postMessage(msg)
        }
    }
}

chrome.runtime.onConnect.addListener(function (conn) {

    let tab_id = conn.sender.tab.id;
    connections[tab_id] = conn;

    debug(0, "conn to tab", tab_id, "opened")

    conn.onDisconnect.addListener(function() {
        debug(0, "conn to tab", tab_id, "closed")
        delete connections[tab_id];
    })

    conn.onMessage.addListener(function (msg) {

        debug(2, "recv:", msg)

        let func = handlers[msg.type]
        if (func) {
            try {
                func(conn, msg)
            } catch (error) {
                debug(0, "uncaught", error)
                reply(conn, msg, {error: error.toString()})
            }
        } else {
            debug(0, "unknown message type:", msg)
            reply(conn, msg, {error: "unknown message type"})
        }

    })

})



handlers.error = function(conn, msg) {
    throw "test error"
}

function getChrome(name) {
    let parts = name.split('.')
    let obj = chrome
    for (let i in parts) {
        obj = obj[parts[i]]
    }
    return obj
}

handlers.chrome = function(conn, msg) {
    let func = getChrome(msg.func)
    let args = msg.args.concat([function(result) {
        // Null is required because undefined gets filtered out.
        reply(conn, msg, {result: result || null})
    }])
    func.apply(null, args)
}

handlers.setDownloadFilename = function(conn, msg) {
    downloadFilename = msg.name
}

chrome.downloads.onDeterminingFilename.addListener(function (item, suggest) {
    debug(1, "downloads.onDeterminingFilename:", item, downloadFilename)
    if (downloadFilename) {
        suggest({filename: downloadFilename})
        downloadFilename = null
    } else {
        suggest()
    }
})

function broadcastChromeEvent(name) {
    let args = [function (data) {
        broadcast({
            type: 'event',
            event: 'chrome.' + name,
            data: data
        })
    }].concat(Array.prototype.slice.call(arguments, 1))
    console.log(args)
    let event = getChrome(name)
    event.addListener.apply(event, args)
}

broadcastChromeEvent('downloads.onCreated')
broadcastChromeEvent('downloads.onChanged')

broadcastChromeEvent(
    'webRequest.onHeadersReceived',
    {urls: ['https://*/*', 'http://*/*']}, // filters
    ['responseHeaders', 'extraHeaders']
)





