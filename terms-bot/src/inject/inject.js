// var words = new Set(['terms', 'service', 'legal', 'agreement']);

// change data if you want to have something else scraped
// var body_text = document.body.innerText;
// var text_list = body_text.split(" ");

// scraping moved to server
var body_text = window.location.hostname;
var send_data = true;

// for (var i = 0; i < text_list.length; i++) {
//     if (words.has(text_list[i].toLowerCase())) {
//         send_data = true;
//         break;
//     }
// }

// console.log(body_text);
// console.log(send_data);

// no longer need this check
if (send_data) {
    chrome.runtime.sendMessage({
        status: 'sending',
        data: body_text,
        url: window.location.hostname
    }, function (response) {
        var readyStateCheckInterval = setInterval(function () {
            if (document.readyState === "complete") {
                clearInterval(readyStateCheckInterval);
                // send info from this function call
            }
        }, 30);
    });


    // summary comes back here
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
}else{
    console.log("don't run");
}

