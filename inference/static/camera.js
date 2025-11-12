const video = document.getElementById('camera');
const canvas = document.getElementById('canvas');
const context = canvas.getContext('2d');
let resultat =  document.getElementById('result')
navigator.mediaDevices.getUserMedia({ video: true })
    .then((stream) => {
        video.srcObject = stream;
    })
    .catch((error) => {
        console.error('Erreur d\'accès à la caméra :', error);
    });

function captureAndSend() {
    context.drawImage(video, 0, 0, 224, 224); 
    
    // Convertir le canvas en un objet Blob (fichier binaire)
    canvas.toBlob((blob) => {
        const formData = new FormData();
        formData.append('file', blob, 'capture.jpg'); // Le nom 'file' doit correspondre à 'request.files['file']' dans Flask

        // 3. Envoyer le fichier à l'API Flask
        fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            htmlContent = ""
            const predictionList = data.predictions;
            predictionList.forEach((prediction, index) => {
                htmlContent += `<p>${index + 1} : ${prediction.label} (${prediction.probabilite})</p>`;
            });
            resultat.innerHTML = htmlContent
            console.log(data)
        })
        .catch(error => console.error('Erreur lors de l\'envoi à l\'API :', error));
    }, 'image/jpeg');
}

document.getElementById('captureButton').addEventListener('click', captureAndSend);

