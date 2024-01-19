// content.js
chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        if (request.action === "predict") {
            const text = document.getElementById('sms-text').value;
            fetch('http://localhost:5000/predict_json', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({sms: text}),
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('prediction').innerText = data.prediction;
                document.getElementById('confidence').innerText = data.confidence + '%';
            });
        }
    }
);
