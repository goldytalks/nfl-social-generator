// NFL Social Content Generator - Frontend JavaScript

// State management
const state = {
    dataLoaded: false,
    moversAnalyzed: false,
    tweetsGenerated: false,
    currentMovers: [],
    currentResults: []
};

// DOM Elements
const fileInput = document.getElementById('file-input');
const uploadBtn = document.getElementById('upload-btn');
const analyzeBtn = document.getElementById('analyze-btn');
const generateBtn = document.getElementById('generate-btn');
const exportBtn = document.getElementById('export-btn');

const uploadStatus = document.getElementById('upload-status');
const dataSummary = document.getElementById('data-summary');
const analyzeStatus = document.getElementById('analyze-status');
const moversSummary = document.getElementById('movers-summary');
const moversTable = document.getElementById('movers-table');
const generateStatus = document.getElementById('generate-status');
const tweetsContainer = document.getElementById('tweets-container');
const exportStatus = document.getElementById('export-status');

const thresholdInput = document.getElementById('threshold-input');
const topNInput = document.getElementById('top-n-input');

// Event Listeners
uploadBtn.addEventListener('click', uploadFile);
analyzeBtn.addEventListener('click', analyzeMovers);
generateBtn.addEventListener('click', generateTweets);
exportBtn.addEventListener('click', exportResults);

// Upload CSV file
async function uploadFile() {
    const file = fileInput.files[0];

    if (!file) {
        showStatus(uploadStatus, 'Please select a file', 'error');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    uploadBtn.disabled = true;
    showStatus(uploadStatus, 'Uploading...', 'info');

    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            showStatus(uploadStatus, `✓ File uploaded successfully: ${data.filename}`, 'success');
            displayDataSummary(data.summary);
            state.dataLoaded = true;
            analyzeBtn.disabled = false;
        } else {
            showStatus(uploadStatus, `Error: ${data.error}`, 'error');
        }
    } catch (error) {
        showStatus(uploadStatus, `Upload failed: ${error.message}`, 'error');
    } finally {
        uploadBtn.disabled = false;
    }
}

// Analyze movers
async function analyzeMovers() {
    const threshold = parseFloat(thresholdInput.value);
    const topN = parseInt(topNInput.value);

    analyzeBtn.disabled = true;
    showStatus(analyzeStatus, 'Analyzing movers...', 'info');

    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ threshold, top_n: topN })
        });

        const data = await response.json();

        if (data.success) {
            showStatus(analyzeStatus, `✓ Found ${data.movers.length} significant movers`, 'success');
            displayMoversSummary(data.summary);
            displayMoversTable(data.movers);
            state.moversAnalyzed = true;
            state.currentMovers = data.movers;
            generateBtn.disabled = false;
        } else {
            showStatus(analyzeStatus, `Error: ${data.error}`, 'error');
        }
    } catch (error) {
        showStatus(analyzeStatus, `Analysis failed: ${error.message}`, 'error');
    } finally {
        analyzeBtn.disabled = false;
    }
}

// Generate tweets
async function generateTweets() {
    generateBtn.disabled = true;
    showStatus(generateStatus, 'Generating tweet drafts...', 'info');

    try {
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({})
        });

        const data = await response.json();

        if (data.success) {
            showStatus(generateStatus, `✓ Generated ${data.count} tweet sets`, 'success');
            displayTweets(data.results);
            state.tweetsGenerated = true;
            state.currentResults = data.results;
            exportBtn.disabled = false;
        } else {
            showStatus(generateStatus, `Error: ${data.error}`, 'error');
        }
    } catch (error) {
        showStatus(generateStatus, `Generation failed: ${error.message}`, 'error');
    } finally {
        generateBtn.disabled = false;
    }
}

// Export results
async function exportResults() {
    exportBtn.disabled = true;
    showStatus(exportStatus, 'Exporting...', 'info');

    try {
        const response = await fetch('/api/export', {
            method: 'POST'
        });

        const data = await response.json();

        if (data.success) {
            showStatus(exportStatus, `✓ Exported to ${data.filename}`, 'success');
        } else {
            showStatus(exportStatus, `Error: ${data.error}`, 'error');
        }
    } catch (error) {
        showStatus(exportStatus, `Export failed: ${error.message}`, 'error');
    } finally {
        exportBtn.disabled = false;
    }
}

// Display functions
function showStatus(element, message, type) {
    element.textContent = message;
    element.className = `status-message ${type}`;
    element.style.display = 'block';
}

