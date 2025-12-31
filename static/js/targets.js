let dragSrcEl = null;

function makeRowDraggable(tr) {
    tr.draggable = true;
    tr.addEventListener('dragstart', (e) => {
        dragSrcEl = tr;
        e.dataTransfer.effectAllowed = 'move';
        tr.style.opacity = '0.5';
    });
    tr.addEventListener('dragend', () => {
        tr.style.opacity = '';
    });
    tr.addEventListener('dragover', (e) => {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'move';
    });
    tr.addEventListener('drop', async (e) => {
        e.stopPropagation();
        if (dragSrcEl && dragSrcEl !== tr) {
            const tbody = document.getElementById('targetsBody');
            const rows = Array.from(tbody.children);
            const srcIndex = rows.indexOf(dragSrcEl);
            const dstIndex = rows.indexOf(tr);
            if (srcIndex >= 0 && dstIndex >= 0) {
                if (srcIndex < dstIndex) {
                    tbody.insertBefore(dragSrcEl, tr.nextSibling);
                } else {
                    tbody.insertBefore(dragSrcEl, tr);
                }
                await persistOrder();
            }
        }
    });
}

async function persistOrder() {
    const tbody = document.getElementById('targetsBody');
    const ids = Array.from(tbody.children).map(r => Number(r.dataset.id));
    const resp = await fetchWithAuth('/api/targets/reorder', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ order: ids })
    });
    if (!resp || !resp.ok) {
        alert('Failed to reorder targets');
    }
}

async function addTarget() {
    const host = document.getElementById('hostInput').value.trim();
    const port = parseInt(document.getElementById('portInput').value, 10);
    const appName = document.getElementById('appNameInput').value.trim();
    const key = document.getElementById('keyInput').value.trim();
    if (!host || !port) {
        alert('Host and port are required');
        return;
    }
    const url = `/api/targets?host=${encodeURIComponent(host)}&port=${encodeURIComponent(port)}${key ? `&key=${encodeURIComponent(key)}` : ''}${appName ? `&app_name=${encodeURIComponent(appName)}` : ''}`;
    const resp = await fetchWithAuth(url, { method: 'POST' });
    if (resp && resp.ok) {
        document.getElementById('hostInput').value = '';
        document.getElementById('portInput').value = '';
        document.getElementById('appNameInput').value = '';
        document.getElementById('keyInput').value = '';
        refresh();
    } else {
        alert('Failed to add target');
    }
}

async function deleteTarget(id) {
    const resp = await fetchWithAuth(`/api/targets/${id}`, { method: 'DELETE' });
    if (resp && resp.ok) {
        refresh();
    } else {
        alert('Failed to delete target');
    }
}

async function editTarget(id) {
    const row = document.querySelector(`tr[data-id="${id}"]`);
    if (!row) return;
    const hostEl = row.querySelector('.host');
    const portEl = row.querySelector('.port');
    const appEl = row.querySelector('.app');
    const keyEl = row.querySelector('.key');
    const actions = row.querySelector('.actions');

    const host = hostEl.textContent;
    const port = portEl.textContent;
    const appName = appEl.textContent;
    const key = keyEl.textContent;

    hostEl.innerHTML = `<input value="${host}">`;
    portEl.innerHTML = `<input type="number" value="${port}">`;
    appEl.innerHTML = `<input value="${appName}">`;
    keyEl.innerHTML = `<input value="${key}">`;

    actions.innerHTML = `
        <button class="action-btn" onclick="saveTarget(${id})">Save</button>
        <button class="action-btn" onclick="cancelEdit(${id}, '${host}', '${port}', '${appName}', '${key}')">Cancel</button>
    `;
}

async function saveTarget(id) {
    const row = document.querySelector(`tr[data-id="${id}"]`);
    const host = row.querySelector('.host input').value.trim();
    const port = parseInt(row.querySelector('.port input').value, 10);
    const appName = row.querySelector('.app input').value.trim();
    const key = row.querySelector('.key input').value.trim();

    const params = new URLSearchParams();
    if (host) params.append('host', host);
    if (!Number.isNaN(port)) params.append('port', String(port));
    params.append('app_name', appName);
    params.append('key', key);

    const resp = await fetchWithAuth(`/api/targets/${id}?` + params.toString(), { method: 'PUT' });
    if (resp && resp.ok) {
        refresh();
    } else {
        alert('Failed to save target');
    }
}

function cancelEdit(id, host, port, appName, key) {
    const row = document.querySelector(`tr[data-id="${id}"]`);
    row.querySelector('.host').textContent = host;
    row.querySelector('.port').textContent = port;
    row.querySelector('.app').textContent = appName;
    row.querySelector('.key').textContent = key;
    row.querySelector('.actions').innerHTML = `
        <button class="action-btn" onclick="editTarget(${id})">Edit</button>
        <button class="action-btn" onclick="deleteTarget(${id})">Delete</button>
    `;
}

async function refresh() {
    const resp = await fetchWithAuth('/api/targets');
    if (!resp || !resp.ok) return;
    const data = await resp.json();
    const tbody = document.getElementById('targetsBody');
    tbody.innerHTML = '';
    data.forEach(t => {
        const tr = document.createElement('tr');
        tr.dataset.id = t.id;
        tr.innerHTML = `
            <td>${t.id}</td>
            <td class="host">${t.host}</td>
            <td class="port">${t.port}</td>
            <td class="app">${t.app_name || ''}</td>
            <td class="key">${t.key || ''}</td>
            <td>${t.created_at || ''}</td>
            <td class="actions">
                <button class="action-btn" onclick="editTarget(${t.id})">Edit</button>
                <button class="action-btn" onclick="deleteTarget(${t.id})">Delete</button>
            </td>
        `;
        makeRowDraggable(tr);
        tbody.appendChild(tr);
    });
}

refresh();