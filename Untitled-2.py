html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Face Detection Web Page</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin-top: 40px;
        }
        video, canvas {
            border: 2px solid #333;
            margin: 10px;
        }
    </style>
</head>
<body>
    <h1>Face Detection Web Page</h1>
    <p>This page shows your webcam feed. For real face detection, use Python and OpenCV.</p>
    <video id="video" width="480" height="360" autoplay></video>
    <script>
        // Access the webcam and stream to the video element
        const video = document.getElementById('video');
        if (navigator.mediaDevices.getUserMedia) {
            navigator.mediaDevices.getUserMedia({ video: true })
                .then(function(stream) {
                    video.srcObject = stream;
                })
                .catch(function(err) {
                    alert("Error accessing webcam: " + err);
                });
        }
    </script>
</body>
</html>
"""

with open("face_detection_webpage.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Web page generated as face_detection_webpage.html")