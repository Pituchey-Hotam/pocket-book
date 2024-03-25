let fileLink = document.getElementById('file-link');

function downloadFile() {
    fileLink.click();
}

function checkFileFinished() {
    let finished_url = fileLink.getAttribute('aria-finished-url');
    
    fetch(finished_url).then(res => res.json()).then(result => {
        if (result.code == 0) {
            // File Finished
            clearInterval(checkFileFinishedInterval);
            downloadFile();
        } else if(result.code == 1) {
            // File doesn't Exists
            clearInterval(checkFileFinishedInterval);
        }
    });
}

let checkFileFinishedInterval = setInterval(checkFileFinished, 5000);