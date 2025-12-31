async function addTarget() {
    const host = document.getElementById('hostInput').value.trim();
    const port = parseInt(document.getElementById('portInput').value, 10);
    const key = document.getElementById('keyInput').value.trim();
    if (!host || !port) {
        alert('Host and port are required');
        return;
    }
    const url = `/api/targets?host=${encodeURIComponent(host)}&port=${encodeURIComponent(port)}${key ? `&key=${encodeURIComponent(key)}` : ''}`;
    const resp = await fetchWithAuth(url, { method: 'POST' });
    if (resp && resp.ok) {
        document.getElementById('hostInput').value = '';
        document.getElementById('portInput').value = '';
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

async function refresh() {
    const resp = await fetchWithAuth('/api/targets');
    if (!resp || !resp.ok) return;
    const data = await resp.json();
    const tbody = document.getElementById('targetsBody');
    tbody.innerHTML = '';
    data.forEach(t => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${t.id}</td>
            <td>${t.host}</td>
            <td>${t.port}</td>
            <td>${t.key || ''}</td>
            <td>${t.created_at || ''}</td>
            <td><button class="btn" onclick="deleteTarget(${t.id})">Delete</button></td>
        `;
        tbody.appendChild(tr);
    });
}

refresh();