// script.js file

function domReady(fn) {
	if (
		document.readyState === "complete" ||
		document.readyState === "interactive"
	) {
		setTimeout(fn, 1000);
	} else {
		document.addEventListener("DOMContentLoaded", fn);
	}
}

domReady(function () {

	// If found your qr code
	function onScanSuccess(decodeText, decodeResult) {
		alert("Your QR is : " + decodeText, decodeResult);
		// insert code here to invoke API Gateway
		// if legitimate site, change background to green
		// if phishing site, change background to red
        checkSite(decodeText)
            .then(isLegitimate => {
                if (isLegitimate) {
                    document.body.style.backgroundColor = "green";
                } else {
                    document.body.style.backgroundColor = "red";
                }
            })
            .catch(error => {
                console.error("Error checking site:", error);
                alert("Error checking site. Please try again.");
            });		
	}

	let htmlscanner = new Html5QrcodeScanner(
		"my-qr-reader",
		{ fps: 10, qrbos: 250 }
	);
	htmlscanner.render(onScanSuccess);
});

async function checkSite(url) {
    // Replace 'YOUR_API_GATEWAY_URL' with actual API Gateway URL
    const apiGatewayUrl = 'YOUR_API_GATEWAY_URL';
    
    const response = await fetch(apiGatewayUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: url })
    });

    if (!response.ok) {
        throw new Error('Network response was not ok');
    }

    const data = await response.json();
    return data === 1; // API returns 1 for legitimate, 0 for phishing
}