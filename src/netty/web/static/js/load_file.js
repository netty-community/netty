// Immediately define loadFile function
window.loadFile = async function(file) {
    const fileContent = document.getElementById('file-content');
    if (!fileContent) {
        console.error('File content container not found!');
        return false;
    }

    // Update URL without reloading
    const newUrl = window.location.pathname + `?file=${encodeURIComponent(file)}`;
    window.history.pushState({file: file}, '', newUrl);

    // Update active state
    const fileLinks = document.querySelectorAll('a[data-file]');
    fileLinks.forEach(l => l.classList.remove('active'));
    const activeLink = document.querySelector(`[data-file="${file}"]`);
    if (activeLink) {
        activeLink.classList.add('active');
    }

    // Update header
    const cardTitle = document.querySelector('.card-title');
    if (cardTitle) {
        cardTitle.textContent = file;
    }

    // Show loading state
    fileContent.innerHTML = `<div class="d-flex justify-content-center">
        <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
    </div>`;

    try {
        const response = await fetch(`${window.location.pathname}/file?file_path=${encodeURIComponent(file)}`);
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
        }
        const data = await response.json();
        console.log('Received data:', data);

        // Helper function to escape HTML
        const escapeHtml = (unsafe) => {
            return unsafe
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/"/g, "&quot;")
                .replace(/'/g, "&#039;");
        };

        // Update content based on file type
        if (data.type === 'yaml') {
            fileContent.innerHTML = `<pre><code class="language-yaml">${escapeHtml(data.content)}</code></pre>`;
        } else if (data.type === 'excel') {
            fileContent.innerHTML = `<div class="alert alert-info">
                <div class="d-flex">
                    <div>
                        <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-file-spreadsheet alert-icon" width="16" height="16" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                            <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                            <path d="M14 3v4a1 1 0 0 0 1 1h4" />
                            <path d="M17 21h-10a2 2 0 0 1 -2 -2v-14a2 2 0 0 1 2 -2h7l5 5v11a2 2 0 0 1 -2 2z" />
                            <path d="M8 11h8v7h-8z" />
                            <path d="M8 15h8" />
                            <path d="M11 11v7" />
                        </svg>
                    </div>
                    <div class="ms-2">${escapeHtml(data.content)}</div>
                </div>
            </div>`;
        } else {
            fileContent.innerHTML = `<pre><code>${escapeHtml(data.content)}</code></pre>`;
        }
    } catch (error) {
        console.error('Error loading file:', error);
        fileContent.innerHTML = `<div class="alert alert-danger">
            <div class="d-flex">
                <div>
                    <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-alert-circle alert-icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                        <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                        <path d="M12 12m-9 0a9 9 0 1 0 18 0a9 9 0 1 0 -18 0" />
                        <path d="M12 8l0 4" />
                        <path d="M12 16l.01 0" />
                    </svg>
                </div>
                <div class="ms-2">Error loading file content: ${escapeHtml(error.message)}</div>
            </div>
        </div>`;
    }
    return false; // Prevent default link behavior
};
