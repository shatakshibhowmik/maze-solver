document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const mazeForm = document.getElementById('mazeForm');
    const fileInput = document.getElementById('mazeImage');
    const imagePreview = document.getElementById('imagePreview');
    const imagePreviewContainer = document.getElementById('imagePreviewContainer');
    const status = document.getElementById('status');
    const mazeGif = document.getElementById('mazeGif');
    const mazeGifContainer = document.getElementById('mazeGifContainer');
    const downloadButton = document.getElementById('downloadGifButton');

    // Hide elements initially
    imagePreviewContainer.style.display = 'none';
    mazeGifContainer.style.display = 'none';
    downloadButton.style.display = 'none';

    // File validation
    const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/gif', 'image/bmp'];
    const MAX_SIZE = 5 * 1024 * 1024; // 5MB

    function validateFile(file) {
        if (!file) {
            throw new Error('Please select a file');
        }
        if (!ALLOWED_TYPES.includes(file.type)) {
            throw new Error('Please upload an image file (JPEG, PNG, GIF, or BMP)');
        }
        if (file.size > MAX_SIZE) {
            throw new Error('File size must be less than 5MB');
        }
        return true;
    }

    // File input change handler
    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        
        try {
            if (validateFile(file)) {
                // Preview image
                const reader = new FileReader();
                reader.onload = function(e) {
                    imagePreview.src = e.target.result;
                    imagePreviewContainer.style.display = 'block';
                    status.textContent = 'Image loaded successfully. Click "Solve Maze" to begin.';
                    status.className = 'status-info';
                };
                reader.readAsDataURL(file);
            }
        } catch (error) {
            status.textContent = error.message;
            status.className = 'status-error';
            imagePreviewContainer.style.display = 'none';
        }
    });

    // Form submission
    mazeForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const file = fileInput.files[0];
        
        try {
            validateFile(file);
            
            // Update UI for processing
            status.textContent = 'Processing maze...';
            status.className = 'status-processing';
            mazeGifContainer.style.display = 'none';
            downloadButton.style.display = 'none';
            
            // Create loading spinner
            const spinner = document.createElement('div');
            spinner.className = 'loading-spinner';
            status.appendChild(spinner);

            // Prepare form data
            const formData = new FormData();
            formData.append('mazeImage', file);

            // Send request
            const response = await fetch('/solve_maze', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                // Update UI for success
                status.textContent = 'Maze solved successfully!';
                status.className = 'status-success';
                
                // Display solution
                mazeGif.src = data.gifUrl;
                mazeGifContainer.style.display = 'block';
                
                // Setup download button
                downloadButton.href = data.gifUrl;
                downloadButton.style.display = 'inline-block';
                
                // Add solution stats if available
                if (data.stats) {
                    const statsHtml = `
                        <div class="solution-stats">
                            <p>Path Length: ${data.stats.pathLength}</p>
                            <p>Cells Explored: ${data.stats.exploredCells}</p>
                            <p>Processing Time: ${data.stats.processingTime.toFixed(2)}s</p>
                        </div>
                    `;
                    status.insertAdjacentHTML('beforeend', statsHtml);
                }
            } else {
                throw new Error(data.error || 'Failed to solve maze');
            }
        } catch (error) {
            status.textContent = `Error: ${error.message}`;
            status.className = 'status-error';
            mazeGifContainer.style.display = 'none';
            downloadButton.style.display = 'none';
        } finally {
            // Remove loading spinner if it exists
            const spinner = status.querySelector('.loading-spinner');
            if (spinner) {
                spinner.remove();
            }
        }
    });

    // Add drag and drop support
    const dropZone = document.querySelector('.upload-section');

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, unhighlight, false);
    });

    function highlight(e) {
        dropZone.classList.add('highlight');
    }

    function unhighlight(e) {
        dropZone.classList.remove('highlight');
    }

    dropZone.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const file = dt.files[0];
        fileInput.files = dt.files;
        fileInput.dispatchEvent(new Event('change'));
    }
});
