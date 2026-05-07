requireAuth();

const tbody = document.getElementById("instr-tbody");
const form = document.getElementById("add-form");
const formMsg = document.getElementById("form-msg");

const isAdmin = (currentUser() || {}).role === "admin";
if (isAdmin) {
    document.getElementById("admin-tools").style.display = "block";
}

async function load() {
    const r = await api("/api/instruments");
    if (!r) return;
    const list = await r.json();
    tbody.innerHTML = "";
    for (const i of list) {
        const tr = document.createElement("tr");
        tr.innerHTML =
            "<td>" + i.id + "</td>" +
            "<td>" + esc(i.name) + "</td>" +
            "<td>" + esc(i.kind || "") + "</td>" +
            "<td class='row-actions'></td>";
        if (isAdmin) {
            const del = document.createElement("button");
            del.textContent = "Удалить";
            del.className = "danger";
            del.addEventListener("click", () => removeItem(i.id));
            tr.lastElementChild.appendChild(del);
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

if (isAdmin) {
    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const fd = new FormData(form);
        const body = { name: fd.get("name"), kind: fd.get("kind") || null };
        const r = await api("/api/instruments", { method: "POST", body });
        if (!r) return;
        if (r.ok) {
            form.reset();
            formMsg.textContent = "";
            load();
        } else {
            const data = await r.json();
            formMsg.textContent = data.error || "Ошибка";
        }
    });
}

async function removeItem(id) {
    if (!confirm("Удалить инструмент?")) return;
    const r = await api("/api/instruments/" + id, { method: "DELETE" });
    if (r && r.ok) load();
}

load();
