// app.js — Frontend do Promptograph
// "Photograph every system prompt that matters."
// https://github.com/4pixeltechBR/promptograph
// SPA pura em vanilla JS, consome a API em /api/*

const $ = (s) => document.querySelector(s);
const $$ = (s) => document.querySelectorAll(s);

const state = {
    index: [],
    filtered: [],
    selected: null,
    view: 'browse', // browse | diff | validate | generate
};

// ============ Init ============
async function init() {
    try {
        const res = await fetch('/api/index');
        state.index = await res.json();
        state.filtered = state.index;
        renderNav();
        renderBrowse();
        renderGenerate();
    } catch (e) {
        console.error('Init failed:', e);
        $('#content').innerHTML = `
            <div class="v-summary" style="border-color: #f59e0b; text-align: left;">
                <h3>⚠️ Backend API not available</h3>
                <p class="v-verdict" style="text-align: left;">This is a <strong>static preview</strong> of <strong>Promptograph v0.3.0</strong>'s UI. The interactive features (browse <strong>20,475+</strong> prompts across <strong>55</strong> repos, diff, validate, generate) require the Python backend running.</p>
                <p style="text-align: left; margin-top: 12px;"><strong>To enable full features:</strong></p>
                <pre style="text-align: left;">git clone https://github.com/4pixeltechBR/promptograph.git
cd promptograph
python3 server.py 8765
# Then open http://localhost:8765</pre>
                <p style="text-align: left; margin-top: 12px;">Or use Docker:</p>
                <pre style="text-align: left;">docker build -t promptograph .
docker run -p 8765:8765 promptograph</pre>
            </div>
        `;
    }
}

// ============ Navegação ============
function renderNav() {
    const nav = $('#nav');
    nav.innerHTML = `
        <button data-view="browse" class="active">📚 Browse (${state.index.length})</button>
        <button data-view="diff">🔀 Diff</button>
        <button data-view="validate">✅ Validate</button>
        <button data-view="generate">✨ Generate</button>
    `;
    nav.querySelectorAll('button').forEach(btn => {
        btn.addEventListener('click', () => switchView(btn.dataset.view));
    });
}

function switchView(view) {
    state.view = view;
    $$('#nav button').forEach(b => b.classList.toggle('active', b.dataset.view === view));
    if (view === 'browse') renderBrowse();
    else if (view === 'diff') renderDiff();
    else if (view === 'validate') renderValidate();
    else if (view === 'generate') renderGenerate();
}

// ============ Browse ============
function renderBrowse() {
    const c = $('#content');
    c.innerHTML = `
        <h2>📚 Browse System Prompts</h2>
        <div class="filters">
            <input id="search" placeholder="🔍 Search by name, model, file..." />
            <select id="company"><option value="">All companies</option></select>
            <select id="sort">
                <option value="tokens">Sort by size</option>
                <option value="date">Sort by date</option>
                <option value="name">Sort by name</option>
            </select>
            <span class="count">${state.filtered.length} prompts</span>
        </div>
        <div class="browse-grid">
            <div id="list" class="list"></div>
            <div id="detail" class="detail">
                <p class="muted">← Select a prompt to see details</p>
            </div>
        </div>
    `;

    // Popula companies
    const companies = [...new Set(state.index.map(p => p.company))].sort();
    const companySel = $('#company');
    companies.forEach(c => {
        const opt = document.createElement('option');
        opt.value = c; opt.textContent = c;
        companySel.appendChild(opt);
    });

    // Listeners
    $('#search').addEventListener('input', applyFilters);
    $('#company').addEventListener('change', applyFilters);
    $('#sort').addEventListener('change', applyFilters);
    applyFilters();
}

function applyFilters() {
    const q = ($('#search').value || '').toLowerCase();
    const company = $('#company').value;
    const sort = $('#sort').value;
    let result = state.index.filter(p => {
        if (company && p.company !== company) return false;
        if (q) {
            const hay = (p.filename + ' ' + p.path + ' ' + p.model + ' ' + (p.persona || '')).toLowerCase();
            if (!hay.includes(q)) return false;
        }
        return true;
    });
    if (sort === 'tokens') result.sort((a, b) => b.tokens_estimate - a.tokens_estimate);
    else if (sort === 'date') result.sort((a, b) => (b.date || '').localeCompare(a.date || ''));
    else if (sort === 'name') result.sort((a, b) => a.filename.localeCompare(b.filename));
    state.filtered = result.slice(0, 500);  // Limita
    renderList();
}

