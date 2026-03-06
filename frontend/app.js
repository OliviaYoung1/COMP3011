const API_BASE = "http://127.0.0.1:8000/api";

// CREATE PLAYLIST
async function createPlaylist() {
    const name = document.getElementById("playlist-name").value;
    const description = document.getElementById("playlist-description").value;

    const response = await fetch(`${API_BASE}/playlists/`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ name, description })
    });

    loadPlaylists();
}

// LOAD PLAYLISTS
async function loadPlaylists() {
    const response = await fetch(`${API_BASE}/playlists/`);
    const playlists = await response.json();

    const container = document.getElementById("playlist-list");
    container.innerHTML = "";

    playlists.forEach(p => {
        const div = document.createElement("div");
        div.className = "playlist";

        div.innerHTML = `
            <h3>${p.name}</h3>
            <p>${p.description}</p>
            <p><strong>ID:</strong> ${p.id}</p>

            <h4>Songs in this playlist:</h4>
            <ul>
                ${p.tracks.map(t => `
                    <li>
                        ${t.track.track_name} (${t.track.track_id})
                        <button onclick="removeTrack(${t.id})">Remove</button>
                    </li>
                `).join("")}
            </ul>

            <button onclick="deletePlaylist(${p.id})">Delete Playlist</button>
        `;

        container.appendChild(div);
    });
}

// DELETE PLAYLIST
async function deletePlaylist(id) {
    await fetch(`${API_BASE}/playlists/${id}/`, { method: "DELETE" });
    loadPlaylists();
}

// ADD TRACK
async function addTrack() {
    const playlist = document.getElementById("playlist-id").value;
    const track = document.getElementById("track-id").value;

    await fetch(`${API_BASE}/playlists/add-track/`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ playlist, track })
    });

    loadPlaylists();
}

// REMOVE TRACK
async function removeTrack(playlistTrackId) {
    await fetch(`${API_BASE}/playlists/remove-track/${playlistTrackId}/`, {
        method: "DELETE"
    });

    loadPlaylists();
}

// LOAD TOP TRACKS
async function loadTopTracks() {
    const response = await fetch(`${API_BASE}/analytics/top-tracks/`);
    const data = await response.json();

    // Extract the array correctly
    const tracks = data.results;

    const container = document.getElementById("top-tracks-list");
    container.innerHTML = "";

    tracks.forEach(track => {
        const div = document.createElement("div");
        div.className = "top-track";

        div.innerHTML = `
            <p><strong>${track.track_name}</strong> — ${track.artists} (Popularity: ${track.popularity})</p>
        `;

        container.appendChild(div);
    });
}

// Load playlists on page load
loadTopTracks();
loadPlaylists();

