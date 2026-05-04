requireAuth();

const tbody = document.getElementById("concerts-tbody");
const dialog = document.getElementById("form-dialog");
const form = document.getElementById("concert-form");
const formMsg = document.getElementById("form-msg");
const formTitle = document.getElementById("form-title");

const isAdmin = (currentUser() || {}).role === "admin";
if (isAdmin) {
    document.getElementById("admin-tools").style.display = "block";
}

async function load() {
    const r = await api("/api/concerts");
    if (!r) return;
    const list = await r.json();
    tbody.innerHTML = "";
    for (const c of list) {
        const tr = document.createElement("tr");
        tr.innerHTML =
            "<td>" + c.id + "</td>" +
            "<td>" + esc(c.title) + "</td>" +
            "<td>" + esc(c.concert_date || "") + "</td>" +
            "<td>" + esc(c.venue || "") + "</td>" +
            "<td>" + esc(c.city || "") + "</td>" +
            "<td class='row-actions'></td>";
        if (isAdmin) {
            const actions = tr.lastElementChild;
            const edit = document.createElement("button");
            edit.textContent = "Изменить";
            edit.addEventListener("click", () => openForm(c));
            const del = document.createElement("button");
            del.textContent = "Удалить";
            del.className = "danger";
            del.addEventListener("click", () => removeItem(c.id));
            actions.append(edit, del);
        }
        tbody.appendChild(tr);
    }
}

function esc(s) {
    return String(s)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;");
}

function openForm(c) {
    formMsg.textContent = "";
    if (c) {
        formTitle.textContent = "Изменить концерт";
        form.id.value = c.id;
        form.title.value = c.title;
        form.concert_date.value = c.concert_date || "";
        form.venue.value = c.venue || "";
        form.city.value = c.city || "";
    } else {
        formTitle.textContent = "Новый концерт";
        form.reset();
        form.id.value = "";
    }
    dialog.showModal();
}

document.getElementById("cancel-btn").addEventListener("click", () => dialog.close());
if (isAdmin) {
    document.getElementById("add-btn").addEventListener("click", () => openForm(null));
}

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const fd = new FormData(form);
    const body = {
        title: fd.get("title"),
        concert_date: fd.get("concert_date"),
        venue: fd.get("venue") || null,
        city: fd.get("city") || null,
    };
    const id = fd.get("id");
    const r = await api(id ? "/api/concerts/" + id : "/api/concerts", {
        method: id ? "PUT" : "POST",
        body,
    });
    if (!r) return;
    if (r.ok) {
        dialog.close();
        load();
    } else {
        const data = await r.json();
        formMsg.textContent = data.error || "Ошибка валидации";
    }
});

async function removeItem(id) {
    if (!confirm("Удалить концерт?")) return;
    const r = await api("/api/concerts/" + id, { method: "DELETE" });
    if (r && r.ok) load();
}

load();