function renderList() {
    const list = $('#list');
    list.innerHTML = state.filtered.map(p => `
        <div class="item" data-id="${p.id}">
            <div class="item-title">${escapeHtml(p.filename)}</div>
            <div class="item-meta">
                <span class="badge">${p.company}</span>
                ${p.model !== 'unknown' ? `<span class="badge model">${escapeHtml(p.model)}</span>` : ''}
                <span class="meta">${p.tokens_estimate.toLocaleString()} tokens</span>
            </div>
        </div>
    `).join('');
    list.querySelectorAll('.item').forEach(el => {
        el.addEventListener('click', () => showDetail(el.dataset.id));
    });
}

async function showDetail(id) {
    const p = state.index.find(x => x.id === id);
    if (!p) return;
    state.selected = p;
    $$('#list .item').forEach(el => el.classList.toggle('active', el.dataset.id === id));
    const d = $('#detail');
    d.innerHTML = `
        <h3>${escapeHtml(p.filename)}</h3>
        <div class="detail-meta">
            <p><strong>Path:</strong> <code>${escapeHtml(p.path)}</code></p>
            <p><strong>Company:</strong> ${p.company} &nbsp; <strong>Model:</strong> ${escapeHtml(p.model)}</p>
            <p><strong>Size:</strong> ${p.tokens_estimate.toLocaleString()} tokens (${p.lines.toLocaleString()} lines, ${(p.size_bytes/1024).toFixed(1)}KB)</p>
            <p><strong>XML tags:</strong> ${p.xml_tags.length} ${p.xml_tags.length > 0 ? '(' + p.xml_tags.slice(0, 12).map(escapeHtml).join(', ') + ')' : ''}</p>
            <p><strong>Tools detected:</strong> ${p.tools.length > 0 ? p.tools.map(escapeHtml).join(', ') : 'none'}</p>
            ${p.persona ? `<p><strong>Persona:</strong> <em>${escapeHtml(p.persona)}</em></p>` : ''}
        </div>
        <div class="actions">
            <button id="view-raw">📄 View raw</button>
            <button id="copy-btn">📋 Copy path</button>
            <button id="add-diff">+ Add to diff</button>
            <button id="validate-btn">✅ Validate</button>
        </div>
        <pre id="raw-content" style="display:none">Loading...</pre>
    `;
    $('#view-raw').addEventListener('click', async () => {
        const raw = $('#raw-content');
        if (raw.style.display === 'none') {
            raw.textContent = 'Loading...';
            raw.style.display = 'block';
            const r = await fetch('/api/raw?id=' + encodeURIComponent(p.id));
            const j = await r.json();
            raw.textContent = j.content || 'Not found';
        } else raw.style.display = 'none';
    });
    $('#copy-btn').addEventListener('click', () => {
        navigator.clipboard.writeText(p.path);
        event.target.textContent = '✓ Copied!';
        setTimeout(() => event.target.textContent = '📋 Copy path', 1500);
    });
    $('#add-diff').addEventListener('click', () => addToDiff(p));
    $('#validate-btn').addEventListener('click', () => validatePrompt(p));
}

// ============ Diff ============
const diffList = [];
function renderDiff() {
    const c = $('#content');
    c.innerHTML = `
        <h2>🔀 Compare two system prompts</h2>
        <p class="muted">Click "+ Add to diff" em um prompt do Browse, ou adicione aqui:</p>
        <div class="diff-pickers">
            <select id="diff-a"><option value="">— select left —</option></select>
            <span>vs</span>
            <select id="diff-b"><option value="">— select right —</option></select>
            <button id="run-diff">Run diff</button>
        </div>
        <div id="diff-output"></div>
    `;
    const opts = state.index.slice(0, 1000).map(p => `<option value="${p.id}">${escapeHtml(p.filename)} [${p.tokens_estimate}t]</option>`).join('');
    $('#diff-a').innerHTML += opts;
    $('#diff-b').innerHTML += opts;
    $('#run-diff').addEventListener('click', runDiff);
}

async function runDiff() {
    const a = $('#diff-a').value;
    const b = $('#diff-b').value;
    if (!a || !b) return alert('Selecione dois prompts');
    const r = await fetch('/api/diff', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({left: a, right: b})
    });
    const j = await r.json();
    renderDiffOutput(j);
}

