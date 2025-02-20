async function uploadFiles() {
    const fileInput = document.getElementById('fileInput');
    const files = fileInput.files;
    const uploadButton = document.querySelector('.upload-section button');
    const responseText = document.getElementById('responseText');
    const uploadLoader = document.getElementById('uploadLoader');
    
    if (files.length === 0) {
        alert('Please select files to upload');
        return;
    }

    uploadButton.disabled = true;
    uploadButton.textContent = 'Uploading...';
    uploadLoader.classList.add('loading');

    const formData = new FormData();
    Array.from(files).forEach(file => {
        formData.append('files[]', file);
    });

    try {

        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        alert(result.message);
        
    } catch (error) {
        alert(`Upload failed: ${error.message}`);
    } finally {
        uploadButton.disabled = false;
        uploadButton.textContent = 'Upload to Vector Store';
        uploadLoader.classList.remove('loading');

    }
}

async function submitQuery() {
    const queryButton = document.getElementById('queryButton');
    const queryInput = document.getElementById('queryInput');
    const responseText = document.getElementById('responseText');
    const llmLoader = document.getElementById('llmLoader');

    if (!queryInput.value.trim()) {
        alert('Please enter a query');
        return;
    }

    queryButton.disabled = true;
    llmLoader.classList.add('loading');

    try {
        const response = await fetch('/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                query: queryInput.value
            })
        });
        const result = await response.json();
        // Convert markdown to HTML
        responseText.innerHTML = marked.parse(result.response);

    } catch (error) {
        alert(`Query Error: ${error.message}`);
    } finally {
        queryButton.disabled = false;
        llmLoader.classList.remove('loading');
    }
}

async function submitAsk() {
    const askButton = document.getElementById('askButton');
    const askInput = document.getElementById('askInput');
    const responseText = document.getElementById('responseText');
    const llmLoader = document.getElementById('llmLoader');

    if (!askInput.value.trim()) {
        alert('Please ask a question');
        return;
    }

    askButton.disabled = true;
    llmLoader.classList.add('loading');

    try {
        const response = await fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                query: askInput.value
            })
        });
        const result = await response.json();
        responseText.textContent = result.response;
    } catch (error) {
        alert(`Query Error: ${error.message}`);
    } finally {
        askButton.disabled = false;
        llmLoader.classList.remove('loading');
    }
}