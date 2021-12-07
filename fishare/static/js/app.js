window.onload = function () {
    // set visibility
    let uploadForm = document.querySelector('#upload-form');
    uploadForm.style.display = 'flex';
    let infoBox = document.querySelector('#info-box');
    infoBox.style.display = 'none';

    uploadForm.querySelector('button').addEventListener('click', function () {
        let file = uploadForm.querySelector("input").files[0];
        if (file === undefined) {
            return;
        }

        // prepare for post
        let formData = new FormData();
        formData.append("payload", file);

        // POST data
        fetch('/api/v1/files/', {method: "POST", body: formData})
            .then(response => response.json())
            .then(function (data) {
                console.log(data);
                uploadForm.style.display = 'none';

                // check if status ic created/201
                if(data.status == 201) {
                    infoBox.style.display = 'block';

                    let link = document.createElement('a');
                    link.href = `/${data.slug}`;
                    link.text = `http://localhost/${data.slug}`;

                    infoBox.querySelector('.url').append(link);
                }else if(data.status === 404){
                    console.log('kurnik');
                }
            });
    });
}