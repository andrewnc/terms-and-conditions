var body_text = window.location.hostname;
chrome.runtime.sendMessage({
    status: 'sending',
    data: body_text,
    url: window.location.hostname
}, function (response) {
    var readyStateCheckInterval = setInterval(function () {
        if (document.readyState === "complete") {
            clearInterval(readyStateCheckInterval);
        }
    }, 30);
});

var info = {};
chrome.runtime.onMessage.addListener(
    function (request, sender, sendResponse) {
        if (request.tag === "from_background") {
            info = {
                data: request.resp
            };
            sendResponse(info);
        } else if (request.tag === "from_popup") {
            sendResponse(info);
        }
    });
