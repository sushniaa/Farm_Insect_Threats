document.addEventListener("DOMContentLoaded", function () {
    const imageInput = document.getElementById("imageInput");
    const imageUploadForm = document.getElementById("imageUploadForm");

    imageInput.addEventListener("change", function () {
        const file = imageInput.files[0];
        if (file) {
            // Update the custom file label with the selected file name
            const fileName = file.name;
            const label = document.querySelector(".custom-file-label");
            label.textContent = fileName;
        }
    });

    imageUploadForm.addEventListener("submit", function (e) {
        e.preventDefault();

        const formData = new FormData(imageUploadForm);

        fetch("/submit", {
            method: "POST",
            body: formData,
        })
            .then((response) => response.json())
            .then((data) => {
                // Process the prediction result or update the UI as needed
                const resultLabel = document.getElementById("resultLabel");
                const resultInsecticides = document.getElementById("resultInsecticides");
                resultLabel.textContent = `Predicted Label: ${data.label}`;
                resultInsecticides.textContent = `Recommended Insecticides: ${data.insecticides_label}`;
            
                const resultImage = document.getElementById("resultImage");
                resultImage.src = data.image_path;
                console.log(data);
            })
            .catch((error) => {
                console.error(error);
            });
    });
});

