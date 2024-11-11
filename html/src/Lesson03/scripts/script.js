function opdaterOverskrift(){
    let overskrift = document.getElementById('overskrift').innerHTML;
    let navn = document.getElementById('navn').value;
    let alder = document.getElementById('alder').value;

    let foedselsaar = 2024 - parseInt(alder);
    let besked = 'Hej '+ navn + ' på ' + alder + ' år. Du er født i ' + foedselsaar + '. Velkommen til!';
    document.getElementById('overskrift').innerHTML = besked;
}