
// change data if you want to have something else scraped
chrome.runtime.sendMessage({status: 'sending', data:document.body.innerText}, function(response) {
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
		// sendResponse(request.resp); // this is sending to the wrong page
		// theParent = document.body;
		// theKid = document.createElement("div");
		// theKid.innerHTML =  request.resp

		// // append theKid to the end of theParent
		// // theParent.appendChild(theKid);

		// // prepend theKid to the beginning of theParent
		// theParent.insertBefore(theKid, theParent.firstChild);
		sendResponse(info)
		console.log(request.resp);
});