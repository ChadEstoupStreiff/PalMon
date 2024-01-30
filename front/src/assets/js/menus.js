

function load_menu(menu) {
    while (document.getElementById("content").firstChild) {
        document.getElementById("content").removeChild(document.getElementById("content").firstChild);
    }
    switch (menu) {
        default:
            load_inventory()
            break;
    }
}

window.onload = () => {
    if (user == null) {
        document.getElementById("header").childNodes.forEach((menu) => {
            menu.addEventListener("click", () => {
                document.getElementById("header").childNodes.forEach((menu_bis) => {menu_bis.className = ""});
                menu.className = "selected"
                load_menu(menu.innerHTML);
            })
        })
        
        
        div = document.createElement("div")
        div.id = "login_name"
        document.body.appendChild(div)
        
        user_input = document.createElement("h1")
        user_input.innerHTML = "Username"
        div.appendChild(user_input)
        
        user_input = document.createElement("input")
        user_input.type = "text"
        user_input.addEventListener('keyup', function (e) {
            if (e.key === 'Enter' || e.keyCode === 13) {
                user = user_input.value;
                document.body.removeChild(div);
                load_menu();
            }
        })
        div.appendChild(user_input)
    } else {
        load_menu();
    }
}