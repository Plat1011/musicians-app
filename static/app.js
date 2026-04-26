const TOKEN_KEY = "ma_token";
const USER_KEY = "ma_user";

function saveSession(token, user) {
    localStorage.setItem(TOKEN_KEY, token);
    localStorage.setItem(USER_KEY, JSON.stringify(user));
}

function getToken() {
    return localStorage.getItem(TOKEN_KEY);
}

function clearSession() {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
}

function currentUser() {
    const v = localStorage.getItem(USER_KEY);
    return v ? JSON.parse(v) : null;
}

function logout() {
    clearSession();
    location.href = "/login";
}

function requireAuth() {
    if (!getToken()) {
        location.href = "/login";
    }
}

async function api(path, options = {}) {
    const headers = options.headers || {};
    const token = getToken();
    if (token) headers["Authorization"] = "Bearer " + token;
    if (options.body && typeof options.body !== "string") {
        headers["Content-Type"] = "application/json";
        options.body = JSON.stringify(options.body);
    }
    const r = await fetch(path, { ...options, headers });
    if (r.status === 401) {
        clearSession();
        location.href = "/login";
        return null;
    }
    return r;
}

function renderNav() {
    const nav = document.getElementById("nav");
    if (!nav) return;
    if (getToken()) {
        const u = currentUser();
        nav.innerHTML =
            '<a href="/">Главная</a>' +
            '<a href="/musicians">Музыканты</a>' +
            '<a href="/concerts">Концерты</a>' +
            '<a href="/performances">Выступления</a>' +
            '<button onclick="logout()">Выйти</button>';
    } else {
        nav.innerHTML = '<a href="/login">Вход</a>';
    }
}

document.addEventListener("DOMContentLoaded", renderNav);
