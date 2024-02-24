function cheat_eggs(quantity) {
    start_loading()
    fetch(api_url + 'cheat/eggs?user=' + user + '&quantity=' + quantity, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
        },
    })
    .then(() => {
        load_menu("egg")
    })
}

function cheat_dollars(amount) {
    start_loading()
    fetch(api_url + 'cheat/dollars?user=' + user + '&amount=' + amount, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
        },
    })
    .then(() => {
        load_menu("shopping_cart")
    })
}

function cheat_palmon(quantity) {
    start_loading()
    fetch(api_url + 'cheat/palmon?user=' + user + '&quantity=' + quantity, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
        },
    })
    .then(() => {
        load_menu("backpack")
    })
}

function cheat_hatch() {
    start_loading()
    fetch(api_url + 'cheat/hatch', {
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
        hatched_palmon.push(response)
        load_menu("egg")
    })
}