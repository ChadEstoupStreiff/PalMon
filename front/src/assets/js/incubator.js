hatched_palmon = null

function hatch(incubator_id) {
    start_loading()
    fetch(api_url + 'incubator/hatch?user=' + user + '&incubator_id=' + incubator_id, {
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
    })
    .then(response => {
        if (response != false) {
            hatched_palmon = response
        }
        load_incubator()
    })
}

function place(incubator_id) {
    start_loading()
    fetch(api_url + 'incubator/place?user=' + user + '&incubator_id=' + incubator_id, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
        },
    })
    .then(() => {
        load_incubator()
    })
}

function load_incubator() {
    start_loading()
    clear_menu()
    fetch(api_url + 'date', {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
            'Access-Control-Allow-Origin': '*',
        },
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Network response was not ok.');
        }
    })
    .then(response => {
        date = response

        date_h = document.createElement("h2")
        date_h.innerHTML = "Server time: " + new Date(date).toLocaleString()
        document.getElementById("content").appendChild(date_h)

        fetch(api_url + 'egg?user=' + user, {
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
        })
        .then(response => {
            money_amount = response

            amount_div = document.createElement("div")
            amount_div.id="shop_amount"
            amount_div.innerHTML = "<h3>You have<h3><h1>" + money_amount + " eggs</h1>"
            document.getElementById("content").appendChild(amount_div)


            fetch(api_url + 'incubator?user=' + user, {
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
            })
            .then(response => {
                incubators = response

                incubator_div = document.createElement("div")
                incubator_div.id="shop_sell"

                incubators.forEach((incubator) => {
                    item_div = document.createElement("div")
                    item_div.className = "shop_item"
                    if (incubator.occupied) {
                        const differenceInMilliseconds =  new Date(incubator.hatch_date) - new Date(date)
                        if (differenceInMilliseconds > 0) {
                            const differenceInSeconds = Math.floor(differenceInMilliseconds / 1000);
                            item_div.innerHTML = "<img src='" + assets_url + "img/general/incubator.webp'/><h3>" + parseInt(differenceInSeconds/3600%60) + ":" + parseInt(differenceInSeconds/60%60) + ":" + parseInt(differenceInSeconds % 60) + "</h3>"
                        } else {
                            item_div.innerHTML = "<img src='" + assets_url + "img/general/incubator.webp'/><h2>Click to hatch!</h2>"
                        }
                        item_div.addEventListener("click", () => {
                            hatch(incubator.incubator_id)
                        })
                    } else {
                        item_div.innerHTML = "<img src='" + assets_url + "img/general/incubator_empty.webp'/><p>Click to place an egg</p>"
                        item_div.addEventListener("click", () => {
                            place(incubator.incubator_id)
                        })
                    }
                    
                    incubator_div.appendChild(item_div)
                });

                document.getElementById("content").appendChild(incubator_div)
                stop_loading()
            })
        })
    })
}