function displayDataSummary(summary) {
    dataSummary.innerHTML = `
        <h3>Data Summary</h3>
        <div class="summary-grid">
            <div class="summary-item">
                <label>Total Rows</label>
                <div class="value">${summary.total_rows}</div>
            </div>
            <div class="summary-item">
                <label>Markets</label>
                <div class="value">${summary.markets.length}</div>
            </div>
            <div class="summary-item">
                <label>Avg Change</label>
                <div class="value">${summary.avg_change.toFixed(2)}%</div>
            </div>
            <div class="summary-item">
                <label>Max Change</label>
                <div class="value">${summary.max_change.toFixed(2)}%</div>
            </div>
        </div>
    `;
    dataSummary.classList.remove('hidden');
}

function displayMoversSummary(summary) {
    moversSummary.innerHTML = `
        <h3>Movers Summary</h3>
        <div class="summary-grid">
            <div class="summary-item">
                <label>Total Movers</label>
                <div class="value">${summary.total_movers}</div>
            </div>
            <div class="summary-item">
                <label>Risers</label>
                <div class="value">${summary.risers_count}</div>
            </div>
            <div class="summary-item">
                <label>Fallers</label>
                <div class="value">${summary.fallers_count}</div>
            </div>
            <div class="summary-item">
                <label>Avg Change</label>
                <div class="value">${summary.avg_change.toFixed(2)}%</div>
            </div>
        </div>
    `;
    moversSummary.classList.remove('hidden');
}

function displayMoversTable(movers) {
    const tableHTML = `
        <h3>Top Movers</h3>
        <table>
            <thead>
                <tr>
                    <th>Market</th>
                    <th>Team/Player</th>
                    <th>Last Week</th>
                    <th>This Week</th>
                    <th>Change</th>
                    <th>Direction</th>
                    <th>Magnitude</th>
                </tr>
            </thead>
            <tbody>
                ${movers.map(mover => `
                    <tr>
                        <td>${mover.market}</td>
                        <td><strong>${mover.team_player}</strong></td>
                        <td>${mover.last_week_american}</td>
                        <td>${mover.this_week_american}</td>
                        <td><strong>${mover.change_pct > 0 ? '+' : ''}${mover.change_pct.toFixed(2)}%</strong></td>
                        <td><span class="badge badge-${mover.direction}">${mover.direction.toUpperCase()}</span></td>
                        <td><span class="badge badge-${mover.magnitude}">${mover.magnitude}</span></td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
    moversTable.innerHTML = tableHTML;
    moversTable.classList.remove('hidden');
}

function displayTweets(results) {
    const tweetsHTML = results.map((result, index) => `
        <div class="tweet-result">
            <div class="tweet-header">
                <div class="tweet-title">
                    ${result.team_player} - ${result.market}
                </div>
                <div class="movement-info">
                    <span class="badge badge-${result.movement.direction}">
                        ${result.movement.direction === 'up' ? '↑' : '↓'}
                        ${result.movement.change_pct > 0 ? '+' : ''}${result.movement.change_pct}%
                    </span>
                    <span>${result.movement.last_week_american} → ${result.movement.this_week_american}</span>
                </div>
            </div>
            <div class="tweet-drafts">
                ${result.tweet_drafts.map((draft, draftIndex) => `
                    <div class="tweet-draft">
                        <div class="tweet-version">${draft.version}</div>
                        <div class="tweet-content">${escapeHtml(draft.content)}</div>
                        <div class="tweet-meta">
                            <span class="char-count ${!draft.within_limit ? 'over-limit' : ''}">
                                ${draft.character_count} / 280 characters
                                ${!draft.within_limit ? ' ⚠️ OVER LIMIT' : ' ✓'}
                            </span>
                            <button class="copy-btn" onclick="copyTweet('${escapeForAttribute(draft.content)}')">
                                Copy Tweet
                            </button>
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>
    `).join('');

    tweetsContainer.innerHTML = tweetsHTML;
    tweetsContainer.classList.remove('hidden');
}

// Copy tweet to clipboard
function copyTweet(content) {
    const textarea = document.createElement('textarea');
    textarea.value = content;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);

    // Show feedback
    alert('Tweet copied to clipboard!');
}

// Utility functions
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function escapeForAttribute(text) {
    return text
        .replace(/\\/g, '\\\\')
        .replace(/'/g, "\\'")
        .replace(/"/g, '&quot;')
        .replace(/\n/g, '\\n');
}
