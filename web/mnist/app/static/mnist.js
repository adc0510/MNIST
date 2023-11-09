// draw.js
const canvas = document.getElementById('drawingCanvas');
const context = canvas.getContext('2d');

let drawing = false;

canvas.addEventListener('mousedown', (event) => {
    context.fillStyle = 'white';
    context.fillRect(0, 0, canvas.width, canvas.height);
    drawing = true;
    context.lineWidth = 50;
    context.lineCap = 'round';
    context.strokeStyle = 'black';
    context.beginPath();
    context.moveTo(event.clientX - canvas.offsetLeft, event.clientY - canvas.offsetTop);
});

canvas.addEventListener('mousemove', (event) => {
    if (!drawing) return;
    context.lineTo(event.clientX - canvas.offsetLeft, event.clientY - canvas.offsetTop);
    context.stroke();
});

canvas.addEventListener('mouseup', () => {
    drawing = false;
    context.closePath();
});

canvas.addEventListener('mouseleave', () => {
    drawing = false;
    context.closePath();

    const img = canvas.toDataURL();
    save(img);

});

function save (img) {
    // JavaScript code
    const dataToSend = {
    data: img,
    };
    // console.log(encodeURIComponent(JSON.stringify(dataToSend)));
    fetch('test/save_drawing/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken'), // Include the CSRF token for security
        },
        body: `data=${(JSON.stringify(dataToSend))}`,
    })
    .then(response => {
        if (response.ok) {
            return response.json(); // If you want a response from the server
        } else {
            throw new Error('Failed to send data to Django.');
        }
    })
    .then(data => {
        // Handle the response from the server, if needed
        document.getElementById('pred').textContent = 'Guest Number:' + data.message;
        console.log(data.message);
    })
    .catch(error => {
        // Handle errors, e.g., display an error message
        console.error(error);
    });

}

const clearButton = document.getElementById('clear');

clearButton.addEventListener('click', () => {
    // Clear the entire canvas
    context.clearRect(0, 0, canvas.width, canvas.height);
    document.getElementById('pred').textContent = 'Guest Number:';
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if this cookie name matches the one you're looking for (e.g., 'csrftoken')
            if (cookie.substring(0, name.length + 1) === name + '=') {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

