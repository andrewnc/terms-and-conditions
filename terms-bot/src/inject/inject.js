var words = new Set(['terms', 'service', 'legal', 'agreement']);

function getSummary() {
    chrome.runtime.sendMessage({
        tag: 'request',
        data: document.body.innerHTML,
        url: window.location.href
    }, function (response) {
        var readyStateCheckInterval = setInterval(function () {
            if (document.readyState === "complete") {
                clearInterval(readyStateCheckInterval);
            }
        }, 30);
    });
}

var info = {};
chrome.runtime.onMessage.addListener(
    function (request, sender, sendResponse) {
        if (request.tag === "from_background") {
            chrome.runtime.sendMessage({
                tag: 'for_popup',
                data: request.resp,
            }, function (response) {
                // Do nothing
            });
        } else if (request.tag === "from_popup") {
            getSummary();
        }
    });
