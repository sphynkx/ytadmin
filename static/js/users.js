let usersData = [];
let columns = [];
let sortState = { column: null, asc: true };

function isLongField(col) {
    return /password|hash|token|secret|key/i.test(col);
}

function isDateField(col) {
    return /(_at|date|time|timestamp)$/i.test(col);
}

function tryParseDate(value) {
    if (value === null || value === undefined) return null;

    if (typeof value === 'number') {
        const ms = value > 1e12 ? value : (value * 1000);
        const d = new Date(ms);
        return isNaN(d.getTime()) ? null : d;
    }

    if (typeof value === 'string') {
        const parsed = Date.parse(value);
        if (!isNaN(parsed)) {
            return new Date(parsed);
        }
    }
    return null;
}

function formatDateTime(value) {
    const d = tryParseDate(value);
    if (!d) {
        return (value === null || value === undefined) ? '' : String(value);
    }
    const pad = (n) => String(n).padStart(2, '0');
    const yyyy = d.getFullYear();
    const mm = pad(d.getMonth() + 1);
    const dd = pad(d.getDate());
    const HH = pad(d.getHours());
    const MM = pad(d.getMinutes());
    const SS = pad(d.getSeconds());
    return `${yyyy}-${mm}-${dd} ${HH}:${MM}:${SS}`;
}

function formatCell(col, value) {
    if (isDateField(col)) {
        return formatDateTime(value);
    }
    return (value === null || value === undefined) ? '' : String(value);
}

function renderHeader() {
    const thead = document.getElementById('usersHead');
    thead.innerHTML = '';
    const tr = document.createElement('tr');

    columns.forEach(col => {
        const th = document.createElement('th');
        th.textContent = col;
        th.classList.add('sortable');
        if (sortState.column === col) {
            th.classList.add(sortState.asc ? 'sort-asc' : 'sort-desc');
        }
        th.addEventListener('click', () => {
            if (sortState.column === col) {
                sortState.asc = !sortState.asc;
            } else {
                sortState.column = col;
                sortState.asc = true;
            }
            renderBody();
            renderHeader();
        });
        tr.appendChild(th);
    });

    thead.appendChild(tr);
}

function compareValues(a, b, col) {
    const va = a[col];
    const vb = b[col];

    const aEmpty = (va === null || va === undefined);
    const bEmpty = (vb === null || vb === undefined);
    if (aEmpty && bEmpty) return 0;
    if (aEmpty) return 1;
    if (bEmpty) return -1;

    if (isDateField(col)) {
        const da = tryParseDate(va);
        const db = tryParseDate(vb);
        if (da && db) return da.getTime() - db.getTime();
    }

    const na = Number(va);
    const nb = Number(vb);
    const bothNumeric = !Number.isNaN(na) && !Number.isNaN(nb) && typeof va !== 'string' && typeof vb !== 'string';
    if (bothNumeric) {
        return na - nb;
    }

    return String(va).localeCompare(String(vb), undefined, { sensitivity: 'base' });
}

function renderBody() {
    const tbody = document.getElementById('usersBody');
    tbody.innerHTML = '';

    let data = [...usersData];
    if (sortState.column) {
        data.sort((a, b) => {
            const r = compareValues(a, b, sortState.column);
            return sortState.asc ? r : -r;
        });
    }

    data.forEach(row => {
        const tr = document.createElement('tr');
        columns.forEach(col => {
            const td = document.createElement('td');

            const text = formatCell(col, row[col]);

            if (isLongField(col)) {
                const div = document.createElement('div');
                div.className = 'cell-scroll';
                div.textContent = text;
                td.appendChild(div);
            } else {
                td.textContent = text;
            }

            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });
}

async function refreshUsers() {
    const resp = await fetchWithAuth('/api/app/users');
    if (!resp || !resp.ok) return;
    const data = await resp.json();

    const empty = document.getElementById('usersEmpty');
    const table = document.getElementById('usersTable');

    if (!Array.isArray(data) || data.length === 0) {
        table.style.display = 'none';
        empty.style.display = 'block';
        const thead = document.getElementById('usersHead');
        const tbody = document.getElementById('usersBody');
        thead.innerHTML = '';
        tbody.innerHTML = '';
        return;
    }

    empty.style.display = 'none';
    table.style.display = 'table';

    usersData = data;
    columns = Object.keys(data[0]);

    renderHeader();
    renderBody();
}

refreshUsers();