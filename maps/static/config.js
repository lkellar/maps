// const neutral = "#FFAE03";
// const death = "#FF0F80";
// const danger = "#E9190F";
// const hazard = "#FE4E00";
// const warning = "#E67F0D";


const colors = {
    // GENERAL: "#FFAE03",  // general calls

    // Misdemeanor
    // Class A:
    //  Assault causing bodily injury, burglary, DUI w/o bodily injury, possession of controlled substance or weapon
    // Class B:
    //  Criminal mischief, criminal trespass, mild assault, indecent exposure, prostitution, graffiti, small theft

    // Felony
    // First-degree:
    //  Murder, rape, kidnapping, arson, fraud
    // Second-degree:
    //  Aggravated assault, felony assault, arson, manslaughter, possession of controlled substance, child molestation
    // Third-degree:
    //  Assault and battery, elder abuse, transmission of pornography, driving under the influence, fraud, arson
    // Fourth-degree:
    //  Involuntary manslaughter, burglary, larceny, resisting arrest
    // Federal:
    //  Bank fraud, Embezzlement, Credit card fraud, Forgery, Health care fraud

    // CRIME1: "#f97",  // Misdemeanor
    // CRIME2: "#f55",  // Non-violent felony
    // CRIME3: "#f00", // Violent felony

    // Danger
    // WARNING: "#E67F0D",  // possible hazard
    // HAZARD: "#FE4E00",  // thing that could be dangerous
    // DANGER: "#E9190F",  // violence probable; do not go here


    // How will this affect you
    GENERAL: "#FFAE03",  // General calls
    WARNING: "#E67F0D",  // Warning; may affect you if you are there
    HAZARD: "#FE4E00",  // Hazardous if you are there or nearby
    DANGER: "#E9190F", // Danger to you or others
    LETHAL: "#FF0F80",  // Lethal danger
    DEATH: "#000000",  // certain death


    // ACCIDENT: "#FE4E00",  //

    // WARNING: "#E67F0D",  // possibility of hazard
    // HAZARD: "#FE4E00",  // a source of danger (NOT IMMINENT)

    // DANGER: "#E9190F",  // probability of violence (NOT VIOLENT)
    // LETHAL: "#FF0F80",  // lethal danger (NOT DEATH)
};


const icons = {
    INFO: "fa-info-circle",
    EXCLAMATION: "fa-exclamation-triangle",

    WATER: "fa-water",
    CHILD: "fa-child",
    BRIEFCASE: "fa-suitcase",
    ID_CARD: "fa-id-card",
    LAPTOP: "fa-laptop",
    BIOHAZARD: "fa-biohazard",
    BED: "fa-bed",
    CAT: "fa-cat",
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
    "ABDUCTION FAMILY": [colors.HAZARD, icons.CHILD],
    "ABDUCTION NON FAMILY": [colors.DANGER, icons.CHILD],
    "ABUSE": [colors.HAZARD, icons.EXCLAMATION],
    "ACCIDENT": [colors.HAZARD, icons.CRASH],
    "ACCIDENT HIT AND RUN": [colors.DANGER, icons.CRASH],
    "ALARM": [colors.GENERAL, icons.EXCLAMATION],
    "ANNOYANCE": [colors.HAZARD, icons.EXCLAMATION],
    "ARMED PERSON": [colors.DANGER, icons.PERSON],
    "ASSAULT BATTERY": [colors.DANGER, icons.INJURED],
    "ASSIST AGENCY": null,
    "ASSIST CITIZEN": null,
    "BREAKING AND ENTERING": [colors.HAZARD, icons.PERSON],
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
    "CIVIL STANDBY": [colors.WARNING, icons.PERSON],
    "CODE 6": false,
    "CODE 7": false,
    "CODE 8": false,
    "CODE 9": false,
    "CRIMINAL MISCHIEF": [colors.DANGER, icons.MASK],
    "DEATH": [colors.DEATH, icons.SKULL],
    "DEATH NOTIFICATION": null,
    "DISTURBANCE": [colors.HAZARD, icons.RUNNING],
    "DRUG": [colors.WARNING, icons.DRUG],
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
    "FOUND PERSON": [colors.GENERAL, icons.PERSON],
    "FOUND PROPERTY": [colors.GENERAL, icons.BRIEFCASE],
    "FRAUD": [colors.WARNING, icons.MASK],
    "HARASSMENT": [colors.HAZARD, icons.PERSON],
    "HOSPICE DEATH": [colors.DEATH, icons.BED],
    "INDECENT EXPOSURE": [colors.HAZARD, icons.PERSON],
    "INFORMATIONAL": [colors.GENERAL, icons.INFO],
    "INTERNET CRIMES": [colors.WARNING, icons.LAPTOP],
    "INTOXICATED DRIVER": [colors.DANGER, icons.ALCOHOL],
    "INTOXICATED PERSON": [colors.HAZARD, icons.ALCOHOL],
    "LOITERING": [colors.HAZARD, icons.PERSON],
    "LOST PROPERTY": null,
    "LOUD PARTY": [colors.WARNING, icons.NOISE],
    "MENTAL PERSON": [colors.HAZARD, icons.PERSON],
    "MISSING PERSON": [colors.WARNING, icons.PERSON],
    "NOISE": [colors.WARNING, icons.NOISE],
    "PARKING PROBLEM": [colors.HAZARD, icons.CAR],
    "PROSTITUTION": [colors.WARNING, icons.EXCLAMATION],
    "PROWLER": [colors.HAZARD, icons.SECRET],
    "RECOVERY REPORT": null,
    "ROBBERY": [colors.DANGER, icons.MASK],
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
    "TRAFFIC LIGHT MALFUNCTION": [colors.WARNING, icons.TRAFFIC],
    "TRANSPORT": [colors.GENERAL, icons.CAR],
    "TRESPASSING": [colors.HAZARD, icons.WALKING],
    "UNLOCK": null,
    "WELFARE CONCERN": [colors.WARNING, icons.PERSON],

    DEFAULT: [colors.GENERAL, icons.EXCLAMATION]
};
