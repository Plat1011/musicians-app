requireAuth();

const tbody = document.getElementById("musicians-tbody");
const dialog = document.getElementById("form-dialog");
const form = document.getElementById("musician-form");
const formMsg = document.getElementById("form-msg");
const formTitle = document.getElementById("form-title");

const isAdmin = (currentUser() || {}).role === "admin";
if (isAdmin) {
    document.getElementById("admin-tools").style.display = "block";
}

async function load() {
    const r = await api("/api/musicians");
    if (!r) return;
    const list = await r.json();
    tbody.innerHTML = "";
    for (const m of list) {
        const tr = document.createElement("tr");
        tr.innerHTML =
            "<td>" + m.id + "</td>" +
            "<td>" + escape(m.name) + "</td>" +
            "<td>" + escape(m.country || "") + "</td>" +
            "<td>" + (m.birth_year || "") + "</td>" +
            "<td>" + escape(m.bio || "") + "</td>" +
            "<td class='row-actions'></td>";
        if (isAdmin) {
            const actions = tr.lastElementChild;
            const edit = document.createElement("button");
            edit.textContent = "Изменить";
            edit.addEventListener("click", () => openForm(m));
            const del = document.createElement("button");
            del.textContent = "Удалить";
            del.className = "danger";
            del.addEventListener("click", () => removeItem(m.id));
            actions.append(edit, del);
        }
        tbody.appendChild(tr);
    }
}

function escape(s) {
    return String(s)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;");
}

function openForm(m) {
    formMsg.textContent = "";
    if (m) {
        formTitle.textContent = "Изменить музыканта";
        form.id.value = m.id;
        form.name.value = m.name;
        form.country.value = m.country || "";
        form.birth_year.value = m.birth_year || "";
        form.bio.value = m.bio || "";
    } else {
        formTitle.textContent = "Новый музыкант";
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
        name: fd.get("name"),
        country: fd.get("country") || null,
        birth_year: fd.get("birth_year") ? Number(fd.get("birth_year")) : null,
        bio: fd.get("bio") || null,
    };
    const id = fd.get("id");
    const r = await api(id ? "/api/musicians/" + id : "/api/musicians", {
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
    if (!confirm("Удалить музыканта?")) return;
    const r = await api("/api/musicians/" + id, { method: "DELETE" });
    if (r && r.ok) load();
}

load();
