async function log_in(username, password) {
    const headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    const data = `grant_type=&username=${username}&password=${password}&scope=&client_id=&client_secret=`
    try {
        let response = await axios.post("http://127.0.0.1:8000/auth/token", data, {
            headers: headers
        })
        if ("access_token" in response.data) {
            localStorage.setItem('access_token', response.data['access_token'])
            localStorage.setItem('authorized', true)
            localStorage.setItem('username', username)
            return { 'authorized': true }
        }
        else if ("detail" in response.data) {
            return { 'authorized': false, 'detail': response.data['detail'] }
        }
        else if ("detail" in response.data) {
            return { 'authorized': false, 'detail': 'Ошибка при авторизации' }
        }

    }
    catch (err) {
        if ("detail" in err.response.data)
            return { 'authorized': false, 'detail': err.response.data['detail'] }
    }
}

function is_authorized() {
    if (!localStorage.getItem('authorized')) {
        window.location.href = "http://127.0.0.1:8000/auth";
    }
}

function get_config() {
    if (localStorage.getItem('authorized')) {
        return {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
        }
    }
}

function log_out() {
    localStorage.clear()
    window.location.href = "http://127.0.0.1:8000/auth";
}

function check_status(error) {
    if ('response' in error && error.response.status == 401) {
        log_out()
    }
}