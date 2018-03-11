var PROTOCOL = "http://";
var DEFAULT_IP = "legalleaf.pythonanywhere.com";
var DEFAULT_PORT = "5000";
var DEFAULT_PATH = "/background.py";

var PROTOCOL = "https://"
var DEFAULT_PATH = "/webapi/summarize";

function sendRequest(ip, port, path, data) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", PROTOCOL + ip + ":" + port + path, false);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.withCredentials = false;
    console.log(data);
    xhr.send(data);

    // xhr.rsponse contains the summary from background.py
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
        chrome.pageAction.show(sender.tab.id);
        // Get the server based on storage
        chrome.storage.sync.get({
            developerMode: false,
            serverIp: "",
            port: ""
        }, function (items) {
            if (items.developerMode === false)
                sendRequest(DEFAULT_IP, DEFAULT_PORT, DEFAULT_PATH,request.data);
            else
                sendRequest(items.serverIp, items.port, DEFAULT_PATH, request.data);
        });
    });
