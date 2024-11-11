function opdaterOverskrift() {
    let overskrift = document.getElementById('overskrift');
    if (overskrift.className == 'orange') {
        overskrift.className = 'blue';
    }
    else {
        overskrift.className = 'orange'
    }
}