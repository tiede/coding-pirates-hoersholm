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
    stopConfetti();
    var currentDate = new Date();
    var currentYear = currentDate.getFullYear();
    var currentMonth = currentDate.getMonth();
    var currentDay = currentDate.getDate(); 

    var birthDay = document.getElementById('birthday').value;
    var birthMonth = document.getElementById('birthmonth').value;
    var birthYear = document.getElementById('birthyear').value;

    var calculatedAge = currentYear - birthYear;

    // Hvis måned nu er mindre end fødselsmåned, så har du ikke haft fødselsdag endnu
    if (currentMonth < birthMonth - 1) {
        calculatedAge--;
    }
    // 
    if (birthMonth == currentMonth + 1 && currentDay < birthDay) {
        calculatedAge--;
    }
    console.log(calculatedAge);
    
    var msg = "Du er " + calculatedAge + " år gammel!";
    if (birthDay == currentDay && birthMonth == currentMonth + 1) {
        startConfetti();
        var birthdayMsg = "Du har fødselsdag i dag - TILLYKKE";
        msg = birthdayMsg + "<br />" + msg;
    }
    document.getElementById('result').innerHTML = msg
    
}
 