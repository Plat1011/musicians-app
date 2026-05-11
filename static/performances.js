requireAuth();

const tbody = document.getElementById("perf-tbody");
const dialog = document.getElementById("form-dialog");
const form = document.getElementById("perf-form");
const formMsg = document.getElementById("form-msg");

const isAdmin = (currentUser() || {}).role === "admin";
if (isAdmin) {
    document.getElementById("admin-tools").style.display = "block";
}

async function load() {
    const r = await api("/api/performances");
    if (!r) return;
    const list = await r.json();
    tbody.innerHTML = "";
    for (const p of list) {
        const tr = document.createElement("tr");
        tr.innerHTML =
            "<td>" + p.id + "</td>" +
            "<td>" + esc(p.musician_name) + "</td>" +
            "<td>" + esc(p.concert_title) + "</td>" +
            "<td>" + esc(p.concert_date || "") + "</td>" +
            "<td>" + esc(p.instrument_name || "") + "</td>" +
            "<td>" + (p.fee != null ? p.fee : "") + "</td>" +
            "<td class='row-actions'></td>";
        if (isAdmin) {
            const del = document.createElement("button");
            del.textContent = "Удалить";
            del.className = "danger";
            del.addEventListener("click", () => removeItem(p.id));
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

async function fillSelects() {
    const [mr, cr, ir] = await Promise.all([
        api("/api/musicians"),
        api("/api/concerts"),
        api("/api/instruments"),
    ]);
    if (!mr || !cr || !ir) return;
    const ms = await mr.json();
    const cs = await cr.json();
    const is = await ir.json();
    const musicianSel = form.musician_id;
    const concertSel = form.concert_id;
    const instrSel = form.instrument_id;
    musicianSel.innerHTML = "";
    concertSel.innerHTML = "";
    instrSel.innerHTML = '<option value="">–</option>';
    ms.forEach((m) => musicianSel.add(new Option(m.name, m.id)));
    cs.forEach((c) => concertSel.add(new Option(c.title + " (" + (c.concert_date || "") + ")", c.id)));
    is.forEach((i) => instrSel.add(new Option(i.name, i.id)));
}

if (isAdmin) {
    document.getElementById("add-btn").addEventListener("click", async () => {
        formMsg.textContent = "";
        form.reset();
        await fillSelects();
        dialog.showModal();
    });
}

document.getElementById("cancel-btn").addEventListener("click", () => dialog.close());

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const fd = new FormData(form);
    const body = {
        musician_id: Number(fd.get("musician_id")),
        concert_id: Number(fd.get("concert_id")),
        instrument_id: fd.get("instrument_id") ? Number(fd.get("instrument_id")) : null,
        fee: fd.get("fee") ? Number(fd.get("fee")) : null,
    };
    const r = await api("/api/performances", { method: "POST", body });
    if (!r) return;
    if (r.ok) {
        dialog.close();
        load();
    } else {
        const data = await r.json();
        formMsg.textContent = data.error || "Ошибка";
    }
});

async function removeItem(id) {
    if (!confirm("Удалить выступление?")) return;
    const r = await api("/api/performances/" + id, { method: "DELETE" });
    if (r && r.ok) load();
}

load();