function renderDiffOutput(j) {
    const out = $('#diff-output');
    out.innerHTML = `
        <div class="diff-stats">
            <span>Left: <strong>${j.left_size.toLocaleString()}</strong> tokens</span>
            <span>Right: <strong>${j.right_size.toLocaleString()}</strong> tokens</span>
            <span>Diff: <strong>${j.diff_tokens >= 0 ? '+' : ''}${j.diff_tokens.toLocaleString()}</strong> tokens (${j.diff_pct}%)</span>
            <span>Added lines: ${j.added} | Removed: ${j.removed}</span>
        </div>
        <div class="diff-content">
            <pre>${j.diff_html}</pre>
        </div>
    `;
}

function addToDiff(p) {
    diffList.push(p.id);
    if (diffList.length === 1) switchView('diff');
    const a = $('#diff-a');
    if (a) { a.value = p.id; }
    else if (diffList.length >= 2) {
        switchView('diff');
        $('#diff-a').value = diffList[0];
        $('#diff-b').value = p.id;
    }
}

// ============ Validate ============
function renderValidate() {
    const c = $('#content');
    c.innerHTML = `
        <h2>✅ Validate a System Prompt</h2>
        <p class="muted">Cole seu prompt ou escolha um do índice pra validar contra as melhores práticas.</p>
        <div class="validate-area">
            <select id="v-from-index"><option value="">— From index (or type below) —</option></select>
            <textarea id="v-content" placeholder="Cole seu system prompt aqui..." rows="20"></textarea>
            <button id="v-run">Run validation</button>
        </div>
        <div id="v-result"></div>
    `;
    const opts = state.index.slice(0, 200).map(p => `<option value="${p.id}">${escapeHtml(p.filename)}</option>`).join('');
    $('#v-from-index').innerHTML += opts;
    $('#v-from-index').addEventListener('change', async (e) => {
        if (e.target.value) {
            const r = await fetch('/api/raw?id=' + encodeURIComponent(e.target.value));
            const j = await r.json();
            $('#v-content').value = j.content || '';
        }
    });
    $('#v-run').addEventListener('click', runValidation);
}

async function runValidation() {
    const content = $('#v-content').value;
    if (!content) return alert('Cole um prompt primeiro');
    const r = await fetch('/api/validate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({content})
    });
    const j = await r.json();
    const gradeColors = { 'A+': '#10b981', 'A': '#22c55e', 'B': '#84cc16', 'C': '#eab308', 'D': '#f97316', 'F': '#ef4444' };
    $('#v-result').innerHTML = `
        <div class="v-summary" style="border-color: ${gradeColors[j.grade] || '#888'}">
            <div class="v-score" style="color: ${gradeColors[j.grade]}">${j.score}%</div>
            <div class="v-grade" style="background: ${gradeColors[j.grade]}">${j.grade}</div>
            <p class="v-verdict">${j.summary}</p>
            <div class="v-stats">
                <span>${j.stats.chars.toLocaleString()} chars</span>
                <span>${j.stats.words.toLocaleString()} words</span>
                <span>~${j.stats.tokens_estimate.toLocaleString()} tokens</span>
            </div>
        </div>
        <div class="v-checks">
            <div class="v-passed">
                <h3>✅ Passed (${j.passed.length})</h3>
                ${j.passed.map(p => `<div class="v-check"><strong>${p.key}</strong>: ${escapeHtml(p.description)}</div>`).join('')}
            </div>
            <div class="v-failed">
                <h3>❌ Missing (${j.failed.length})</h3>
                ${j.failed.map(p => `<div class="v-check failed"><strong>${p.key}</strong>: ${escapeHtml(p.description)}</div>`).join('')}
            </div>
            ${j.warnings.length > 0 ? `
            <div class="v-warnings">
                <h3>⚠️ Warnings (${j.warnings.length})</h3>
                ${j.warnings.map(p => `<div class="v-check warning"><strong>${p.key}</strong>: ${escapeHtml(p.description)}</div>`).join('')}
            </div>
            ` : ''}
        </div>
    `;
}

function validatePrompt(p) {
    switchView('validate');
    setTimeout(() => {
        const v = $('#v-from-index');
        if (v) v.value = p.id;
        const t = $('#v-content');
        if (t) t.value = `Loading...`;
        fetch('/api/raw?id=' + encodeURIComponent(p.id)).then(r => r.json()).then(j => {
            if (t) t.value = j.content;
        });
    }, 100);
}

