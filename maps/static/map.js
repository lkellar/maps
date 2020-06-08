
const colors = {
    GENERAL: "#FFAE03",  // General calls
    WARNING: "#E67F0D",  // Warning; may affect you if you are there
    HAZARD: "#FE4E00",  // Hazardous if you are there or nearby
    DANGER: "#E9190F", // Danger to you or others
    LETHAL: "#FF0F80",  // Lethal danger
    DEATH: "#000000",  // Certain death
};


const icons = {
    INFO: "fa-info-circle",
    EXCLAMATION: "fa-exclamation-triangle",
    QUESTION: "fa-question-circle",

    WATER: "fa-water",
    CHILD: "fa-child",
    BRIEFCASE: "fa-suitcase",
    ID_CARD: "fa-id-card",
    LAPTOP: "fa-laptop",
    BIOHAZARD: "fa-biohazard",
    BED: "fa-bed",
    CAT: "fa-cat",
    DOG: "fa-dog",
    RUNNING: "fa-running",
    WALKING: "fa-walking",
    TRAFFIC: "fa-traffic-light",
    PHONE: "fa-phone",
    TRUCK: "fa-truck",
    CAR: "fa-car",
    TRASH: "fa-trash",
    SHOPPING: "fa-shopping-cart",
    NOISE: "fa-volume-up",
    PERSON: "fa-male",
    ALCOHOL: "fa-wine-bottle",
    OIL: "fa-oil-can",
    SPRAY_CAN: "fa-spray-can",

    INJURED: "fa-user-injured",
    AMBULANCE: "fa-ambulance",
    CRASH: "fa-car-crash",
    MASK: "fa-mask",
    SECRET: "fa-user-secret",
    DRUG: "fa-cannabis",
    FIRE: "fa-fire",
    DUMPSTER_FIRE: "fa-dumpster-fire",

    SKULL: "fa-skull-crossbones"
};

