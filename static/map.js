
function timeSince(date) {
    var seconds = Math.floor((new Date() - date) / 1000);
    var interval = Math.floor(seconds / 31536000);

    if (interval > 1) {
        return interval + " years";
    }
    interval = Math.floor(seconds / 2592000);
    if (interval > 1) {
        return interval + " months";
    }
    interval = Math.floor(seconds / 86400);
    if (interval > 1) {
        return interval + " days";
    }
    interval = Math.floor(seconds / 3600);
    if (interval > 1) {
        return interval + " hours";
    }
    interval = Math.floor(seconds / 60);
    if (interval > 1) {
        return interval + " minutes";
    }
    return Math.floor(seconds) + " seconds";
}








function initMap() {
    map = L.map('leafletmap').setView([36.082157, -94.171852], 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
}


function displayMap(data, filter=null) {
    markers = L.markerClusterGroup({
        maxClusterRadius: 2
    });
    for (const call of data) {
        if (call["address"] !== "<UNKNOWN>" && call["city"] !== null) {
            let latlon = [call["lat"], call["lon"]];

            let cfg = callTypeConfig[call["call_type"]];
            if (cfg !== false) {
                cfg = (cfg === null) ? callTypeConfig["DEFAULT"] : cfg;
                let [icon, color] = cfg;
                if (filter === null || filter.includes(color)) {
                    let myIcon = L.divIcon({
                        html: `<i class="fa ${icon}" style="color: ${color};"></i>`,
                        iconSize: [40, 40],
                        className: 'iconDiv'
                    });

                    $time_ago = timeSince(new Date(call["datetime"]));

                    let marker = L.marker(latlon, {
                        icon: myIcon,
                        timestamp: call["datetime"]
                    }).bindPopup(`${call["call_type"]} <br> ${call["address"]} <br> ${call["city"]} <br> ${call["datetime"]} (${$time_ago} ago)`)
                        .openPopup();

                    markers.addLayer(marker);
                }
            }
        }
    }
    map.addLayer(markers);
}


let data;
let markers;
let map;

async function main() {
    let filter = [];
    if (document.getElementById("neutral").checked)
        filter.push(neutral);
    if (document.getElementById("warning").checked)
        filter.push(warning);
    if (document.getElementById("hazard").checked)
        filter.push(hazard);
    if (document.getElementById("danger").checked)
        filter.push(danger);
    if (document.getElementById("death").checked)
        filter.push(death);

    let daysAgo = document.getElementById("selectDaysAgo");
    daysAgo = daysAgo.options[daysAgo.selectedIndex].value;

    data = await fetch(`fetch?days=${daysAgo}`)
        .then(response => {
            return response.json()
        })
        .catch(err => {
            console.log(err)
        });

    if (map == null) initMap();
    else {
        map.removeLayer(markers);
    }
    displayMap(data, filter);
}


main();
