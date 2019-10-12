
function displayMap(data) {
    console.log(data);

    var map = L.map('map').setView([36.082157, -94.171852], 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    for (const call of data) {
        L.marker([call["lat"], call["lon"]]).addTo(map)
            .bindPopup('A pretty CSS3 popup.<br> Easily customizable.')
            .openPopup();
    }
}



fetch('fetch')
    .then(response => {
        return response.json()
    })
    .then(data => {
        displayMap(data)
    })
    .catch(err => {
        console.log(err)
    });

