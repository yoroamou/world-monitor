document.addEventListener('DOMContentLoaded', () => {
    // 1. Initialize Leaflet Map
    const map = L.map('world-map', {
        zoomControl: false, // We'll add it in a custom position if needed
        attributionControl: false,
        minZoom: 2,
        maxBounds: [
            [-90, -180],
            [90, 180]
        ]
    }).setView([20, 0], 2);

    // Add Dark Matter Tile Layer (matches dark UI)
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        subdomains: 'abcd',
        maxZoom: 19
    }).addTo(map);

    let geojsonLayer;
    let selectedLayer = null;

    // 2. Fetch GeoJSON Data for Countries
    const GEOJSON_URL = 'https://raw.githubusercontent.com/datasets/geo-boundaries-world-110m/master/countries.geojson';

    fetch(GEOJSON_URL)
        .then(response => response.json())
        .then(data => {
            geojsonLayer = L.geoJSON(data, {
                style: getCountryStyle,
                onEachFeature: onEachFeature
            }).addTo(map);
        })
        .catch(error => console.error("Error loading GeoJSON:", error));

    // 3. Map Styling and Interaction Methods
    function getCountryStyle(feature) {
        return {
            fillColor: '#1a1d29', // Dark card bg
            weight: 1,
            opacity: 1,
            color: 'rgba(255, 255, 255, 0.1)', // Subtle border
            fillOpacity: 0.7
        };
    }

    function highlightFeature(e) {
        const layer = e.target;
        if (layer !== selectedLayer) {
            layer.setStyle({
                fillColor: '#2d3348',
                fillOpacity: 0.9,
                color: 'rgba(255, 255, 255, 0.3)'
            });
        }
    }

    function resetHighlight(e) {
        const layer = e.target;
        if (layer !== selectedLayer) {
            geojsonLayer.resetStyle(layer);
        }
    }

    function selectCountry(e) {
        const layer = e.target;
        const feature = layer.feature;
        const isoCode = feature.properties.iso_a2; // 'US', 'IN', etc.
        const countryName = feature.properties.name;

        // Visual selection on map
        if (selectedLayer) geojsonLayer.resetStyle(selectedLayer);
        selectedLayer = layer;
        layer.setStyle({
            fillColor: '#f472b6', // Accent Pink
            fillOpacity: 0.8,
            color: '#fff',
            weight: 2
        });
        
        // Ensure the layer is brought to front visually
        if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
            layer.bringToFront();
        }

        fetchCountryData(isoCode, countryName);
    }

    function onEachFeature(feature, layer) {
        layer.on({
            mouseover: highlightFeature,
            mouseout: resetHighlight,
            click: selectCountry
        });
    }

    // 4. API Fetching and UI Updates
    const emptyState = document.getElementById('empty-state');
    const loadingState = document.getElementById('loading-state');
    const dataState = document.getElementById('data-state');

    function fetchCountryData(isoCode, countryName) {
        // Show loading state
        emptyState.classList.add('hidden');
        dataState.classList.add('hidden');
        loadingState.classList.remove('hidden');
        loadingState.classList.add('flex');

        // Note: iso_a2 might be '-99' for some missing regions in the dataset
        if (!isoCode || isoCode === '-99') {
            showErrorUI(countryName, "Country code not recognized.");
            return;
        }

        fetch(`/api/country/${isoCode}/`)
            .then(response => {
                if (!response.ok) throw new Error('API request failed');
                return response.json();
            })
            .then(data => {
                updatePanelUI(data, countryName);
            })
            .catch(error => {
                console.error("Fetch error:", error);
                showErrorUI(countryName, "Unable to fetch data at this time.");
            });
    }

    function updatePanelUI(data, fallbackName) {
        // Hide loading, show data
        loadingState.classList.add('hidden');
        loadingState.classList.remove('flex');
        dataState.classList.remove('hidden');
        dataState.classList.add('flex');

        // Update Header
        document.getElementById('panel-country-name').textContent = data.country_name || fallbackName;
        document.getElementById('panel-last-updated').textContent = data.last_fetched || 'Just now';
        
        // Quick emoji flag hack based on ISO code
        let flag = "🇺🇳";
        if (data.country_code) {
            const codePoints = data.country_code
                .toUpperCase()
                .split('')
                .map(char =>  127397 + char.charCodeAt());
            flag = String.fromCodePoint(...codePoints);
        }
        document.getElementById('panel-flag').textContent = flag;

        // Update Summary
        document.getElementById('panel-summary').textContent = data.summary;

        // Update News List
        const container = document.getElementById('news-container');
        const template = document.getElementById('news-card-template');
        container.innerHTML = ''; // Clear old

        if (data.articles && data.articles.length > 0) {
            data.articles.forEach(article => {
                const clone = template.content.cloneNode(true);
                clone.querySelector('.title').textContent = article.title;
                clone.querySelector('.description').textContent = article.description || 'No description available.';
                clone.querySelector('.source').textContent = article.source || 'News';
                clone.querySelector('.date').textContent = article.published_at;
                
                const link = clone.querySelector('.link');
                link.href = article.url;
                if (!article.url || article.url === '#') {
                    link.style.display = 'none';
                }
                
                container.appendChild(clone);
            });
        } else {
            container.innerHTML = `<p class="text-xs text-gray-500 italic p-4">No recent news found for this region.</p>`;
        }
    }

    function showErrorUI(countryName, message) {
        loadingState.classList.add('hidden');
        loadingState.classList.remove('flex');
        dataState.classList.remove('hidden');
        dataState.classList.add('flex');

        document.getElementById('panel-country-name').textContent = countryName;
        document.getElementById('panel-last-updated').textContent = 'N/A';
        document.getElementById('panel-flag').textContent = '⚠️';
        document.getElementById('panel-summary').textContent = message;
        document.getElementById('news-container').innerHTML = '';
    }
});
