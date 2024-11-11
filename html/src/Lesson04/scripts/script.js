function opdaterOverskrift() {
    let overskrift = document.getElementById('overskrift');
    if (overskrift.className == 'orange') {
        overskrift.className = 'blue';
    }
    else {
        overskrift.className = 'orange'
    }
}

function skiftSpil(spilnummer){
    spil = [];
    spil[0] = "https://www.onlinegames.io/games/2024/unity/drift-king/index.html";
    spil[1] = "https://playpager.com/embed/chess/index.html";
    spil[2] = "https://www.onlinegames.io/games/2023/construct/280/head-soccer-2022/index.html";

    let spil_iframe = document.getElementById('spil');
    spil_iframe.src = spil[spilnummer];
}