//example of using a message handler from the inject scripts
chrome.runtime.onMessage.addListener(
    function (request, sender, sendResponse) {
        chrome.pageAction.show(sender.tab.id);
        var xhr = new XMLHttpRequest();

        // this will change if we host somewhere
        // xhr.open("POST", 'http://127.0.0.1:5000/background.py', false);
        xhr.open("POST", 'http://legalleaf.pythonanywhere.com/background.py', false);

        //Send the proper header information along with the request
        xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhr.withCredentials = false;

        xhr.send(request.data);

        // xhr.rsponse contains the summary from background.py
        var summary = xhr.response;
        summary = summary.substr(1, summary.length - 2);

        // We can technically remove this, but we may want to try and get it working
        chrome.tabs.query({active: true, currentWindow: true}, function (tabs) {
            chrome.tabs.sendMessage(tabs[0].id, {tag: "from_background", resp: summary}, function (response) {
                // nothing
            });
        });
    });