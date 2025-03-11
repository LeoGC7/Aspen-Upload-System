const fileInput = document.getElementById('video');
        const fileDetails = document.getElementById('fileDetails');
        const fileName = document.getElementById('fileName');
        const fileSize = document.getElementById('fileSize');
        const uploadVideoButton = document.getElementById('uploadVideoButton');
        const progressBarContainer = document.getElementById('progressBarContainer');
        const progressBar = document.getElementById('progressBar');
        const progressPercentage = document.getElementById('progressPercentage');
        const progressText = document.getElementById('progressText');

        fileInput.addEventListener('change', (event) => {
            const file = event.target.files[0];
            if (file) {
                // Display file details
                fileName.textContent = file.name;
                fileSize.textContent = (file.size / (1024 * 1024)).toFixed(2); // Convert to MB
                fileDetails.classList.remove('hidden');
                uploadVideoButton.classList.remove('hidden'); // Show the "Upload Video" button
            } else {
                fileDetails.classList.add('hidden');
                uploadVideoButton.classList.add('hidden'); // Hide the "Upload Video" button
            }
        });

        document.getElementById('uploadForm').addEventListener('submit', function (e) {
            e.preventDefault();

            const file = fileInput.files[0];
            if (!file) return;

            const formData = new FormData();
            formData.append('video', file);

            const xhr = new XMLHttpRequest();

            // Show progress bar and spinner
            progressBarContainer.classList.remove('hidden');
            document.getElementById('spinner').classList.remove('hidden');

            xhr.upload.addEventListener('progress', (event) => {
                if (event.lengthComputable) {
                    const percentComplete = (event.loaded / event.total) * 100;
                    progressBar.style.width = `${percentComplete}%`;
                    progressPercentage.textContent = `${Math.round(percentComplete)}%`;
                }
            });

            xhr.addEventListener('load', () => {
                // Hide spinner and show completion message
                document.getElementById('spinner').classList.add('hidden');
                progressBar.style.backgroundColor = '#10B981'; // Green color
                progressText.classList.add('text-green-600');
                progressPercentage.textContent = 'Upload Complete!';
            });

            xhr.addEventListener('error', () => {
                // Handle error
                document.getElementById('spinner').classList.add('hidden');
                progressBar.style.backgroundColor = 'red'; // Red color
                progressText.classList.add('text-red-600');
                progressPercentage.textContent = 'Upload Failed!';
            });

            let actualUrl = window.location.href;
            xhr.open('POST', actualUrl, true);
            xhr.send(formData);
        });