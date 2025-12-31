async function fetchWithAuth(url, opts) {
    const resp = await fetch(url, opts);
    if (resp.status === 401) {
        window.location.href = '/';
        return null;
    }
    return resp;
}

async function logout() {
    await fetch('/logout', { method: 'POST' });
    window.location.reload();
}

// format seconds -> Xd Yh Zm Ts
function formatUptime(value) {
    if (value === undefined || value === null || value === '') return '';
    let sec = Number(value);
    if (Number.isNaN(sec)) return String(value);
    const d = Math.floor(sec / 86400); sec %= 86400;
    const h = Math.floor(sec / 3600); sec %= 3600;
    const m = Math.floor(sec / 60); const s = Math.floor(sec % 60);
    const parts = [];
    if (d) parts.push(`${d}d`);
    if (h) parts.push(`${h}h`);
    if (m) parts.push(`${m}m`);
    parts.push(`${s}s`);
    return parts.join(' ');
}

function pick(obj, ...keys) {
    for (const k of keys) {
        if (obj && obj[k] !== undefined) return obj[k];
    }
    return undefined;
}