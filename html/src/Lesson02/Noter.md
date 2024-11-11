
# Hvad skal vi i dag 

- Vi skal lave et favicon
- Vi skal kode noget javascript

# Hvad skal vi lave i dag (7/10)
- Vi skal lege med stylesheets
- Vi skal kode noget javascript
    - Vi skal forstå løkker og forgreninger




function opdaterOverskrift(){
    for (let i = 0; i < 5; i++) {
        alert('Hej med dig');
    }
}

- Skift farve på overskrift

<link href="styles/styles.css" rel="stylesheet" />

<h1 id="overskrift" class="blue">Velkommen til min hjemmeside om alt muligt</h1>

function opdaterOverskrift() {
    let overskrift = document.getElementById('overskrift');
    if (overskrift.className == "orange") {
        overskrift.className = "blue";
    }
    else {
        overskrift.className = "orange";
    }
}
<<<½½½½½½½½½½½1>>>
- iframe spil
<iframe src="https://cdn.htmlgames.com/TetroClassic/" scrolling="no" height="600" width="600">
</iframe></br>