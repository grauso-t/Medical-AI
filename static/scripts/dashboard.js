document.addEventListener("DOMContentLoaded", function () {
    const jqueryScript = document.createElement('script');
    jqueryScript.src = 'https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.1/jquery.js';
    jqueryScript.onload = function () {
        $(document).ready(function () {
            updateClock();
            fetchData();
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

function showLoading() {
    var loadingImages = document.getElementsByClassName('loading-image');
    for (var i = 0; i < loadingImages.length; i++) {
        loadingImages[i].style.display = 'block';
    }
}

function hideLoading() {
    var loadingImages = document.getElementsByClassName('loading-image');
    for (var i = 0; i < loadingImages.length; i++) {
        loadingImages[i].style.display = 'none';
    }
}

function fetchData() {
    showLoading();
    fetch('/loadata')
        .then(response => response.json())
        .then(data => {
            hideLoading();
            console.log(data);
            
            var observationDataDiv = document.getElementById('container-observation');
            data.observation.forEach(function(item) {
                var observationDiv = document.createElement('div');
                observationDiv.innerHTML = `
                    <p><strong>Observation ID:</strong> ${item['Observation ID']}</p>
                    <p><strong>Last Updated:</strong> ${item['Last Updated']}</p>
                    <p><strong>Observation Code (LOINC):</strong> ${item['Observation Code (LOINC)']}</p>
                    <hr>
                `;
                observationDataDiv.appendChild(observationDiv);
            });

            var patientDataDiv = document.getElementById('container-patient');
            data.patient.forEach(function(items) {
                var patientDiv = document.createElement('div');
                patientDiv.innerHTML = `
                    <p><strong>Patient ID:</strong> ${items['Patient ID']}</p>
                    <p><strong>Birth Date:</strong> ${items['Birth Date']}</p>
                    <p><strong>Gender:</strong> ${items['Gender']}</p>
                    <hr>
                `;
                patientDataDiv.appendChild(patientDiv);
            });
        })
        .catch(error => {
            hideLoading();
            console.error('Errore:', error)
        });
}