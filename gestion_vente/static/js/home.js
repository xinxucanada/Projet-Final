var img_roulant_container = document.querySelector(".img_roulant_container ul");
            var ul = document.querySelector(".img_roulant_container ul");
            var img = img_roulant_container.querySelector("img")
            var ol = document.querySelector(".circle");
            var arrow_l = document.querySelector(".arrow_l");
            var arrow_r = document.querySelector(".arrow_r");
            var img_width = img.offsetWidth;
            function animation(objet, but, callback){
                clearInterval(objet.timer);
                objet.timer = setInterval(function(){
                    var etape = (but - objet.offsetLeft) / 10;
                    etape = etape > 0 ? Math.ceil(etape) : Math.floor(etape)
                    if(objet.offsetLeft == but){
                        clearInterval(objet.timer);
                        callback && callback();
                    }
                    objet.style.left = objet.offsetLeft + etape + "px";
                }, 20);
                
            }
            img_roulant_container.addEventListener("mouseenter", function() {
                clearInterval(timer_auto_rouler);
                timer_auto_rouler = null;
            })
            img_roulant_container.addEventListener("mouseleave", function() {
                timer_auto_rouler = setInterval(function() {
                arrow_r.click();
            }, 2000)
            })
            // arrow_l.addEventListener("mouseenter", function(){
            //     clearInterval(timer_auto_rouler);
            //     timer_auto_rouler = null;
            // })
            // arrow_r.addEventListener("mouseenter", function(){
            //     clearInterval(timer_auto_rouler);
            //     timer_auto_rouler = null;
            // })
            // arrow_l.addEventListener("mouseleave", function(){
            //     timer_auto_rouler = setInterval(function() {
            //     arrow_r.click();
            // }, 2000)
            // })
            // arrow_r.addEventListener("mouseleave", function(){
            //     timer_auto_rouler = setInterval(function() {
            //     arrow_r.click();
            // }, 2000)
            // })
            for (var i = 0; i < ul.children.length; i++) {
                var li = document.createElement("li");
                li.setAttribute("index", i);
                ol.appendChild(li);
                li.addEventListener("mouseenter", function() {
                    for (var i = 0; i < ol.children.length; i++) {
                    ol.children[i].className = "";
                    }
                    this.className = "current_circle";
                    var index = this.getAttribute("index");
                    click_numbre = index;
                    circle_index = index;
                    animation(ul, -index * img_width)
                })
            }
            ol.children[0].className = "current_circle";
            var first_img_clone = ul.children[0].cloneNode(true);
            ul.appendChild(first_img_clone);
            var click_numbre = 0;
            var circle_index = 0;
            let flag = true;
            function circle_change() {
                for(var i = 0 ; i < ol.children.length; i++) {
                    ol.children[i].className = "";
                }
                ol.children[circle_index].className = "current_circle" 
            }
            arrow_r.addEventListener("click", function(){
                if (flag) {
                    flag = false;
                    if(click_numbre == ul.children.length - 1) {
                        ul.style.left = 0;
                        click_numbre = 0;
                    }
                    click_numbre++;
                    animation(ul, -click_numbre * img_width, function() {
                        flag = true;
                    });
                    circle_index++;
                    circle_index = circle_index == ol.children.length ? 0 : circle_index
                    // if(circle_index == ol.children.length) {
                    //     circle_index = 0;
                    // }
                    circle_change()
                    // for(var i = 0 ; i < ol.children.length; i++) {
                    //     ol.children[i].className = "";
                    // }
                    // ol.children[circle_index].className = "current_circle" 
                }
            })
            arrow_l.addEventListener("click", function(){
                if (flag) {
                    flag = false;
                    if(click_numbre == 0) {
                        click_numbre = ul.children.length - 1;
                        ul.style.left = -click_numbre * img_width + "px";
                    }
                    click_numbre--;
                    animation(ul, -click_numbre * img_width, function() {
                        flag = true;
                    });
                    circle_index--;
                    circle_index = circle_index < 0? ol.children.length - 1 : circle_index;
                    // if(circle_index < 0) {
                    //     circle_index = ol.children.length - 1;
                    // }
                    circle_change()
                    // for(var i = 0 ; i < ol.children.length; i++) {
                    //     ol.children[i].className = "";
                    // }
                    // ol.children[circle_index].className = "current_circle"
                }
            })
            var timer_auto_rouler = setInterval(function() {
                arrow_r.click();
            }, 2000)
