let browseWindow = null;
let photosDir = '';

document.addEventListener('DOMContentLoaded', function() {
    // Get the photos directory from the hidden input
    photosDir = document.getElementById('photos-dir').value;
    
    // Initialize controls
    initControls();
    
    // Initialize window message handler
    initWindowMessaging();
});

function initControls() {
    // Movement controls
    document.getElementById('up').addEventListener('click', () => sendCommand('up'));
    document.getElementById('down').addEventListener('click', () => sendCommand('down'));
    document.getElementById('left').addEventListener('click', () => sendCommand('left'));
    document.getElementById('right').addEventListener('click', () => sendCommand('right'));
    document.getElementById('center').addEventListener('click', () => sendCommand('center'));

    // Keyboard controls
    document.addEventListener('keydown', (e) => {
        switch(e.key) {
            case 'ArrowUp': sendCommand('up'); break;
            case 'ArrowDown': sendCommand('down'); break;
            case 'ArrowLeft': sendCommand('left'); break;
            case 'ArrowRight': sendCommand('right'); break;
        }
    });

    // Button events
    document.getElementById('capture').addEventListener('click', capturePhoto);
    document.getElementById('browse').addEventListener('click', browsePhotos);
}

function sendCommand(direction) {
    fetch('/control', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ direction: direction })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('pan-value').textContent = data.pan;
        document.getElementById('tilt-value').textContent = data.tilt;
    })
    .catch(error => console.error('Error:', error));
}

async function capturePhoto() {
    try {
        const response = await fetch('/capture', { method: 'POST' });
        const result = await response.json();
        if (result.status === 'success') {
            showPhotoPreview(result.url);
        } else {
            alert('Error: ' + result.message);
        }
    } catch (error) {
        alert('Failed to capture photo');
        console.error('Capture error:', error);
    }
}

function showPhotoPreview(imageUrl) {
    const preview = window.open('', '_blank');
    preview.document.write(`
        <!DOCTYPE html>
        <html>
        <head>
            <title>Photo Preview</title>
            <link rel="stylesheet" href="/static/css/preview.css">
        </head>
        <body>
            <button id="close-viewer" onclick="window.close()">×</button>
            <img id="viewer-image" src="${imageUrl}" alt="Captured photo">
            <script src="/static/js/preview.js"></script>
        </body>
        </html>
    `);
}

function browsePhotos() {
    const browseUrl = '/browse?directory=' + encodeURIComponent(photosDir);
    if (browseWindow && !browseWindow.closed) {
        browseWindow.location.href = browseUrl;
        browseWindow.focus();
    } else {
        browseWindow = window.open(browseUrl, 'photoBrowserWindow');
    }
}

function initWindowMessaging() {
    window.addEventListener('message', function(event) {
        if (event.data && event.data.type === 'browseWindowClosed') {
            browseWindow = null;
        }
    });
}