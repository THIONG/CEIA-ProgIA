const imageInput = document.getElementById("imageInput");
const preview = document.getElementById("preview");
const canvas = document.getElementById("canvas");
const uploadButton = document.getElementById("uploadButton");
const results = document.getElementById("results");
const labelsTable = document.getElementById("labelsTable");

imageInput.addEventListener("change", function () {
    const file = this.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            preview.src = e.target.result;
            preview.style.display = "block";
            canvas.style.display = "none";
        };
        reader.readAsDataURL(file);
    }
});

uploadButton.addEventListener("click", async function () {
    const file = imageInput.files[0];
    if (!file) {
        alert("Por favor, selecciona una imagen.");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch("http://127.0.0.1:8000/upload/", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error("Error al procesar la imagen.");
        }

        const result = await response.json();
        const rekognitionData = result.rekognition_data;
        labelsTable.innerHTML = "";
        results.style.display = "block";

        rekognitionData.Labels.forEach(label => {
            const row = labelsTable.insertRow();
            row.insertCell(0).textContent = label.Name;
            row.insertCell(1).textContent = `${label.Confidence.toFixed(2)}%`;
        });

        if (rekognitionData.Labels.some(label => label.Instances.length > 0)) {
            drawBoundingBoxes(rekognitionData.Labels);
        }
    } catch (error) {
        alert("Error al subir la imagen.");
        console.error(error);
    }
});

function drawBoundingBoxes(labels) {
    const ctx = canvas.getContext("2d");

    // Ajustar tamaño del canvas al tamaño de la imagen
    const img = new Image();
    img.src = preview.src;
    img.onload = function () {
        canvas.width = img.width;
        canvas.height = img.height;
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 0, 0, img.width, img.height);

        // Oculta la imagen de preview y muestra el canvas
        preview.style.display = "none";
        canvas.style.display = "block";

        labels.forEach(label => {
            label.Instances.forEach(instance => {
                if (instance.BoundingBox) {
                    const box = instance.BoundingBox;
                    const x = box.Left * canvas.width;
                    const y = box.Top * canvas.height;
                    const width = box.Width * canvas.width;
                    const height = box.Height * canvas.height;

                    // Dibujar el rectángulo
                    ctx.strokeStyle = "red";
                    ctx.lineWidth = 2;
                    ctx.strokeRect(x, y, width, height);

                    // Dibujar el texto encima de la bounding box
                    const text = label.Name;
                    ctx.font = "bold 14px Arial";
                    ctx.fillStyle = "rgba(255, 0, 0, 0.7)"; // Fondo rojo semitransparente
                    ctx.fillRect(x, y - 20, ctx.measureText(text).width + 10, 20);
                    ctx.fillStyle = "white"; // Texto en blanco
                    ctx.fillText(text, x + 5, y - 5);
                }
            });
        });

        // Ajustar el tamaño del canvas dentro del contenedor
        canvas.style.maxWidth = "100%";
        canvas.style.maxHeight = "100%";
    };
}