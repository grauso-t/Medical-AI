document.addEventListener("DOMContentLoaded", function () {
    const jqueryScript = document.createElement('script');
    jqueryScript.src = 'https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.1/jquery.min.js';
    jqueryScript.onload = function () {
        $(".chat-button").click(function () {
            $(".chat-container").slideDown();
            $(".chat-button").hide();
        });

        $(".close-button").click(function () {
            $(".chat-container").slideUp();
            $(".chat-button").show();
        });
    };
    document.head.appendChild(jqueryScript);

    const chartScript = document.createElement('script');
    chartScript.src = 'https://cdn.jsdelivr.net/npm/chart.js';
    document.head.appendChild(chartScript);

    const inputField = document.querySelector(".input-field");
    const chatBody = document.querySelector(".chat-body");

    function addMessage(sender, message) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add(`${sender}-message`);
        messageDiv.innerHTML = `<div class="message">${message}</div>`;
        chatBody.appendChild(messageDiv);

        chatBody.scrollTop = chatBody.scrollHeight;
        return messageDiv;
    }

    function createChart(dates, values) {
        const chartContainer = document.createElement("div");
        chartContainer.className = "chart-container";

        const canvas = document.createElement("canvas");
        canvas.id = "myChart";

        chartContainer.appendChild(canvas);
        chatBody.appendChild(chartContainer);

        const ctx = canvas.getContext("2d");

        const numericValues = values.map(value => parseFloat(value));

        const units = values.map(value => {
            const match = value.match(/[a-zA-Z]+$/);
            return match ? match[0] : '';
        });

        new Chart(ctx, {
            type: "line",
            data: {
                labels: dates,
                datasets: [
                    {
                        label: units[0],
                        data: numericValues,
                        borderColor: "blue",
                        fill: false,
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        ticks: {
                            callback: function (value) {
                                return value + " " + units[0];
                            },
                        },
                    },
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    zoom: {
                        zoom: {
                            wheel: {
                                enabled: true,
                            },
                            pinch: {
                                enabled: true,
                            },
                            mode: 'x',
                        },
                    },
                },
            },
        });

        chatBody.scrollTop = chatBody.scrollHeight;
    }

    function addLoadingMessage() {
        const loadingDiv = document.createElement("div");
        loadingDiv.classList.add("bot-message", "loading-message");
        loadingDiv.innerHTML = '<div class="loader-dot"></div>';
        chatBody.appendChild(loadingDiv);
        disableInputAndButton();

        chatBody.scrollTop = chatBody.scrollHeight;
    }

    function removeLoadingMessage() {
        const loadingMessage = document.querySelector(".loading-message");
        if (loadingMessage) {
            loadingMessage.remove();
            enableInputAndButton();
        }
    }

    function disableInputAndButton() {
        inputField.disabled = true;
        document.querySelector(".input-button").disabled = true;
    }

    function enableInputAndButton() {
        inputField.disabled = false;
        document.querySelector(".input-button").disabled = false;
    }

    function sendMessageToServer(message) {
        addLoadingMessage();

        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user_message: message }),
        })
            .then(response => response.json())
            .then(data => {
                if (data.hasOwnProperty('error')) {
                    addMessage('bot', `Error: ${data.error}`);
                    removeLoadingMessage();
                } else {
                    const botResponse = data.bot_message;
                    if (botResponse === "graph") {
                        if (data.hasOwnProperty('dates') && data.hasOwnProperty('values')) {
                            createChart(data.dates, data.values);
                            removeLoadingMessage();
                        } else {
                            addMessage('bot', 'Graph data is missing.');
                            removeLoadingMessage();
                        }
                    }
                    else if (botResponse === "stream") {
                        startStreaming(data.data);
                    }
                    else {
                        removeLoadingMessage();
                        addMessage('bot', botResponse);
                    }
                }
            })
            .catch(error => {
                console.error('Error sending message:', error);
                removeLoadingMessage();
                addMessage('bot', 'An error occurred while communicating with the server.');
            });
    }

    document.querySelector(".input-button").addEventListener("click", function () {
        const userMessage = inputField.value;
        if (userMessage.trim() !== "") {
            addMessage('user', userMessage);
            sendMessageToServer(userMessage);
            inputField.value = "";
        }
    });

    inputField.addEventListener("keyup", function (event) {
        if (event.key === "Enter") {
            const userMessage = inputField.value;
            if (userMessage.trim() !== "") {
                addMessage('user', userMessage);
                sendMessageToServer(userMessage);
                inputField.value = "";
            }
        }
    });

    function startStreaming(data) {

        // Send POST request to Flask endpoint with data
        fetch('/stream', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json' // Specify content type as JSON
            },
            body: JSON.stringify({ data: data }), // Include data in the request body
        })
        .then(response => {
            removeLoadingMessage();
            disableInputAndButton();
            text = "";
            message = addMessage("bot", "");
            // ReadableStream to consume data
            const reader = response.body.getReader();
            // Function to continuously read data
            function read() {
                reader.read().then(({ done, value }) => {
                    // If stream ends, exit
                    if (done) {
                        enableInputAndButton();
                        return;
                    }
                    // Append data to container
                    text = text + (new TextDecoder().decode(value));
                    message.innerHTML = `<div class="message">${text}</div>`;
                    chatBody.scrollTop = chatBody.scrollHeight;
                    read();
                });
            }
            // Start reading data
            read();
        })
        .catch(error => console.error('Error:', error));
    }
});