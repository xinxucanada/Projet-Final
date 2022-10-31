window.addEventListener('load', function(){
    let connecter = document.querySelector(".connecter");
        let ul = connecter.querySelector("ul");
        connecter.onmouseover = function(){
            ul.style.display = 'block';
        }
        connecter.onmouseout = function(){
            ul.style.display = 'none';
        }
})


