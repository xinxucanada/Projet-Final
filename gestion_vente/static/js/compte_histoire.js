let commandes = document.querySelectorAll(".commande");
    let btns = document.querySelectorAll("#btn");
    let btnMoins = document.querySelectorAll("#btnMoins");
    
    let tables = document.querySelectorAll("table");
    function affiche_moins () {
        for (let i = 0; i < tables.length; i++) {
        let trs = tables[i].querySelectorAll("tr");
        if (trs.length > 7) {
            for (let j = 7; j < trs.length; j++) {
                trs[j].style.display = "none";
            }
        }
        }
    }
    affiche_moins()

    for (let i = 0; i < commandes.length; i++) {
        btns[i].onclick = function() {
            let trs = tables[i].querySelectorAll("tr");
            let h = trs.length;
            commandes[i].style.height = 190 + (h - 7) * 18 + "px";
            for (let k = 0; k < trs.length; k++) {
                trs[k].style.display = "revert";
            }
        }
        btnMoins[i].onclick = function () {
            commandes[i].style.height = "150px";
            let trs = tables[i].querySelectorAll("tr");
            let h = trs.length;
            for (let k = 7; k < trs.length; k++) {
                trs[k].style.display = "none";
            }
        }
    }

