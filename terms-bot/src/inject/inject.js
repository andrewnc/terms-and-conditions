
// change data if you want to have something else scraped
chrome.runtime.sendMessage({status: 'sending', data:document.body.innerText, url: window.location.hostname}, function(response) {
	var readyStateCheckInterval = setInterval(function() {
	if (document.readyState === "complete") {
		clearInterval(readyStateCheckInterval);
		// send info from this function call
		console.log('sending');
		console.log(document.body.innerText)
	}
	}, 30);
});


// summary comes back here
chrome.runtime.onMessage.addListener(
	function(request, sender, sendResponse) {
		var info = {
			data: request.resp
		}
		sendResponse(info)
		console.log(request.resp);
});