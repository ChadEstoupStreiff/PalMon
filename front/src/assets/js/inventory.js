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
}

function load_inventory() {
    content = document.getElementById("content")

    bag = document.createElement("div")
    bag.id = "bag"
    content.appendChild(bag)

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