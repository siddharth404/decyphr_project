/* ==========================================================================
   FILE: 3_Source_Code/decyphr/report_builder/assets/scripts/interactivity.js
   PURPOSE: Handles all client-side interactivity for the Decyphr report,
            including theme switching, lazy plot rendering, and tabbed navigation.
   VERSION: 4.1 (Robust Navigation Fix)
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {

    // --- Global State & Element Selection ---
    const body = document.body;
    const themeToggleButton = document.getElementById('theme-toggle');
    const navLinks = document.querySelectorAll('.top-nav a.nav-link');
    const contentPanels = document.querySelectorAll('.content-panel');

    // --- 1. Load and Parse Embedded Plot Data ---
    let ALL_PLOTS_DATA = {};
    const plotDataElement = document.getElementById('plot-data');
    if (plotDataElement) {
        try {
            ALL_PLOTS_DATA = JSON.parse(plotDataElement.textContent || '{}');
            console.log("Decyphr: Plot data loaded successfully.");
        } catch (e) {
            console.error("Decyphr Error: Failed to parse plot data.", e);
        }
    } else {
        console.warn("Decyphr Warning: No plot-data element found.");
    }

    let renderedSections = new Set(); // Keep track of which sections have been rendered

    // --- 2. Theme Management Module ---
    const applyTheme = (theme) => {
        body.setAttribute('data-theme', theme);
        localStorage.setItem('decyphrTheme', theme);
        // We only update themes for plots that are already visible
        try {
            updateVisiblePlotlyThemes(theme);
        } catch (e) {
            console.warn("Theme update failed (possibly Plotly not loaded):", e);
        }
    };

    const updateVisiblePlotlyThemes = (theme) => {
        if (typeof Plotly === 'undefined') return;

        const layoutUpdate = theme === 'dark'
            ? { paper_bgcolor: '#1e293b', plot_bgcolor: 'rgba(0,0,0,0)', font: { color: '#e2e8f0' }, 'xaxis.gridcolor': '#334155', 'yaxis.gridcolor': '#334155', 'legend.bgcolor': 'rgba(0,0,0,0.3)' }
            : { paper_bgcolor: '#ffffff', plot_bgcolor: 'rgba(0,0,0,0)', font: { color: '#0f172a' }, 'xaxis.gridcolor': '#e5e7eb', 'yaxis.gridcolor': 'rgba(255,255,255,0.7)' };

        document.querySelectorAll('.plot-placeholder:not(:empty) .js-plotly-plot').forEach(plotDiv => {
            if (plotDiv.data) {
                Plotly.relayout(plotDiv, layoutUpdate);
            }
        });
    };

    if (themeToggleButton) {
        themeToggleButton.addEventListener('click', () => {
            const newTheme = body.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
            applyTheme(newTheme);
        });
    }

    // --- 3. Lazy Plot Rendering Module ---
    const renderPlotsForSection = (sectionId) => {
        if (typeof Plotly === 'undefined') {
            console.warn("Decyphr Warning: Plotly library not loaded. Charts will not match.");
            return;
        }

        // Only render a section's plots once to save resources
        if (renderedSections.has(sectionId)) {
            return;
        }

        const plotDataForSection = ALL_PLOTS_DATA[sectionId];
        if (!plotDataForSection || plotDataForSection.length === 0) {
            renderedSections.add(sectionId); // Mark as "rendered" even if no plots
            return;
        }

        console.log(`Lazy loading plots for section: ${sectionId}`);

        plotDataForSection.forEach((plotJson, index) => {
            const placeholderId = `plot-${sectionId}-${index}`;
            const placeholderDiv = document.getElementById(placeholderId);
            if (placeholderDiv) {
                try {
                    // Use Plotly.newPlot to draw the chart from its JSON definition
                    Plotly.newPlot(placeholderDiv, plotJson.data, plotJson.layout, { responsive: true, displayModeBar: false });
                } catch (e) {
                    console.error(`Failed to render plot ${placeholderId}:`, e);
                }
            }
        });

        renderedSections.add(sectionId);
        // Apply the current theme to the newly rendered plots
        updateVisiblePlotlyThemes(body.getAttribute('data-theme'));
    };

    // --- 4. Tabbed Navigation Module ---
    navLinks.forEach(link => {
        link.addEventListener('click', (event) => {
            event.preventDefault();
            const targetSectionId = link.getAttribute('data-section-id');
            console.log("Navigating to section:", targetSectionId);

            // Update Navigation Link states
            navLinks.forEach(nav => nav.classList.remove('active'));
            link.classList.add('active');

            // Update Content Panel visibility
            contentPanels.forEach(panel => {
                const isActive = panel.id === `panel-${targetSectionId}`;
                panel.classList.toggle('active', isActive);
                // CRITICAL FIX: Toggle display property because inline styles are used in HTML
                panel.style.display = isActive ? 'block' : 'none';
            });

            // Render plots for the newly visible section
            // Wrap in try-catch to ensure navigation works even if plotting fails
            try {
                renderPlotsForSection(targetSectionId);
            } catch (e) {
                console.error("Plot rendering failed during navigation:", e);
            }

            // Scroll to top of content area on tab switch
            const mainContent = document.querySelector('.main-content');
            if (mainContent) mainContent.scrollTop = 0;
        });
    });

    // --- 5. Initial Page Load Logic ---
    const savedTheme = localStorage.getItem('decyphrTheme') || 'dark';
    applyTheme(savedTheme);

    // Render plots for the initially active section on page load
    const initialActiveSection = document.querySelector('.content-panel.active');
    if (initialActiveSection) {
        const initialSectionId = initialActiveSection.id.replace('panel-', '');
        try {
            renderPlotsForSection(initialSectionId);
        } catch (e) {
            console.error("Initial plot rendering failed:", e);
        }
    }
});