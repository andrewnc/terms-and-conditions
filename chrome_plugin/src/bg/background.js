var PROTOCOL = "https://";
var DEFAULT_IP = "legal-leaf.appspot.com";
var DEFAULT_PORT = "443";
var DEFAULT_PATH = "/webapi/summarize";


function sendRequest(protocol, ip, port, path, req) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", protocol + ip + ":" + port + path, false);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.setRequestHeader("target_url", req.url);
    xhr.withCredentials = false;
    xhr.send(req.data);

    var summary = xhr.response;
    summary = summary.substr(1, summary.length - 2);

    chrome.tabs.query({active: true, currentWindow: true}, function (tabs) {
        chrome.tabs.sendMessage(tabs[0].id, {tag: "from_background", resp: summary}, function (response) {
            // nothing
        });
    });
}

chrome.runtime.onMessage.addListener(
    function (request, sender, sendResponse) {
        if (request.tag === "request") {
            chrome.storage.sync.get({
                developerMode: false,
                protocol: "",
                serverIp: "",
                port: "",
                path: ""
            }, function (items) {
                if (items.developerMode === false)
                    sendRequest(PROTOCOL, DEFAULT_IP, DEFAULT_PORT, DEFAULT_PATH, request);
                else
                    sendRequest(items.protocol, items.serverIp, items.port, items.path, request);
            });
        }
    });
