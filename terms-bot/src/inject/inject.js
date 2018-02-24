
// change data if you want to have something else scraped
chrome.runtime.sendMessage({status: 'sending', data:document.body.innerText, url: window.location.hostname}, function(response) {
	var readyStateCheckInterval = setInterval(function() {
	if (document.readyState === "complete") {
		clearInterval(readyStateCheckInterval);
		// send info from this function call
		console.log('sending');
	}
	}, 30);
});


// summary comes back here
chrome.runtime.onMessage.addListener(
	function(request, sender, sendResponse) {
		var info = {
			data: request.resp
		}

		// here we log the response, if they want it
		console.log(request.resp);
});