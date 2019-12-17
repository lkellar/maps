const colors = {
    GENERAL: "#FFAE03",  // General calls
    WARNING: "#E67F0D",  // Warning; may affect you if you are there
    HAZARD: "#FE4E00",  // Hazardous if you are there or nearby
    DANGER: "#E9190F", // Danger to you or others
    LETHAL: "#FF0F80",  // Lethal danger
    DEATH: "#000000",  // Certain death
};

function timeSince(dt) {
    let now = DateTime.utc();
    let seconds = ((now - dt) / 1000);
    let interval = Math.floor(seconds / 31536000);

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
        maxClusterRadius: 40
    });
    for (const call of data) {
        if (call["address"] !== "<UNKNOWN>" && call["city"] !== null) {
            let latlon = [call["lat"], call["lon"]];

            let cfg = CALL_TYPES[call["call_type"]];
            if (cfg !== false) {
                cfg = (cfg === null || cfg === undefined) ? CALL_TYPES.DEFAULT : cfg;
                let [color, icon] = cfg;
                if (filter === null || filter.includes(color)) {
                    let myIcon = L.divIcon({
                        html: `<i class="fa ${icon}" style="color: ${color};"></i>`,
                        iconSize: [40, 40],
                        className: 'iconDiv'
                    });

                    let datetime = DateTime.fromISO(call["timestamp"]);
                    let time_ago = timeSince(datetime);
                    let dt_string = datetime.toLocaleString(DateTime.DATETIME_SHORT);

                    let marker = L.marker(latlon, {
                        icon: myIcon,
                        timestamp: call["timestamp"]
                    }).bindPopup(`${call["call_type"]} <br> ${call["address"]} <br> ${call["city"]} <br> ${dt_string} (${time_ago} ago)`)
                        .openPopup();

                    markers.addLayer(marker);
                }
            }
        }
    }
    map.addLayer(markers);
}

const DateTime = luxon.DateTime;

let data;
let markers;
let map;

async function main() {
    let filter = [];
    if (document.getElementById("general").checked)
        filter.push(colors.GENERAL);
    if (document.getElementById("warning").checked)
        filter.push(colors.WARNING);
    if (document.getElementById("hazard").checked)
        filter.push(colors.HAZARD);
    if (document.getElementById("danger").checked)
        filter.push(colors.DANGER);
    if (document.getElementById("lethal").checked)
        filter.push(colors.LETHAL);
    if (document.getElementById("death").checked)
        filter.push(colors.DEATH);

    let daysAgo = document.getElementById("selectDaysAgo");
    daysAgo = daysAgo.options[daysAgo.selectedIndex].value;

    data = await fetch(`fetch/${daysAgo}`)
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
