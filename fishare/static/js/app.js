async function uploadFile() {
    let uploadForm = document.querySelector('#upload-form');
    let infoBox = document.querySelector('#info-box');

    let file = uploadForm.querySelector("input").files[0];
    if (file === undefined) {
        return;
    }

    // prepare for post
    let formData = new FormData();
    formData.append("payload", file);

    // POST data
    const response = await fetch('/api/v1/files/', {method: "POST", body: formData});

    uploadForm.style.display = 'none';

    // if created/uploaded
    if (response.status == 201) {
        // get the data
        const data = await response.json();

        // prepare link for download
        let link = document.createElement('a');
        link.href = data.url;
        link.text = data.url;

        // show the infobox
        infoBox.querySelector('.url').append(link);
        infoBox.style.display = 'block';
    } else {
        console.error('>> kurnik sopa');
    }
}


window.onload = function () {
    document.querySelector('#upload-form > button').addEventListener('click', uploadFile);
}
