const video = document.getElementById('cameraFeed');
const canvas = document.getElementById('canvas');
const context = canvas.getContext('2d');
// 1. Accéder à la caméra
navigator.mediaDevices.getUserMedia({ video: true })
    .then((stream) => {
        video.srcObject = stream;
    })
    .catch((error) => {
        console.error('Erreur d\'accès à la caméra :', error);
    });

// 2. Fonction pour capturer et envoyer l'image
function captureAndSend() {
    // Dessiner l'image courante de la vidéo sur le canvas
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
            document.getElementById('result').textContent = 
                `Prédiction : ${data.object} (${(data.confidence * 100).toFixed(2)}%)`;
        })
        .catch(error => console.error('Erreur lors de l\'envoi à l\'API :', error));
    }, 'image/jpeg');
}

// Assurez-vous d'appeler captureAndSend() quand l'utilisateur clique sur un bouton.
// Par exemple : document.getElementById('captureButton').addEventListener('click', captureAndSend);