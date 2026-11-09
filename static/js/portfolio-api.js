function escapeHtml(value) {
    return String(value ?? '').replaceAll('&', '&amp;').replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;').replaceAll('"', '&quot;').replaceAll("'", '&#39;');
}

function safePortfolioUrl(value) {
    if (!value) return '';
    try {
        const url = new URL(value, window.location.origin);
        return ['http:', 'https:'].includes(url.protocol) ? url.href : '';
    } catch { return ''; }
}

function getCookie(name) {
    const prefix = `${name}=`;
    const cookie = document.cookie.split(';').map(value => value.trim()).find(value => value.startsWith(prefix));
    return cookie ? decodeURIComponent(cookie.slice(prefix.length)) : '';
}

function initPortfolioApi(config) {
    const grid = document.getElementById(config.grid);
    const search = document.getElementById(config.search);
    const form = document.getElementById(config.form);
    const editForm = config.editForm ? document.getElementById(config.editForm) : null;
    let controller;
    let timer;

    function showState(state) {
        for (const key of ['loading', 'error', 'empty', 'grid']) {
            document.getElementById(config[key]).classList.toggle('hide', key !== state);
        }
    }

    async function fetchResources(query = search.value.trim()) {
        controller?.abort();
        controller = new AbortController();
        const current = controller;
        showState('loading');
        try {
            const url = new URL(config.list, window.location.origin);
            if (query) url.searchParams.set('title', query);
            const response = await fetch(url, {headers: {Accept: 'application/json'}, signal: current.signal});
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            const data = await response.json();
            if (current.signal.aborted) return;
            grid.replaceChildren(...data.map(config.buildCard));
            showState(data.length ? 'grid' : 'empty');
        } catch (error) {
            if (error.name !== 'AbortError') showState('error');
        }
    }

    async function writeResource(url, method, payload) {
        const response = await fetch(url, {
            method, headers: {Accept: 'application/json', 'Content-Type': 'application/json',
                              'X-CSRFToken': getCookie('csrftoken')},
            body: payload === undefined ? undefined : JSON.stringify(payload),
        });
        if (response.ok && response.status === 204) return null;
        const data = await response.json().catch(() => ({}));
        if (!response.ok) {
            const messages = Object.values(data || {}).flat().filter(value => typeof value === 'string');
            throw new Error(messages.join(' ') || `Permintaan gagal (HTTP ${response.status}).`);
        }
        return data;
    }

    async function submitResource(event, targetForm, modal, url, method, message) {
        event.preventDefault();
        const button = targetForm.querySelector('button[type="submit"]');
        if (button.disabled) return;
        button.disabled = true;
        try {
            const fields = new FormData(targetForm);
            const payload = Object.fromEntries(config.fields.map(name => [name, fields.get(name)]));
            if (config.checkbox) payload[config.checkbox] = fields.has(config.checkbox);
            await writeResource(url, method, payload);
            targetForm.reset();
            document.getElementById(modal).hidePopover();
            showToast('Berhasil', message, 'success');
            await fetchResources();
        } catch (error) {
            showToast('Belum berhasil', error.message, 'error');
        } finally { button.disabled = false; }
    }

    form?.addEventListener('submit', event => {
        submitResource(event, form, config.modal, config.list, 'POST', config.createdMessage);
    });
    editForm?.addEventListener('submit', event => {
        const url = config.detail.replace(config.placeholder, editForm.dataset.id);
        submitResource(event, editForm, config.editModal, url, 'PATCH', config.updatedMessage);
    });

    grid.addEventListener('click', async event => {
        const button = event.target.closest('button[data-action]');
        if (!button || button.disabled) return;
        const action = button.dataset.action;
        if (!['star', 'delete', 'edit'].includes(action)) return;
        if (action === 'delete' && !window.confirm(config.deleteMessage)) return;
        button.disabled = true;
        try {
            if (action === 'edit' && editForm) {
                const url = config.detail.replace(config.placeholder, button.dataset.id);
                const response = await fetch(url, {headers: {Accept: 'application/json'}});
                const data = await response.json().catch(() => ({}));
                if (!response.ok) throw new Error(data.detail || `Permintaan gagal (HTTP ${response.status}).`);
                editForm.reset();
                editForm.dataset.id = button.dataset.id;
                for (const field of config.fields) editForm.elements.namedItem(field).value = data[field] ?? '';
                if (config.checkbox) editForm.elements.namedItem(config.checkbox).checked = data[config.checkbox];
                const modal = document.getElementById(config.editModal);
                modal.showPopover();
                modal.querySelector('.project-form-modal__content').scrollTop = 0;
                editForm.elements.namedItem(config.fields[0]).focus({preventScroll: true});
                return;
            }
            const pattern = action === 'star' ? config.star : config.detail;
            await writeResource(pattern.replace(config.placeholder, button.dataset.id), action === 'star' ? 'POST' : 'DELETE');
            showToast('Berhasil', action === 'star' ? 'Star berhasil diperbarui.' : 'Data berhasil dihapus.', 'success');
            await fetchResources();
        } catch (error) {
            showToast('Belum berhasil', error.message, 'error');
        } finally { button.disabled = false; }
    });

    search.addEventListener('input', () => {
        clearTimeout(timer);
        timer = setTimeout(() => fetchResources(), 300);
    });
    document.getElementById(config.searchForm).addEventListener('submit', event => {
        event.preventDefault();
        clearTimeout(timer);
        fetchResources();
    });
    fetchResources();
    return {fetchResources, writeResource};
}
