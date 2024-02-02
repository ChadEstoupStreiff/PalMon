function cheat_palmon() {
    fetch(api_url + 'palmon', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
        },
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Network response was not ok.');
        }
    }).then(data => {
        fetch(api_url + 'storage?user=' + user + '&palmon_id=' + data.id, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
            },
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Network response was not ok.');
            }
        }).then(data => {
            if (data.length > 0)
                data.forEach(palmon => {
                    display_palmon_card(bag, palmon)
                });
            else {
                error = document.createElement("h1")
                error.innerHTML = "No Palmons"
                bag.appendChild(error)
            }
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
    })
    .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
    });
}

function display_info_palmon(palmon) {
    div = document.createElement("div");
    div.id = "palmon_info"

    img = document.createElement("img")
    img.src = assets_url + "img/palmons/" + palmon.type + ".webp"
    div.appendChild(img)

    palmonname = document.createElement("h1")
    palmonname.innerHTML = palmon.type
    div.appendChild(palmonname)

    lvl = document.createElement("h3")
    lvl.innerHTML = "lvl " + palmon.lvl + " | exp " + palmon.exp
    div.appendChild(lvl)

    stats = document.createElement("p")
    stats.innerHTML = "HP " + palmon.stat_hp + "<br/>Damage " + palmon.stat_dmg + "<br/>Defense " + palmon.stat_def + "<br/>Speed " + palmon.stat_spd
    div.appendChild(stats)

    div.appendChild(document.createElement("hr"))

    switch_button = document.createElement("p");
    switch_button.className = "button"
    switch_button.addEventListener("click", () => {
        fetch(api_url + 'switch?user=' + user + '&palmon_id=' + palmon.id, {
            method: 'PUT',
            headers: {
                'Accept': 'application/json',
            },
        })
        .then(() => {
            clear_menu()
            load_inventory()
        })
        document.body.removeChild(div)
    })
    switch_button.innerHTML = "Move"
    div.appendChild(switch_button)

    release_button = document.createElement("p");
    release_button.className = "button red"
    release_button.addEventListener("click", () => {
        fetch(api_url + 'release?user=' + user + '&palmon_id=' + palmon.id, {
            method: 'DELETE',
            headers: {
                'Accept': 'application/json',
            },
        })
        .then(() => {
            clear_menu()
            load_inventory()
        })
        document.body.removeChild(div)
    })
    release_button.innerHTML = "Release"
    div.appendChild(release_button)
    
    div.appendChild(document.createElement("hr"))

    close_button = document.createElement("p");
    close_button.className = "button red"
    close_button.addEventListener("click", () => {
        document.body.removeChild(div)
    })
    close_button.innerHTML = "Cancel"
    div.appendChild(close_button)

    document.body.appendChild(div)
}

function display_palmon_card(element, palmon) {
    div = document.createElement("div");
    div.className = "palmon_card"

    img = document.createElement("img")
    img.src = assets_url + "img/palmons/" + palmon.type + ".webp"
    div.appendChild(img)

    palmonname = document.createElement("h2")
    palmonname.innerHTML = palmon.type
    div.appendChild(palmonname)

    lvl = document.createElement("h3")
    lvl.innerHTML = "lvl " + palmon.lvl + " | exp " + palmon.exp
    div.appendChild(lvl)

    stats = document.createElement("p")
    stats.innerHTML = "HP " + palmon.stat_hp + "<br/>Damage " + palmon.stat_dmg + "<br/>Defense " + palmon.stat_def + "<br/>Speed " + palmon.stat_spd
    div.appendChild(stats)

    element.appendChild(div)

    div.addEventListener("click", () => {
        display_info_palmon(palmon)
    });
}

function load_inventory() {
    content = document.getElementById("content")

    bag_title = document.createElement("h2")
    bag_title.innerHTML = "Equipe"
    content.appendChild(bag_title)

    bag = document.createElement("div")
    bag.id = "bag"
    content.appendChild(bag)

    storage_title = document.createElement("h2")
    storage_title.innerHTML = "Storage"
    content.appendChild(storage_title)

    storage = document.createElement("div")
    storage.id = "storage"
    content.appendChild(storage)

    fetch(api_url + 'bag?user=' + user, {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
        },
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Network response was not ok.');
        }
    }).then(data => {
        if (data.length > 0)
            data.forEach(palmon => {
                display_palmon_card(bag, palmon)
            });
        else {
            error = document.createElement("h1")
            error.innerHTML = "No Palmon"
            bag.appendChild(error)
        }
    })
    .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
    });

    fetch(api_url + 'storage?user=' + user, {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
        },
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Network response was not ok.');
        }
    }).then(data => {
        if (data.length > 0)
            data.forEach(palmon => {
                display_palmon_card(storage, palmon)
            });
        else {
            error = document.createElement("h1")
            error.innerHTML = "No Palmon"
            storage.appendChild(error)
        }
    })
    .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
    });
}