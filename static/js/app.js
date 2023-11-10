const express = require('express');
const app = express();

// Middleware for serving static files (e.g., CSS, images)
app.use(express.static('public'));

// Define a route to handle both GET and POST requests to "/submit".
app.route('/submit')
  .get((req, res) => {
    // Handle GET request (if needed).
    res.send('This is the GET request handler for /submit');
  })
  .post((req, res) => {
    // Handle POST request to upload and process the file.
    // You can access the uploaded file using req.body.images.
    // Process the image and send the prediction result back.
    // Replace the following lines with your prediction logic.

    const prediction = {
      label: 'Insect',
      image_path: '/path-to-predicted-image.jpg',
    };

    res.json(prediction);
  });

app.listen(3000, () => {
  console.log('Server is running on http://localhost:3000');
});
