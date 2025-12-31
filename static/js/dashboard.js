async function refresh() {
    const resp = await fetchWithAuth('/api/targets/status');
    if (!resp || !resp.ok) return;
    const items = await resp.json();

    const grid = document.getElementById('cardsGrid');
    const empty = document.getElementById('emptyState');
    grid.innerHTML = '';

    if (!items || items.length === 0) {
        empty.style.display = 'block';
        return;
    }
    empty.style.display = 'none';

    items.forEach(it => {
        const info = (it.details && it.details.info) || {};
        const appName = pick(it.details, 'app_name') || pick(info, 'appName', 'app_name') || 'Unknown';
        const instanceId = pick(info, 'instanceId', 'instance_id') || pick(it.details, 'instance_id');
        const statusText = it.healthy ? 'HEALTHY' : 'DOWN';
        const statusClass = it.healthy ? 'green' : 'red';
        const host = it.host;
        const port = it.port;
        const uptimeRaw = pick(it.details, 'uptime') || pick(info, 'uptime');
        const uptime = formatUptime(uptimeRaw);

        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
            <div class="card-header">
                <div class="title">${appName}</div>
                <div class="badge ${statusClass}">${statusText}</div>
            </div>
            <div class="row"><div class="pill">Instance: ${instanceId || '-'}</div></div>
            <div class="row">
                <div class="pill">Host: ${host}</div>
                <div class="pill">Port: ${port}</div>
            </div>
            <div class="row">
                <div class="pill">Uptime: ${uptime || '-'}</div>
            </div>
            <div class="meta">${it.status_code || ''}</div>
        `;
        grid.appendChild(card);
    });
}

refresh();
setInterval(refresh, 5000);