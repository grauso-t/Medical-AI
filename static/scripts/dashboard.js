document.addEventListener("DOMContentLoaded", function () {
    const jqueryScript = document.createElement('script');
    jqueryScript.src = 'https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.1/jquery.js';
    jqueryScript.onload = function () {
        $(document).ready(function () {
            updateClock();
        });
    };
    document.head.appendChild(jqueryScript);
});

function updateClock() {
    var now = new Date();
    var hours = now.getHours();
    var minutes = now.getMinutes();
    var seconds = now.getSeconds();
    hours = hours < 10 ? '0' + hours : hours;
    minutes = minutes < 10 ? '0' + minutes : minutes;
    seconds = seconds < 10 ? '0' + seconds : seconds;
    var time = hours + ':' + minutes + ':' + seconds;

    var dayOfWeek = now.toLocaleDateString('en-US', { weekday: 'long' });
    var date = now.toISOString().slice(0, 10); // Ottieni la data nel formato YYYY-MM-DD

    var formattedDateTime = date + ' (' + dayOfWeek + ') ' + time;
    document.getElementById('clock').innerText = formattedDateTime;

    setTimeout(updateClock, 1000); // Aggiorna ogni secondo
}
