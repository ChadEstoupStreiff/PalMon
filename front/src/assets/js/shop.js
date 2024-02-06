function buy(item) {
    start_loading()
    fetch(api_url + 'buy?user=' + user + '&object=' + item, {
        method: 'PUT',
        headers: {
            'Accept': 'application/json',
        },
    })
    .then(response => {
        if (response.ok) {
            load_shop()
        } else {
            throw new Error('Network response was not ok.');
        }
    })
}

function sell(item) {
    start_loading()
    fetch(api_url + 'sell?user=' + user + '&object=' + item, {
        method: 'PUT',
        headers: {
            'Accept': 'application/json',
        },
    })
    .then(() => {
        load_shop()
    })
}

function load_shop() {
    start_loading()
    clear_menu()
    fetch(api_url + 'money?user=' + user, {
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

        fetch(api_url + 'shop', {
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
            shop_items = response;

            amount_div = document.createElement("div")
            amount_div.id="shop_amount"
            amount_div.innerHTML = "<h1>" + money_amount + " $</h1>"

            sell_div = document.createElement("div")
            sell_div.id="shop_sell"

            Object.entries(shop_items.sell).forEach(([key, value]) => {
                item_div = document.createElement("div")
                item_div.className = "shop_item"
                item_div.innerHTML = "<img src='" + assets_url + "img/general/" + key + ".webp'/><h2>" + key + "</h2><h1>" + value + " $</h1>"
                item_div.addEventListener("click", () => {
                    sell(key)
                })
                sell_div.appendChild(item_div)
            });

            buy_div = document.createElement("div")
            buy_div.id="shop_buy"

            Object.entries(shop_items.buy).forEach(([key, value]) => {
                item_div = document.createElement("div")
                item_div.className = "shop_item"
                item_div.innerHTML = "<img src='" + assets_url + "img/general/" + key + ".webp'/><h2>" + key + "</h2><h1>" + value + " $</h1>"
                item_div.addEventListener("click", () => {
                    buy(key)
                })
                buy_div.appendChild(item_div)
            });

            document.getElementById("content").appendChild(amount_div)
            title = document.createElement("h1")
            title.innerHTML = "Sell"
            document.getElementById("content").appendChild(title)
            document.getElementById("content").appendChild(sell_div)
            title = document.createElement("h1")
            title.innerHTML = "Buy"
            document.getElementById("content").appendChild(title)
            document.getElementById("content").appendChild(buy_div)
            stop_loading()
        })
    })
}