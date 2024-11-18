function opdaterOverskrift() {
    let overskrift = document.getElementById('overskrift');
    if (overskrift.className == 'orange') {
        overskrift.className = 'blue';
    }
    else {
        overskrift.className = 'orange'
    }
}

// https://www.onlinegames.io/t/embeddable-games-for-websites/
function skiftSpil(spilnummer) {
    spil = [];
    spil[0] = "https://www.onlinegames.io/games/2023/construct/280/head-soccer-2022/index.html";
    spil[1] = "https://playpager.com/embed/chess/index.html";
    spil[2] = "https://www.onlinegames.io/games/2023/construct/280/head-soccer-2022/index.html"

    let iframe = document.getElementById('spil');
    iframe.src = spil[spilnummer];
}

function calculateAge() {
    // alert('test');
    var currentDate = new Date();
    //alert(currentDate);
    var currentYear = currentDate.getFullYear();
    var currentMonth = currentDate.getMonth() + 1;
    var currentDay = currentDate.getDate();
    
    var birthDay = document.getElementById("birthday").value;
    var birthMonth = document.getElementById("birthmonth").value;
    var birthYear = document.getElementById("birthyear").value;

    var calculatedAge = currentYear - birthYear;

    if (currentMonth < birthMonth) {
        calculatedAge = calculatedAge - 1;
    }

    if (birthMonth == currentMonth && currentDay < birthDay) {
        calculatedAge = calculatedAge - 1;
    }

    var message = "Du er " + calculatedAge + " år gammel";
    if (birthDay == currentDay && birthMonth == currentMonth) {
        message = "DU har fødselsdag - stort tilykke!!!";
        var canvas = document.getElementById('confetti-canvas');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        startConfetti();
    }

    
    document.getElementById('result').innerHTML = message;
}