// ============ Generate ============
function renderGenerate() {
    const c = $('#content');
    c.innerHTML = `
        <h2>✨ Generate a System Prompt</h2>
        <p class="muted">Descreva o que você quer e eu monto um prompt completo baseado em padrões dos melhores modelos.</p>
        <div class="gen-presets">
            <strong>Quick start:</strong>
            <button data-preset="claude_coding_agent">🤖 Claude Code-style agent</button>
            <button data-preset="gpt5_assistant">💬 ChatGPT-style assistant</button>
            <button data-preset="cursor_style_coding">⚡ Cursor-style IDE agent</button>
            <button data-preset="perplexity_search">🔍 Perplexity-style search</button>
            <button data-preset="devin_autonomous">🛠️ Devin-style autonomous</button>
        </div>
        <div class="gen-form">
            <div class="form-row">
                <label>Name <input id="g-name" placeholder="MyBot"></label>
                <label>Role <input id="g-role" placeholder="a helpful coding assistant"></label>
            </div>
            <div class="form-row">
                <label>Company <input id="g-company" placeholder="Acme Inc"></label>
                <label>Model <input id="g-model" placeholder="claude-sonnet-4-5"></label>
            </div>
            <div class="form-row">
                <label>Tone
                    <select id="g-tone">
                        <option value="default">Default (warm + concise)</option>
                        <option value="concise">Concise</option>
                        <option value="professional">Professional</option>
                        <option value="creative">Creative</option>
                    </select>
                </label>
                <label>Safety
                    <select id="g-safety">
                        <option value="default">Default (strict)</option>
                        <option value="minimal">Minimal</option>
                        <option value="creative">Creative (looser)</option>
                    </select>
                </label>
                <label>Memory
                    <select id="g-memory">
                        <option value="default">With memory</option>
                        <option value="none">No memory</option>
                    </select>
                </label>
            </div>
            <div class="form-row">
                <label>Tools (comma-separated) <input id="g-tools" placeholder="web_search, file_read, bash"></label>
            </div>
            <div class="form-row">
                <label><input type="checkbox" id="g-examples" checked> Include example section</label>
            </div>
            <button id="g-generate">✨ Generate</button>
        </div>
        <div id="gen-output"></div>
    `;
    $$('.gen-presets button').forEach(b => {
        b.addEventListener('click', () => loadPreset(b.dataset.preset));
    });
    $('#g-generate').addEventListener('click', generatePrompt);
}

async function loadPreset(name) {
    const r = await fetch('/api/presets/' + name);
    const j = await r.json();
    $('#g-name').value = j.spec.name || '';
    $('#g-role').value = j.spec.role_description || '';
    $('#g-company').value = j.spec.company || '';
    $('#g-model').value = j.spec.model || '';
    $('#g-tone').value = j.spec.tone || 'default';
    $('#g-safety').value = j.spec.safety || 'default';
    $('#g-memory').value = j.spec.memory || 'default';
    $('#g-tools').value = (j.spec.tools || []).join(', ');
    $('#g-examples').checked = j.spec.include_examples !== false;
    generatePrompt();
}

async function generatePrompt() {
    const spec = {
        name: $('#g-name').value || 'Assistant',
        role_description: $('#g-role').value || 'an AI assistant',
        company: $('#g-company').value || 'your company',
        model: $('#g-model').value || 'your-model',
        tone: $('#g-tone').value,
        safety: $('#g-safety').value,
        memory: $('#g-memory').value,
        tools: $('#g-tools').value.split(',').map(s => s.trim()).filter(Boolean),
        include_examples: $('#g-examples').checked,
    };
    const r = await fetch('/api/generate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(spec)
    });
    const j = await r.json();
    $('#gen-output').innerHTML = `
        <h3>Generated prompt (${j.tokens} tokens, ${j.chars} chars)</h3>
        <div class="actions">
            <button id="g-copy">📋 Copy to clipboard</button>
            <button id="g-download">💾 Download as .md</button>
            <button id="g-validate">✅ Validate this prompt</button>
        </div>
        <pre id="gen-pre">${escapeHtml(j.prompt)}</pre>
    `;
    $('#g-copy').addEventListener('click', () => {
        navigator.clipboard.writeText(j.prompt);
        event.target.textContent = '✓ Copied!';
    });
    $('#g-download').addEventListener('click', () => {
        const blob = new Blob([j.prompt], {type: 'text/markdown'});
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = 'system-prompt.md';
        a.click();
    });
    $('#g-validate').addEventListener('click', () => {
        switchView('validate');
        $('#v-content').value = j.prompt;
        setTimeout(runValidation, 200);
    });
}

// ============ Utils ============
function escapeHtml(s) {
    if (!s) return '';
    return String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}

init();
