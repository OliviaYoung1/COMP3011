//GenAI Declearation: Code was written with help by ClaudeAI- All generated suggestions were reviewed and adapted by me before implementing them.
const API_BASE = "http://127.0.0.1:8000/api";

/* ─────────────────────────────────────────────
   RENDERERS
   ───────────────────────────────────────────── */

function renderTopTracks(tracks) {
    const container = document.getElementById("top-tracks-list");

    if (!tracks || tracks.length === 0) {
        container.innerHTML = '<p style="padding:20px 28px;color:var(--text-muted);font-size:14px;">No tracks found.</p>';
        return;
    }

    const rows = tracks.map((track, i) => `
        <tr>
            <td>
                <span class="track-num">${i + 1}</span>
                <span class="play-icon" style="display:none">▶</span>
            </td>
            <td>
                <div class="track-info-cell">
                    <div class="track-art-placeholder">♪</div>
                    <div>
                        <div class="track-name">${track.track_name}</div>
                        <div class="track-artist">${track.artists}</div>
                    </div>
                </div>
            </td>
            <td>${track.album_name ?? "—"}</td>
            <td>${track.duration_ms ? msToMinSec(track.duration_ms) : "—"}</td>
            <td>
                <div class="popularity-bar">
                    <div class="bar-track">
                        <div class="bar-fill" style="width:${track.popularity ?? 0}%"></div>
                    </div>
                    <span>${track.popularity ?? 0}</span>
                </div>
            </td>
        </tr>`
    ).join("");

    container.innerHTML = `
        <table class="tracks-table">
            <thead>
                <tr>
                    <th>#</th>
                    <th>Title</th>
                    <th>Album</th>
                    <th>Duration</th>
                    <th>Popularity</th>
                </tr>
            </thead>
            <tbody>${rows}</tbody>
        </table>`;
}

function renderPlaylists(playlists) {
    const container = document.getElementById("playlist-list");

    if (!playlists || playlists.length === 0) {
        container.innerHTML = '<p style="padding:8px 0 4px;color:var(--text-muted);font-size:14px;">No playlists yet.</p>';
        return;
    }

    container.innerHTML = playlists.map(p => {
        const count = p.tracks ? p.tracks.length : 0;

        const trackRows = p.tracks && p.tracks.length > 0
            ? p.tracks.map((t, i) => `
                <tr>
                    <td>${i + 1}</td>
                    <td>${t.track.track_name}</td>
                    <td>${t.track.artists ?? "—"}</td>
                    <td>${t.track.album_name ?? "—"}</td>
                    <td>${t.track.duration_ms ? msToMinSec(t.track.duration_ms) : "—"}</td>
                    <td>
                        <button class="btn-remove" onclick="removeTrack(${t.id})">Remove</button>
                    </td>
                </tr>`).join("")
            : null;

        const tableHtml = trackRows
            ? `<table class="playlist-tracks-table">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Title</th>
                            <th>Artist</th>
                            <th>Album</th>
                            <th>Duration</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>${trackRows}</tbody>
               </table>`
            : `<div class="playlist-empty">No tracks yet — add some above!</div>`;

        return `
            <div class="playlist" id="playlist-${p.id}">
                <div class="playlist-header">
                    <div class="playlist-icon">🎵</div>
                    <div class="playlist-meta">
                        <h3>${p.name}</h3>
                        <p>${p.description ? p.description + " · " : ""}${count} track${count !== 1 ? "s" : ""}</p>
                    </div>
                    <button class="btn-delete" onclick="deletePlaylist(${p.id})" style="margin-left:auto">Delete</button>
                </div>
                ${tableHtml}
            </div>`;
    }).join("");
}

/* ─────────────────────────────────────────────
   HELPERS
   ───────────────────────────────────────────── */

function msToMinSec(ms) {
    const total = Math.floor(ms / 1000);
    const min = Math.floor(total / 60);
    const sec = String(total % 60).padStart(2, "0");
    return `${min}:${sec}`;
}

/* ─────────────────────────────────────────────
   API FUNCTIONS
   ───────────────────────────────────────────── */

async function loadFilteredTracks() {
    const params = new URLSearchParams();

    const genre = document.getElementById("filter-genre").value.trim();
    const minDance = document.getElementById("filter-min-dance").value.trim();
    const minEnergy = document.getElementById("filter-min-energy").value.trim();
    const minValence = document.getElementById("filter-min-valence").value.trim();
    const minTempo = document.getElementById("filter-min-tempo").value.trim();
    const explicit = document.getElementById("filter-explicit").value;

    if (genre) params.append("genre", genre);
    if (minDance) params.append("min_danceability", minDance);
    if (minEnergy) params.append("min_energy", minEnergy);
    if (minValence) params.append("min_valence", minValence);
    if (minTempo) params.append("min_tempo", minTempo);
    if (explicit) params.append("explicit", explicit);

    params.append("limit", "10");

    const response = await fetch(`${API_BASE}/analytics/top-tracks/?${params}`);
    const data = await response.json();

    console.log("Filtered tracks:", data);

    renderFilteredTracks(data.results);
}

