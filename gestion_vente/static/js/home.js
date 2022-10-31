var img_roulant_container = document.querySelector(".img_roulant_container ul");
            var ul = document.querySelector(".img_roulant_container ul");
            var img = img_roulant_container.querySelector("img")
            var ol = document.querySelector(".circle");
            var arrow_l = document.querySelector(".arrow_l");
            var arrow_r = document.querySelector(".arrow_r");
            var img_width = img.offsetWidth;
            // 封装动画函数，objet为DOM里的node，but为目标位置
            function animation(objet, but){
                clearInterval(objet.timer);
                objet.timer = setInterval(function(){
                    // 移动减速效果
                    var etape = (but - objet.offsetLeft) / 10;
                    // 大于零往上圆整，小于零向下圆整
                    etape = etape > 0 ? Math.ceil(etape) : Math.floor(etape)
                    if(objet.offsetLeft == but){
                        clearInterval(objet.timer);
                        
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
            arrow_l.addEventListener("mouseenter", function(){
                clearInterval(timer_auto_rouler);
                timer_auto_rouler = null;
            })
            arrow_r.addEventListener("mouseenter", function(){
                clearInterval(timer_auto_rouler);
                timer_auto_rouler = null;
            })
            arrow_l.addEventListener("mouseleave", function(){
                timer_auto_rouler = setInterval(function() {
                arrow_r.click();
            }, 2000)
            })
            arrow_r.addEventListener("mouseleave", function(){
                timer_auto_rouler = setInterval(function() {
                arrow_r.click();
            }, 2000)
            })
            //动态生成小圆圈
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
                    // 当鼠标经过圆圈，把圆圈的index给右键点击的计数click_numbre和circle_index
                    click_numbre = index;
                    circle_index = index;
                    // console.log(click_numbre)
                    animation(ul, -index * img_width)
                })
            }
            ol.children[0].className = "current_circle";
            // 克隆第一张图并放在尾部，当再点击右箭头，不经过动画直接跳转
            var first_img_clone = ul.children[0].cloneNode(true);
            ul.appendChild(first_img_clone);
            // 右箭头无缝滚动
            // 设置小圆圈index和右键点击计数起始值为0，随着点击右键自增1，到图的个数尾部再清零重来。
            var click_numbre = 0;
            var circle_index = 0;
            arrow_r.addEventListener("click", function(){
                if(click_numbre == ul.children.length - 1) {
                    ul.style.left = 0;
                    click_numbre = 0;
                }
                click_numbre++;
                // console.log("aa"+click_numbre)
                // console.log(-click_numbre * img_width)
                animation(ul, -click_numbre * img_width);
                circle_index++;
                if(circle_index == 6) {
                    circle_index = 0;
                }
                for(var i = 0 ; i < ol.children.length; i++) {
                    ol.children[i].className = "";
                }
                ol.children[circle_index].className = "current_circle"
                
            })
            arrow_l.addEventListener("click", function(){
                if(click_numbre == 0) {
                    
                    click_numbre = ul.children.length - 1;
                    ul.style.left = -click_numbre * img_width + "px";
                   
                }
                // console.log(-click_numbre * img_width)
                click_numbre--;
                // console.log("aa"+click_numbre)
                animation(ul, -click_numbre * img_width);
                circle_index--;
                if(circle_index < 0) {
                    circle_index = 5;
                }
                for(var i = 0 ; i < ol.children.length; i++) {
                    ol.children[i].className = "";
                }
                ol.children[circle_index].className = "current_circle"
            })
            var timer_auto_rouler = setInterval(function() {
                arrow_r.click();
            }, 2000)