const CALL_TYPES = {
    "911 HANGUP": [colors.GENERAL, icons.PHONE],
    "911 OPEN LINE": [colors.GENERAL, icons.PHONE],
    ">CHOOSE CALL TYPE<": false,
    "ABANDONED VEH": [colors.WARNING, icons.CAR],
    "ABANDONED VEHICLES": [colors.WARNING, icons.CAR],
    "ABDUCTION FAMILY": [colors.HAZARD, icons.CHILD],
    "ABDUCTION NON FAMILY": [colors.DANGER, icons.CHILD],
    "ABUSE": [colors.HAZARD, icons.EXCLAMATION],
    "ACCIDENT": [colors.HAZARD, icons.CRASH],
    "ACCIDENT HIT AND RUN": [colors.DANGER, icons.CRASH],
    "ACCIDENT - PRIVATE PROPERTY": [colors.HAZARD, icons.CRASH],
    "ALARM": [colors.GENERAL, icons.EXCLAMATION],
    "ANIMAL BITE": [colors.WARNING, icons.CAT],
    "ANIMAL CALL": [colors.WARNING, icons.CAT],
    "ANIMAL COMPLAINT": [colors.WARNING, icons.CAT],
    "ANIMAL STRAY DOG": [colors.WARNING, icons.DOG],
    "ANNOYANCE": [colors.HAZARD, icons.EXCLAMATION],
    "ARMED PERSON": [colors.DANGER, icons.PERSON],
    "ASSAULT BATTERY": [colors.DANGER, icons.INJURED],
    "ASSIST AGENCY": null,
    "AGENCY ASSIST": null,
    "ASSIST CITIZEN": null,
    "BREAKING AND ENTERING": [colors.HAZARD, icons.PERSON],
    "BREAKING OR ENTERING": [colors.HAZARD, icons.PERSON],
    "BURGLARY": [colors.HAZARD, icons.MASK],
    "CD ANIMAL SERVICES": [colors.WARNING, icons.CAT],
    "CD FACILITIES": null,
    "CD FLEET": null,
    "CD METER": null,
    "CD PARKING ENFORCEMENT": null,
    "CD PARKS": null,
    "CD SEWER": null,
    "CD SOLID WASTE": null,
    "CD STREET": null,
    "CD TRAFFIC": null,
    "CD WATER": [colors.GENERAL, icons.WATER],
    "CHECKING SUBJECT": null, // I don't even know what this is
    "CIVIL STANDBY": [colors.WARNING, icons.PERSON],
    "CIVIL MATTER": [colors.GENERAL, icons.INFO],
    "CODE 6": false,
    "CODE 7": false,
    "CODE 8": false,
    "CODE 9": false,
    "CONTRABAND": [colors.HAZARD, icons.SHOPPING],
    "CRIMINAL MISCHIEF": [colors.DANGER, icons.MASK],
    "DEATH": [colors.DEATH, icons.SKULL],
    "DEATH NOTIFICATION": null,
    "DISORDERLY CONDUCT": [colors.WARNING, icons.PERSON],
    "DISTURBANCE": [colors.HAZARD, icons.RUNNING],
    "DOMESTIC BATTERY REPORT": [colors.DANGER, icons.INJURED],
    "DOMESTIC DISTURBANCE": [colors.HAZARD, icons.RUNNING],
    "DRUG": [colors.WARNING, icons.DRUG],
    "DRUGS-NARCOTICS": [colors.WARNING, icons.DRUG],
    "DUMPING LITTERING": [colors.WARNING, icons.TRASH],
    "EMERGENCY MESSAGE": null,
    "ESCORT": null,
    "FD AIRCRAFT EMERGENCY": null,
    "FD AIRCRAFT STANDBY": null,
    "FD ALARM": [colors.HAZARD, icons.EXCLAMATION],
    "FD CARBON MONOXIDE DETECTOR": null,
    "FD CEMS ASSIST": [colors.HAZARD, icons.AMBULANCE],  // community EMS; community emergency medical services
    "FD CONTROLLED BURN": [colors.WARNING, icons.DUMPSTER_FIRE],
    "FD EXTRICATION": [colors.DANGER, icons.FIRE],
    "FD FUEL SPILL": [colors.WARNING, icons.OIL],
    "FD HAZMAT": [colors.HAZARD, icons.BIOHAZARD],
    "FD LARGE VEH": [colors.GENERAL, icons.TRUCK],
    "FD LIFTING ASSISTANCE": null,
    "FD MUTUAL AID": null,
    "FD MVA": [colors.HAZARD, icons.CRASH],  // motor vehicle accident
    "FD RESCUE": null,
    "FD RUBBISH": [colors.GENERAL, icons.TRASH],
    "FD SERVICE CALL": null,
    "FD STRUCTURE FIRE": [colors.DANGER, icons.DUMPSTER_FIRE],
    "FD UTILITIES": null,
    "FD VEGETATION": null,
    "FD VEH FIRE": [colors.DANGER, icons.FIRE],
    "FIREWORKS": [colors.GENERAL, icons.FIRE],
    "FLAGGED DOWN": [colors.GENERAL, icons.INFO],
    "FOLLOW UP": null,
    "FOUND PERSON": [colors.GENERAL, icons.PERSON],
    "FOUND PROPERTY": [colors.GENERAL, icons.BRIEFCASE],
    "FRAUD": [colors.WARNING, icons.MASK],
    "GRAFFITI": [colors.WARNING, icons.SPRAY_CAN],
    "GUNSHOTS": [colors.DANGER, icons.NOISE],
    "HARASSMENT": [colors.HAZARD, icons.PERSON],
    "HARASSING COMMUNICATIONS": [colors.HAZARD, icons.PERSON],
    "HOSPICE DEATH": [colors.DEATH, icons.BED],
    "INDECENT EXPOSURE": [colors.HAZARD, icons.PERSON],
    "INFORMATIONAL": [colors.GENERAL, icons.INFO],
    "INTERNET CRIMES": [colors.WARNING, icons.LAPTOP],
    "INTOXICATED DRIVER": [colors.DANGER, icons.ALCOHOL],
    "INTOXICATED PERSON": [colors.HAZARD, icons.ALCOHOL],
    "LOITERING": [colors.HAZARD, icons.PERSON],
    "LOST PROPERTY": [colors.GENERAL, icons.QUESTION],
    "LOST-FOUND PROPERTY": [colors.GENERAL, icons.QUESTION],
    "LOUD PARTY": [colors.WARNING, icons.NOISE],
    "LOST PET": [colors.GENERAL, icons.CAT],
    "MENTAL PERSON": [colors.HAZARD, icons.PERSON],
    "MISSING PERSON": [colors.WARNING, icons.PERSON],
    "NOISE": [colors.WARNING, icons.NOISE],
    "NOISE COMPLAINT": [colors.WARNING, icons.NOISE],
    "PARKING PROBLEM": [colors.HAZARD, icons.CAR],
    "PROSTITUTION": [colors.WARNING, icons.EXCLAMATION],
    "PROWLER": [colors.HAZARD, icons.SECRET],
    "RECKLESS": [colors.DANGER, icons.EXCLAMATION],
    "RECKLESS DRIVER": [colors.DANGER, icons.EXCLAMATION],
    "RECOVERY REPORT": null,
    "ROBBERY": [colors.DANGER, icons.MASK],
    "SAFETY CK OF PREMISES": [colors.WARNING, icons.PERSON],
    "SCHOOL ASSIGNMENT": [colors.WARNING, icons.BRIEFCASE],
    "SHOOTING": [colors.LETHAL, icons.SKULL],
    "SHOPLIFTER": [colors.HAZARD, icons.SHOPPING],
    "SHOTS HEARD": [colors.DANGER, icons.NOISE],
    "SPECIAL ASSIGNMENT": null,
    "STABBING": [colors.LETHAL, icons.SKULL],
    "STOLEN VEHICLE": [colors.HAZARD, icons.CAR],
    "SUICIDE THREAT": [colors.LETHAL, icons.SKULL],
    "SUSPICIOUS ACTIVITY": [colors.HAZARD, icons.SECRET],
    "TEST": null,
    "THEFT": [colors.HAZARD, icons.MASK],
    "THREAT": [colors.HAZARD, icons.PERSON],
    "TRAFFIC COMPL": [colors.GENERAL, icons.TRAFFIC],  // traffic complaint
    "TRAFFIC CONTROL": [colors.GENERAL, icons.TRAFFIC],
    "TRAFFIC HAZARD": [colors.WARNING, icons.TRAFFIC],
    "TRAFFIC HAZARD-LIVESTOCK": [colors.WARNING, icons.TRAFFIC],
    "TRAFFIC LIGHT MALFUNCTION": [colors.WARNING, icons.TRAFFIC],
    "TFC LIGHT PROBLEM": [colors.WARNING, icons.TRAFFIC],
    "TRAFFIC STOP": [colors.WARNING, icons.TRAFFIC],
    "TRANSPORT": [colors.GENERAL, icons.CAR],
    "TRESPASSING": [colors.HAZARD, icons.WALKING],
    "TRESPASSING-IN PROGESS": [colors.HAZARD, icons.WALKING],
    "UNLOCK": null,
    "UNAUTHORIZED USE VEHICLE": [colors.HAZARD, icons.CAR],
    "VEHICLE RECOVERY": [colors.WARNING, icons.CAR],
    "VEHICLE REPOSSESSION": [colors.WARNING, icons.CAR],
    "VEHICLE TOWED": [colors.WARNING, icons.CAR],
    "WELFARE CONCERN": [colors.WARNING, icons.PERSON],
    "WELFARE CHECK": [colors.WARNING, icons.PERSON],

    DEFAULT: [colors.GENERAL, icons.EXCLAMATION]
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

            let cfg = CALL_TYPES[call["call_type"].toUpperCase()];
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

                    let popupText = `${call["call_type"]}<br>${call["address"]}<br>${call["city"]}`;
                    if (call["notes"]) {
                        popupText += `<br>${call["notes"].replace('\n', '<br>')}`;
                    }
                    popupText += `<br>${dt_string} (${time_ago} ago)`;

                    let marker = L.marker(latlon, {
                        icon: myIcon,
                        timestamp: call["timestamp"]
                    }).bindPopup(popupText).openPopup();

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

function validateDateInputs() {
    start = document.getElementById('start').value;
    end = document.getElementById('end').value;

    if (start === '') {
        // If empty, set placeholder
        document.getElementById('start').placeholder = new Date(new Date().getTime() - 8640000).toISOString().split('T')[0];
        return false;
    } else if ( !start.match(/^\d{4}-[01]\d-[0-3]\d$/)) {
        // If invalid date, make it red and return false
        document.getElementById('start').style.color = 'red';
        return false;
    }

    if (end === '') {
        document.getElementById('end').placeholder = new Date().toISOString().split('T')[0];
        return false;
    } else if (!end.match(/^\d{4}-[01]\d-[0-3]\d$/)) {
        document.getElementById('end').style.color = 'red';
        return false;
    }

    if (Date.parse(end) - Date.parse(start) < 0) {

        // If start after end, make both red
        
        document.getElementById('start').style.color = 'red';
        document.getElementById('end').style.color = 'red';
        return false;
    }

    // Both good, make them both black
    document.getElementById('start').style.color = 'black';
    document.getElementById('end').style.color = 'black';

    return true;
}

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

    if (daysAgo === 'custom') {
        document.getElementById('datepicker').style.display = 'inherit';
        if (!validateDateInputs()) {
            return;
        }

        start = document.getElementById('start').value;
        end = document.getElementById('end').value;

        data = await fetch(`fetch/${start}/${end}`)
        .then(response => {
            return response.json();
        })
        .catch(err => {
            console.log(err);
        });
    } else {
        document.getElementById('datepicker').style.display = 'none';
        data = await fetch(`fetch/${daysAgo}`)
        .then(response => {
            return response.json();
        })
        .catch(err => {
            console.log(err);
        });
    }

    if (map == null) initMap();
    else {
        map.removeLayer(markers);
    }
    displayMap(data, filter);
}

// set defaults
document.getElementById('start').value = new Date(new Date().getTime() - 86400000).toISOString().split('T')[0];
document.getElementById('end').value = new Date().toISOString().split('T')[0];

main();