function renderFilteredTracks(tracks) {
    const tbody = document.getElementById("top-tracks-body");
    tbody.innerHTML = "";

    tracks.forEach((track, index) => {
        const tr = document.createElement("tr");

        tr.innerHTML = `
            <td>${index + 1}</td>
            <td>${track.track_name}</td>
            <td>${track.artists}</td>
            <td>${track.track_genre || "-"}</td>
            <td>${track.popularity}</td>
            <td>${track.danceability?.toFixed(2)}</td>
            <td>${track.energy?.toFixed(2)}</td>
        `;

        tbody.appendChild(tr);
    });
}

async function loadPlaylists() {
    const response = await fetch(`${API_BASE}/playlists/`);
    const playlists = await response.json();
    renderPlaylists(playlists);
    refreshPlaylistDropdown(playlists);
}

async function createPlaylist() {
    const name = document.getElementById("playlist-name").value;
    const description = document.getElementById("playlist-description").value;

    const response = await fetch(`${API_BASE}/playlists/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, description })
    });

    if (response.ok) {
        document.getElementById("playlist-name").value = "";
        document.getElementById("playlist-description").value = "";
        alert("Playlist created successfully!");
        loadPlaylists();
    } else {
        alert("Failed to create playlist.");
    }
}

async function deletePlaylist(id) {
    await fetch(`${API_BASE}/playlists/${id}/`, { method: "DELETE" });
    loadPlaylists();
}

async function addTrack() {
    const playlist = document.getElementById("playlist-select").value;

    if (!selectedTrack) {
        alert("Please select a track first.");
        return;
    }

    const response = await fetch(`${API_BASE}/playlists/add-track/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ playlist, track: selectedTrack })
    });

    if (response.ok) {
        alert("Track added to playlist!");
        loadPlaylists();
        selectedTrack = null;
        document.getElementById("track-search").value = "";
        document.getElementById("track-results").innerHTML = "";
    } else {
        alert("Failed to add track.");
    }
}

async function removeTrack(playlistTrackId) {
    await fetch(`${API_BASE}/playlists/remove-track/${playlistTrackId}/`, {
        method: "DELETE"
    });
    loadPlaylists();
}

/* ─────────────────────────────────────────────
   DROPDOWN + SEARCH
   ───────────────────────────────────────────── */

function refreshPlaylistDropdown(playlists) {
    const playlistSelect = document.getElementById("playlist-select");
    playlistSelect.innerHTML = "";

    playlists.forEach(p => {
        const option = document.createElement("option");
        option.value = p.id;
        option.textContent = `${p.name} (ID: ${p.id})`;
        playlistSelect.appendChild(option);
    });
}

async function loadDropdownData() {
    const playlistResponse = await fetch(`${API_BASE}/playlists/`);
    const playlists = await playlistResponse.json();
    refreshPlaylistDropdown(playlists);
}

function filterPlaylists() {
    const search = document.getElementById("playlist-search").value.toLowerCase();
    const options = document.getElementById("playlist-select").options;

    for (let opt of options) {
        opt.style.display = opt.textContent.toLowerCase().includes(search) ? "" : "none";
    }
}

let selectedTrack = null;

async function searchTracks() {
    const query = document.getElementById("track-search").value;

    if (query.length < 2) {
        document.getElementById("track-results").innerHTML = "";
        return;
    }

    const response = await fetch(`${API_BASE}/tracks/?search=${query}`);
    const tracks = await response.json();

    const container = document.getElementById("track-results");
    container.innerHTML = "";

    tracks.slice(0, 10).forEach(track => {
        const div = document.createElement("div");
        div.className = "result-item";
        div.innerHTML = `
            <span>♪</span>
            <span><strong>${track.track_name}</strong> — ${track.artists}</span>
            <button class="btn-select" onclick="selectTrack('${track.track_id}', '${track.track_name.replace(/'/g, "\\'")}')">Select</button>
        `;
        container.appendChild(div);
    });
}

function selectTrack(id, name) {
    selectedTrack = id;
    document.getElementById("track-search").value = name;
    document.getElementById("track-results").innerHTML = "";
}

function selectTrackFromExplorer(trackId, trackName) {
    selectedTrack = trackId;
    document.getElementById("track-search").value = trackName;
    document.getElementById("track-results").innerHTML = "";
    document.getElementById("add-track").scrollIntoView({ behavior: "smooth" });
}

async function loadGenres() {
    const response = await fetch(`${API_BASE}/analytics/genres/`);
    const data = await response.json();

    const select = document.getElementById("filter-genre");
    select.innerHTML = `<option value="">Any</option>`; // reset

    data.genres.forEach(genre => {
        const option = document.createElement("option");
        option.value = genre;
        option.textContent = genre;
        select.appendChild(option);
    });
}

/* ─────────────────────────────────────────────
   INIT
   ───────────────────────────────────────────── */
loadGenres();
loadFilteredTracks();
loadPlaylists();
loadDropdownData();