// State Variables
let database = { last_updated: "", surgeries: [] };
let activeTab = "tab-dashboard";
let historyViewMode = "grid"; // "grid" or "table"
let selectedTreeDays = []; // Array of checked day strings
let bookmarkedSurgeries = [];
try {
    bookmarkedSurgeries = JSON.parse(localStorage.getItem("bookmarked_surgeries") || "[]");
} catch (e) {
    console.warn("localStorage is not available, using in-memory fallback:", e);
}

// DOM Elements
const tabButtons = document.querySelectorAll(".nav-btn, .mobile-nav-btn");
const tabContents = document.querySelectorAll(".tab-content");
const currentTabTitle = document.getElementById("current-tab-title");
const currentTabSubtitle = document.getElementById("current-tab-subtitle");

// KPI elements
const kpiActiveSurgeries = document.getElementById("kpi-active-surgeries");
const kpiEmptySlots = document.getElementById("kpi-empty-slots");
const kpiTopSpecialty = document.getElementById("kpi-top-specialty");
const kpiTopDoctor = document.getElementById("kpi-top-doctor");

// Lists
const insuranceListContainer = document.getElementById("insurance-list");
const statusListContainer = document.getElementById("status-list");

// Tree & History Table/Grid View Panels
const historyTreeContainer = document.getElementById("history-tree");
const historySelectionTitle = document.getElementById("history-selection-title");
const historyTableBody = document.getElementById("history-table-body");
const historyTimelineContainer = document.getElementById("history-timeline-container");
const tableTotalBadge = document.getElementById("table-total-badge");

const btnViewGrid = document.getElementById("btn-view-grid");
const btnViewTable = document.getElementById("btn-view-table");
const historyGridViewPanel = document.getElementById("history-grid-view");
const historyTableViewPanel = document.getElementById("history-table-view");

// Search & Datepicker
const searchInput = document.getElementById("search-input");
const datePickerInput = document.getElementById("date-picker");
const searchResultsGrid = document.getElementById("search-results-grid");
const resultsCountTitle = document.getElementById("results-count-title");
const clearSearchBtn = document.getElementById("clear-search-btn");

// Bookmarks/Selection elements
const selectionResultsGrid = document.getElementById("selection-results-grid");
const selectionCountTitle = document.getElementById("selection-count-title");
const selectionBadgeDesktop = document.getElementById("selection-badge-desktop");
const selectionBadgeMobile = document.getElementById("selection-badge-mobile");

// Modal Elements
const patientModal = document.getElementById("patient-modal");
const modalPatientName = document.getElementById("modal-patient-name");
const modalPatientBody = document.getElementById("modal-patient-body");

// Chart references
let specialtyChartRef = null;
let weeklyChartRef = null;

// Initialize App
function initializeApp() {
    try {
        setupTabNavigation();
        setupViewToggle();
        loadDatabase();
        setupSearchFilters();
    } catch (e) {
        console.error("Critical initialization error:", e);
        // Display error on page so user can see what failed
        const errorDiv = document.createElement("div");
        errorDiv.style.position = "fixed";
        errorDiv.style.top = "0";
        errorDiv.style.left = "0";
        errorDiv.style.width = "100%";
        errorDiv.style.background = "#fef2f2";
        errorDiv.style.color = "#991b1b";
        errorDiv.style.borderBottom = "3px solid #ef4444";
        errorDiv.style.padding = "20px";
        errorDiv.style.zIndex = "99999";
        errorDiv.style.fontFamily = "monospace";
        errorDiv.style.whiteSpace = "pre-wrap";
        errorDiv.innerHTML = `
            <h3 style="margin-bottom: 10px; font-weight: bold;">⚠️ Error de Inicialización Crítico</h3>
            <p style="margin-bottom: 15px;">La aplicación no se pudo cargar debido a un error de JavaScript:</p>
            <code style="background: #ffffff; padding: 10px; display: block; border: 1px solid #fca5a5; border-radius: 4px; overflow: auto; max-height: 200px;">${e.name}: ${e.message}\n${e.stack}</code>
            <p style="margin-top: 15px; font-size: 12px; color: #7f1d1d;">Si está corriendo de forma local, asegúrese de que no haya restricciones de seguridad en su navegador.</p>
        `;
        document.body.appendChild(errorDiv);
    }
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initializeApp);
} else {
    initializeApp();
}

// Tab Navigation Logic (sidebar & bottom mobile nav)
function setupTabNavigation() {
    tabButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            // Remove active class from all buttons and tabs
            tabButtons.forEach(b => b.classList.remove("active"));
            tabContents.forEach(c => c.classList.remove("active"));
            
            const tabId = btn.getAttribute("data-tab");
            activeTab = tabId;
            
            // Mark both sidebar and mobile nav buttons for this tab as active
            document.querySelectorAll(`[data-tab="${tabId}"]`).forEach(b => b.classList.add("active"));
            
            // Show tab content
            document.getElementById(tabId).classList.add("active");
            
            updateHeaderTitles();
            
            if (tabId === "tab-selection") {
                renderBookmarks();
            }
        });
    });
}

function updateHeaderTitles() {
    if (activeTab === "tab-dashboard") {
        currentTabTitle.textContent = "Panel de Estadísticas";
        currentTabSubtitle.textContent = "Resumen analítico de la programación quirúrgica";
        if (specialtyChartRef) specialtyChartRef.resize();
        if (weeklyChartRef) weeklyChartRef.resize();
    } else if (activeTab === "tab-history") {
        currentTabTitle.textContent = "Historial General";
        currentTabSubtitle.textContent = "Navegación jerárquica de turnos por fecha";
    } else if (activeTab === "tab-search") {
        currentTabTitle.textContent = "Búsqueda Detallada";
        currentTabSubtitle.textContent = "Filtrar por fecha y buscar fichas de pacientes";
    } else if (activeTab === "tab-selection") {
        currentTabTitle.textContent = "Mi Selección Personal";
        currentTabSubtitle.textContent = "Seguimiento y control de sus pacientes seleccionados";
    }
}

// Setup View Toggle (Grid vs Table)
function setupViewToggle() {
    btnViewGrid.addEventListener("click", () => {
        historyViewMode = "grid";
        btnViewGrid.classList.add("active");
        btnViewTable.classList.remove("active");
        historyGridViewPanel.classList.add("active");
        historyTableViewPanel.classList.remove("active");
        renderSelectedDays();
    });

    btnViewTable.addEventListener("click", () => {
        historyViewMode = "table";
        btnViewTable.classList.add("active");
        btnViewGrid.classList.remove("active");
        historyTableViewPanel.classList.add("active");
        historyGridViewPanel.classList.remove("active");
        renderSelectedDays();
    });
}

// Fetch & Load Data
async function loadDatabase() {
    try {
        if (window.SURGICAL_DATABASE) {
            console.log("Cargando datos desde window.SURGICAL_DATABASE (CORS-free)");
            database = window.SURGICAL_DATABASE;
        } else {
            console.log("Intentando cargar datos desde fetch('database.json')");
            const response = await fetch("database.json");
            if (!response.ok) {
                throw new Error("No se pudo cargar el archivo database.json");
            }
            database = await response.json();
        }
        
        // Ensure every record has a valid hash
        database.surgeries.forEach(s => {
            if (!s.hash) {
                s.hash = getRecordHash(s);
            }
        });
        
        renderDatabaseStatus();
        renderDashboard();
        renderHistoryTree();
        renderSearchResults(); // Load initial patient grid
        updateBookmarkBadges();
    } catch (error) {
        console.error("Error al cargar base de datos:", error);
        document.getElementById("db-status-info").innerHTML = `
            <p style="color: #ef4444;"><i class="fa-solid fa-triangle-exclamation"></i> Error al cargar datos. Asegúrese de haber ejecutado <code>update_database.py</code> para generar la base de datos.</p>
        `;
    }
}

function getRecordHash(r) {
    const sig = `${r.date}|${r.time_slot}|${r.qx}|${r.specialty}|${r.doctor}|${r.patient}|${r.surgery}`;
    let hash = 0;
    for (let i = 0; i < sig.length; i++) {
        const char = sig.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash; // Convert to 32bit integer
    }
    return Math.abs(hash).toString(16);
}

// Render DB Status Panel
function renderDatabaseStatus() {
    const totalRecords = database.surgeries.length;
    let formattedDate = "Nunca";
    if (database.last_updated) {
        try {
            const lastUpdated = new Date(database.last_updated);
            if (lastUpdated && !isNaN(lastUpdated.getTime())) {
                formattedDate = lastUpdated.toLocaleString("es-AR", { dateStyle: 'short', timeStyle: 'short' });
            }
        } catch (e) {
            console.warn("Error formatting date:", e);
        }
    }
        
    document.getElementById("db-status-info").innerHTML = `
        <p>Registros Históricos: <strong>${totalRecords}</strong></p>
        <p>Última Sincronización: <strong>${formattedDate}</strong></p>
    `;
}

// Helper to split date into Year, Month, Day
function parseDateParts(dateStr) {
    if (!dateStr || typeof dateStr !== 'string') {
        return { day: "??", month: "??", year: "????" };
    }
    const parts = dateStr.split("/");
    if (parts.length === 3) {
        return {
            day: parts[0],
            month: parts[1],
            year: parts[2]
        };
    }
    return { day: "??", month: "??", year: "????" };
}

// Month Number to Spanish Name
const MONTH_NAMES = {
    "01": "Enero", "02": "Febrero", "03": "Marzo", "04": "Abril",
    "05": "Mayo", "06": "Junio", "07": "Julio", "08": "Agosto",
    "09": "Septiembre", "10": "Octubre", "11": "Noviembre", "12": "Diciembre"
};

// 1. Dashboard Tab Functions
function renderDashboard() {
    const activeSurgeries = database.surgeries.filter(s => !s.is_empty_slot);
    const emptySlots = database.surgeries.filter(s => s.is_empty_slot);
    
    kpiActiveSurgeries.textContent = activeSurgeries.length;
    kpiEmptySlots.textContent = emptySlots.length;
    
    const specialtyCounts = {};
    activeSurgeries.forEach(s => {
        specialtyCounts[s.specialty] = (specialtyCounts[s.specialty] || 0) + 1;
    });
    const sortedSpecs = Object.entries(specialtyCounts).sort((a, b) => b[1] - a[1]);
    kpiTopSpecialty.textContent = sortedSpecs.length > 0 ? sortedSpecs[0][0] : "Ninguna";
    
    const doctorCounts = {};
    activeSurgeries.forEach(s => {
        doctorCounts[s.doctor] = (doctorCounts[s.doctor] || 0) + 1;
    });
    const sortedDocs = Object.entries(doctorCounts).sort((a, b) => b[1] - a[1]);
    kpiTopDoctor.textContent = sortedDocs.length > 0 ? `Dr./Dra. ${sortedDocs[0][0]}` : "Ninguno";
    
    renderCharts(sortedSpecs, activeSurgeries);
    renderInsuranceList(activeSurgeries);
    renderStatusList(activeSurgeries);
}

function renderCharts(sortedSpecs, activeSurgeries) {
    if (typeof Chart === 'undefined') {
        console.warn("Chart.js is not loaded. Skipping chart rendering.");
        const chartContainers = document.querySelectorAll(".chart-container");
        chartContainers.forEach(container => {
            const canvas = container.querySelector("canvas");
            if (canvas) {
                const parent = canvas.parentElement;
                parent.innerHTML = `
                    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; color: var(--text-muted); font-size: 13px; font-style: italic; text-align: center; padding: 20px;">
                        <i class="fa-solid fa-triangle-exclamation" style="font-size: 24px; color: var(--warning); margin-bottom: 8px;"></i>
                        Los gráficos no se pueden mostrar sin conexión a Internet (Chart.js CDN inaccesible).
                    </div>
                `;
            }
        });
        return;
    }
    const specLabels = sortedSpecs.map(item => item[0]);
    const specData = sortedSpecs.map(item => item[1]);
    
    const ctxSpecialty = document.getElementById('specialtyChart').getContext('2d');
    if (specialtyChartRef) specialtyChartRef.destroy();
    
    specialtyChartRef = new Chart(ctxSpecialty, {
        type: 'doughnut',
        data: {
            labels: specLabels,
            datasets: [{
                data: specData,
                backgroundColor: [
                    '#2563eb', '#10b981', '#f59e0b', '#ef4444', 
                    '#8b5cf6', '#ec4899', '#14b8a6', '#64748b'
                ],
                borderWidth: 1,
                borderColor: '#ffffff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        font: { family: 'Inter', size: 11 },
                        boxWidth: 12
                    }
                }
            }
        }
    });
    
    const weekCounts = {};
    activeSurgeries.forEach(s => {
        const weekName = s.source_folder_name || "Semana General";
        weekCounts[weekName] = (weekCounts[weekName] || 0) + 1;
    });
    
    const weekLabels = Object.keys(weekCounts).sort((a, b) => a.localeCompare(b));
    const weekData = weekLabels.map(w => weekCounts[w]);
    
    const ctxWeekly = document.getElementById('weeklyChart').getContext('2d');
    if (weeklyChartRef) weeklyChartRef.destroy();
    
    weeklyChartRef = new Chart(ctxWeekly, {
        type: 'line',
        data: {
            labels: weekLabels.map(w => w.replace(" AL ", "-").replace(" DE ", " ")),
            datasets: [{
                label: 'Cirugías Realizadas',
                data: weekData,
                backgroundColor: 'rgba(37, 99, 235, 0.1)',
                borderColor: '#2563eb',
                borderWidth: 3,
                tension: 0.3,
                fill: true,
                pointBackgroundColor: '#2563eb',
                pointRadius: 5
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { stepSize: 2, font: { family: 'Inter', size: 10 } },
                    grid: { color: 'rgba(0, 0, 0, 0.05)' }
                },
                x: {
                    ticks: { font: { family: 'Inter', size: 10 } },
                    grid: { display: false }
                }
            }
        }
    });
}

function renderInsuranceList(activeSurgeries) {
    const insuranceCounts = {};
    activeSurgeries.forEach(s => {
        insuranceCounts[s.insurance] = (insuranceCounts[s.insurance] || 0) + 1;
    });
    const sortedInsurances = Object.entries(insuranceCounts).sort((a, b) => b[1] - a[1]);
    insuranceListContainer.innerHTML = sortedInsurances.map(item => `
        <div class="list-item">
            <span class="list-item-name">${item[0]}</span>
            <span class="list-item-value">${item[1]} cirugías</span>
        </div>
    `).join("");
}

function renderStatusList(activeSurgeries) {
    const statusCounts = {
        "Completa y lista": 0,
        "Sin observaciones (Documentación estándar)": 0,
        "Pendiente - No pasó evaluación prequirúrgica/trámite": 0,
        "Pendiente - Falta pago/autorización de anestesia": 0,
        "Otros / No Especificados": 0
    };
    
    activeSurgeries.forEach(s => {
        const st = (s.status || "").trim().toUpperCase();
        if (!st) {
            statusCounts["Sin observaciones (Documentación estándar)"]++;
        } else if (st.includes("COMPLETA")) {
            statusCounts["Completa y lista"]++;
        } else if (st.includes("NO PASO")) {
            statusCounts["Pendiente - No pasó evaluación prequirúrgica/trámite"]++;
        } else if (st.includes("ANEST")) {
            statusCounts["Pendiente - Falta pago/autorización de anestesia"]++;
        } else {
            statusCounts["Otros / No Especificados"]++;
        }
    });
    
    const total = activeSurgeries.length;
    statusListContainer.innerHTML = Object.entries(statusCounts).map(item => {
        const name = item[0];
        const count = item[1];
        const pct = total > 0 ? (count / total) * 100 : 0;
        
        let colorClass = "";
        if (name.includes("lista") || name.includes("estándar")) colorClass = "#10b981";
        else if (name.includes("anestesia")) colorClass = "#f59e0b";
        else if (name.includes("No pasó")) colorClass = "#ef4444";
        else colorClass = "#64748b";
        
        return `
            <div class="status-item">
                <div class="status-item-header">
                    <span>${name}</span>
                    <strong>${count} (${pct.toFixed(1)}%)</strong>
                </div>
                <div class="status-progress-bar">
                    <div class="status-progress-fill" style="width: ${pct}%; background-color: ${colorClass};"></div>
                </div>
            </div>
        `;
    }).join("");
}

// 2. History Navigation Tree Tab
function renderHistoryTree() {
    const hierarchy = {};
    
    database.surgeries.forEach(s => {
        const parts = parseDateParts(s.date);
        const year = parts.year;
        const monthNum = parts.month;
        const monthName = MONTH_NAMES[monthNum] || monthNum;
        const week = s.source_folder_name || "Semana Desconocida";
        const day = s.date;
        const dayLabel = `${s.day} ${parts.day}/${parts.month}`;
        
        if (!hierarchy[year]) hierarchy[year] = {};
        if (!hierarchy[year][monthName]) hierarchy[year][monthName] = {};
        if (!hierarchy[year][monthName][week]) hierarchy[year][monthName][week] = {};
        if (!hierarchy[year][monthName][week][day]) {
            hierarchy[year][monthName][week][day] = {
                label: dayLabel,
                surgeries: []
            };
        }
        hierarchy[year][monthName][week][day].surgeries.push(s);
    });
    
    let treeHTML = "";
    const sortedYears = Object.keys(hierarchy).sort().reverse();
    for (const year of sortedYears) {
        treeHTML += `
            <div class="tree-node expanded">
                <div class="tree-node-title" onclick="toggleTreeNode(this)"><i class="fa-solid fa-chevron-down"></i> <i class="fa-solid fa-calendar"></i> Año ${year}</div>
                <div class="tree-node-children">
        `;
        
        const sortedMonths = Object.keys(hierarchy[year]).sort();
        for (const month of sortedMonths) {
            treeHTML += `
                <div class="tree-node expanded">
                    <div class="tree-node-title" onclick="toggleTreeNode(this)"><i class="fa-solid fa-chevron-down"></i> <i class="fa-solid fa-calendar-minus"></i> ${month}</div>
                    <div class="tree-node-children">
            `;
            
            const sortedWeeks = Object.keys(hierarchy[year][month]).sort();
            for (const week of sortedWeeks) {
                treeHTML += `
                    <div class="tree-node expanded">
                        <div class="tree-node-title" onclick="toggleTreeNode(this)"><i class="fa-solid fa-chevron-down"></i> <i class="fa-solid fa-folder-open"></i> ${week}</div>
                        <div class="tree-node-children">
                `;
                
                const sortedDays = Object.keys(hierarchy[year][month][week]).sort((a,b) => {
                    const da = a.split("/");
                    const db = b.split("/");
                    return new Date(da[2], da[1], da[0]) - new Date(db[2], db[1], db[0]);
                });
                
                for (const day of sortedDays) {
                    const dayObj = hierarchy[year][month][week][day];
                    const activeCount = dayObj.surgeries.filter(s => !s.is_empty_slot).length;
                    
                    treeHTML += `
                        <div class="tree-node">
                            <div class="tree-node-title leaf" onclick="handleDayTextClick(this)">
                                <input type="checkbox" class="tree-cb" data-day="${day}" onchange="handleDayCheckboxChange(event)">
                                <span>${dayObj.label} (${activeCount})</span>
                            </div>
                        </div>
                    `;
                }
                treeHTML += `</div></div>`;
            }
            treeHTML += `</div></div>`;
        }
        treeHTML += `</div></div>`;
    }
    historyTreeContainer.innerHTML = treeHTML;
    
    // Check and select first day by default
    const firstCheckbox = historyTreeContainer.querySelector(".tree-cb");
    if (firstCheckbox) {
        firstCheckbox.checked = true;
        selectedTreeDays = [firstCheckbox.getAttribute("data-day")];
        firstCheckbox.closest(".tree-node-title.leaf").classList.add("selected");
        renderSelectedDays();
    }
}

window.toggleTreeNode = function(element) {
    const parentNode = element.parentElement;
    parentNode.classList.toggle("expanded");
    const icon = element.querySelector("i.fa-solid");
    if (parentNode.classList.contains("expanded")) {
        icon.className = "fa-solid fa-chevron-down";
    } else {
        icon.className = "fa-solid fa-chevron-right";
    }
};

// Toggle checkbox when clicking text next to it
window.handleDayTextClick = function(element) {
    const cb = element.querySelector(".tree-cb");
    if (cb) {
        cb.checked = !cb.checked;
        // Trigger manual event dispatch for checkbox change
        const event = new Event('change', { bubbles: true });
        cb.dispatchEvent(event);
    }
};

window.handleDayCheckboxChange = function(e) {
    const checkbox = e.target;
    const dateStr = checkbox.getAttribute("data-day");
    const leafTitle = checkbox.closest(".tree-node-title.leaf");
    
    if (checkbox.checked) {
        leafTitle.classList.add("selected");
        if (!selectedTreeDays.includes(dateStr)) {
            selectedTreeDays.push(dateStr);
        }
    } else {
        leafTitle.classList.remove("selected");
        selectedTreeDays = selectedTreeDays.filter(d => d !== dateStr);
    }
    
    renderSelectedDays();
};

function renderSelectedDays() {
    if (selectedTreeDays.length === 0) {
        historySelectionTitle.innerHTML = `<i class="fa-solid fa-calendar-xmark"></i> Sin Selección`;
        tableTotalBadge.textContent = "0 Cirugías";
        historyTableBody.innerHTML = `<tr><td colspan="10" class="empty-table-message">Marque uno o varios días en el navegador temporal.</td></tr>`;
        historyTimelineContainer.innerHTML = `<div class="empty-timeline-message">Marque uno o varios días en el navegador temporal para desplegar las cirugías.</div>`;
        return;
    }
    
    // Sort selected days chronologically
    selectedTreeDays.sort((a, b) => {
        const da = a.split("/");
        const db = b.split("/");
        return new Date(da[2], da[1], da[0]) - new Date(db[2], db[1], db[0]);
    });
    
    // Gather all surgeries for selected days
    const allSelectedSurgeries = database.surgeries.filter(s => selectedTreeDays.includes(s.date));
    
    // Sort all surgeries
    allSelectedSurgeries.sort((a, b) => {
        const da = a.date.split("/");
        const db = b.date.split("/");
        const dateDiff = new Date(da[2], da[1], da[0]) - new Date(db[2], db[1], db[0]);
        if (dateDiff !== 0) return dateDiff;
        return a.time_slot.localeCompare(b.time_slot);
    });
    
    // Title header text
    if (selectedTreeDays.length === 1) {
        historySelectionTitle.innerHTML = `<i class="fa-solid fa-calendar-check"></i> Agenda del Día: <strong>${selectedTreeDays[0]}</strong>`;
    } else {
        historySelectionTitle.innerHTML = `<i class="fa-solid fa-calendar-days"></i> Rango: <strong>${selectedTreeDays[0]}</strong> al <strong>${selectedTreeDays[selectedTreeDays.length - 1]}</strong>`;
    }
    
    const activeCount = allSelectedSurgeries.filter(s => !s.is_empty_slot).length;
    tableTotalBadge.textContent = `${activeCount} Cirugías / ${allSelectedSurgeries.length} Total`;
    
    if (historyViewMode === "table") {
        renderClassicTable(allSelectedSurgeries);
    } else {
        renderTimelineGrid(allSelectedSurgeries);
    }
}

// Render Classic Table
function renderClassicTable(surgeries) {
    if (surgeries.length === 0) {
        historyTableBody.innerHTML = `<tr><td colspan="10" class="empty-table-message">No hay programaciones registradas para el período.</td></tr>`;
        return;
    }
    
    historyTableBody.innerHTML = surgeries.map(s => {
        let statusBadgeClass = "pendiente";
        let statusLabel = s.status || "Pendiente";
        const st = (s.status || "").toUpperCase();
        
        if (s.is_empty_slot) {
            statusBadgeClass = "pendiente";
            statusLabel = "RESERVADO";
        } else if (!s.status) {
            statusBadgeClass = "completa";
            statusLabel = "ESTÁNDAR";
        } else if (st.includes("COMPLETA")) {
            statusBadgeClass = "completa";
        } else if (st.includes("NO PASO")) {
            statusBadgeClass = "incompleta";
        } else if (st.includes("ANEST")) {
            statusBadgeClass = "incompleta";
        }
        
        const qxVal = s.qx ? s.qx : "-";
        const isFav = isBookmarked(s.hash);
        
        const patientName = s.is_empty_slot 
            ? `<em style="color: var(--text-muted);">Bloque Médico Reservado</em>`
            : `<strong>${s.patient}</strong> <span style="font-size: 10.5px; color: var(--text-muted); display: block;">DNI: ${s.dni || "-"} | ${s.age || "-"} años</span>`;
            
        return `
            <tr class="${s.is_empty_slot ? 'row-reserved-slot' : 'row-clickable'}" onclick="handleRowClick(event, '${s.hash}', ${s.is_empty_slot})">
                <td onclick="event.stopPropagation()">
                    <button class="bookmark-btn-table ${isFav ? 'active' : ''}" onclick="toggleBookmark('${s.hash}', this)">
                        <i class="${isFav ? 'fa-solid' : 'fa-regular'} fa-star"></i>
                    </button>
                </td>
                <td>${s.date}</td>
                <td><strong>${s.time_slot}</strong></td>
                <td><span class="badge" style="background-color: #f1f5f9; color: var(--bg-sidebar); border: 1px solid #cbd5e1;">${qxVal}</span></td>
                <td>${s.specialty}</td>
                <td>Dr./Dra. ${s.doctor}</td>
                <td>${patientName}</td>
                <td>${s.surgery || "-"}</td>
                <td>${s.insurance}</td>
                <td><span class="status-badge ${statusBadgeClass}">${statusLabel}</span></td>
            </tr>
        `;
    }).join("");
}

window.handleRowClick = function(event, hash, isEmpty) {
    if (isEmpty) return;
    openPatientModal(hash);
};

// Render Visual Timeline / Quirófanos Grid (Supports multi-day rendering)
function renderTimelineGrid(surgeries) {
    if (surgeries.length === 0) {
        historyTimelineContainer.innerHTML = `<div class="empty-timeline-message">No hay programaciones registradas para el período.</div>`;
        return;
    }
    
    // Group surgeries by Date first, then by Time Slot
    const dayGroups = {};
    surgeries.forEach(s => {
        if (!dayGroups[s.date]) {
            dayGroups[s.date] = {};
        }
        if (!dayGroups[s.date][s.time_slot]) {
            dayGroups[s.date][s.time_slot] = [];
        }
        dayGroups[s.date][s.time_slot].push(s);
    });
    
    let html = "";
    const sortedDates = Object.keys(dayGroups).sort((a, b) => {
        const da = a.split("/");
        const db = b.split("/");
        return new Date(da[2], da[1], da[0]) - new Date(db[2], db[1], db[0]);
    });
    
    for (const dateVal of sortedDates) {
        const dateParts = parseDateParts(dateVal);
        const dayLabel = surgeries.find(s => s.date === dateVal).day;
        
        html += `
            <div class="timeline-day-section">
                <div class="timeline-day-title">
                    <i class="fa-solid fa-calendar-check"></i> ${dayLabel} ${dateParts.day}/${dateParts.month}/${dateParts.year}
                </div>
        `;
        
        const slotsMap = dayGroups[dateVal];
        const sortedSlots = Object.keys(slotsMap).sort((a,b) => a.localeCompare(b));
        
        for (const timeSlot of sortedSlots) {
            const slotSurgeries = slotsMap[timeSlot];
            const isStandardShift = timeSlot.includes("a") && (timeSlot.includes("10") || timeSlot.includes("12") || timeSlot.includes("14"));
            
            html += `
                <div class="timeline-row">
                    <div class="timeline-row-header">
                        <span><i class="fa-regular fa-clock"></i> Horario: ${timeSlot}</span>
                        <span style="font-size: 11px; opacity: 0.8;">Programadas: ${slotSurgeries.length}</span>
                    </div>
            `;
            
            if (isStandardShift) {
                html += `<div class="timeline-grid-layout">`;
                for (const qx of ["Q1", "Q2", "Q3"]) {
                    const surg = slotSurgeries.find(s => s.qx === qx);
                    if (surg) {
                        html += renderQuirofanoCard(surg, qx);
                    } else {
                        html += `
                            <div class="quirofano-card empty">
                                <span>Quirófano ${qx}: Disponible</span>
                            </div>
                        `;
                    }
                }
                html += `</div>`;
            } else {
                html += `<div class="non-standard-list">`;
                slotSurgeries.forEach(surg => {
                    html += renderQuirofanoCard(surg, surg.qx || "Local");
                });
                html += `</div>`;
            }
            
            html += `</div>`; // Close row
        }
        
        html += `</div>`; // Close day section
    }
    
    historyTimelineContainer.innerHTML = html;
}

function renderQuirofanoCard(s, qxName) {
    let statusColor = "yellow";
    let statusLabel = s.status || "Pendiente";
    const st = (s.status || "").toUpperCase();
    
    if (s.is_empty_slot) {
        statusColor = "yellow";
        statusLabel = "Bloque Reservado";
    } else if (!s.status) {
        statusColor = "green";
        statusLabel = "Lista";
    } else if (st.includes("COMPLETA")) {
        statusColor = "green";
        statusLabel = "Lista";
    } else if (st.includes("NO PASO")) {
        statusColor = "red";
        statusLabel = "No pasó prequirúrgico";
    } else if (st.includes("ANEST")) {
        statusColor = "red";
        statusLabel = "Falta anestesia";
    }
    
    const isFav = isBookmarked(s.hash);
    const clickHandler = s.is_empty_slot ? "" : `onclick="openPatientModal('${s.hash}')"`;
    
    if (s.is_empty_slot) {
        return `
            <div class="quirofano-card row-reserved-slot" style="border-left: 4px solid var(--warning);">
                <div class="quirofano-card-header">
                    <span class="qx-tag">${qxName}</span>
                    <span class="quirofano-status"><span class="status-dot yellow"></span> RESERVADO</span>
                </div>
                <div class="quirofano-card-body">
                    <span class="quirofano-patient" style="font-style: italic; font-weight: 500; color: var(--text-muted);">Bloque Médico</span>
                    <span class="quirofano-surgery">Dr./Dra. ${s.doctor}</span>
                    <span class="quirofano-details">${s.specialty}</span>
                </div>
            </div>
        `;
    }
    
    return `
        <div class="quirofano-card" style="border-left: 4px solid ${statusColor === 'green' ? 'var(--success)' : (statusColor === 'red' ? 'var(--danger)' : 'var(--warning)')};" ${clickHandler}>
            <button class="bookmark-btn ${isFav ? 'active' : ''}" onclick="event.stopPropagation(); toggleBookmark('${s.hash}', this)">
                <i class="${isFav ? 'fa-solid' : 'fa-regular'} fa-star"></i>
            </button>
            <div class="quirofano-card-header">
                <span class="qx-tag">${qxName}</span>
                <span class="quirofano-status"><span class="status-dot ${statusColor}"></span> ${statusLabel}</span>
            </div>
            <div class="quirofano-card-body">
                <span class="quirofano-patient">${s.patient}</span>
                <span class="quirofano-surgery">${s.surgery || "Procedimiento no descripto"}</span>
                <span class="quirofano-details">Dr./Dra. ${s.doctor} | ${s.specialty}</span>
                <span class="quirofano-details" style="font-size: 9.5px; margin-top: 2px;"><i class="fa-solid fa-shield-halved"></i> ${s.insurance}</span>
            </div>
        </div>
    `;
}

// 3. Search and Detailed Picker Tab
function setupSearchFilters() {
    searchInput.addEventListener("input", filterSearchResults);
    datePickerInput.addEventListener("change", filterSearchResults);
    
    clearSearchBtn.addEventListener("click", () => {
        searchInput.value = "";
        datePickerInput.value = "";
        filterSearchResults();
    });
}

function filterSearchResults() {
    const q = searchInput.value.toLowerCase().trim();
    const dateQuery = datePickerInput.value;
    
    let formattedDateQuery = "";
    if (dateQuery) {
        const dateParts = dateQuery.split("-");
        if (dateParts.length === 3) {
            formattedDateQuery = `${dateParts[2]}/${dateParts[1]}/${dateParts[0]}`;
        }
    }
    
    const filtered = database.surgeries.filter(s => {
        if (formattedDateQuery && s.date !== formattedDateQuery) {
            return false;
        }
        
        if (q) {
            const nameMatch = s.patient.toLowerCase().includes(q);
            const dniMatch = s.dni.toLowerCase().includes(q);
            const docMatch = s.doctor.toLowerCase().includes(q);
            const specMatch = s.specialty.toLowerCase().includes(q);
            const insMatch = s.insurance.toLowerCase().includes(q);
            const surgMatch = s.surgery.toLowerCase().includes(q);
            const dateMatch = s.date.includes(q);
            
            return nameMatch || dniMatch || docMatch || specMatch || insMatch || surgMatch || dateMatch;
        }
        
        return true;
    });
    
    renderPatientCards(filtered, searchResultsGrid);
}

function renderSearchResults() {
    renderPatientCards(database.surgeries, searchResultsGrid);
}

function renderPatientCards(surgeries, targetGridContainer) {
    const activeOnly = surgeries.filter(s => !s.is_empty_slot);
    
    if (targetGridContainer === searchResultsGrid) {
        resultsCountTitle.innerHTML = `<i class="fa-solid fa-list-check"></i> Turnos Programados: <strong>${activeOnly.length} pacientes</strong> en total`;
    }
    
    if (activeOnly.length === 0) {
        targetGridContainer.innerHTML = `
            <div class="empty-results">
                <i class="fa-solid fa-user-slash" style="font-size: 32px; color: var(--text-muted); display: block; margin-bottom: 12px;"></i>
                No se encontraron pacientes.
            </div>
        `;
        return;
    }
    
    // Sort chronologically
    activeOnly.sort((a,b) => {
        const da = a.date.split("/");
        const db = b.date.split("/");
        const dateDiff = new Date(da[2], da[1], da[0]) - new Date(db[2], db[1], db[0]);
        if (dateDiff !== 0) return dateDiff;
        return a.time_slot.localeCompare(b.time_slot);
    });
    
    targetGridContainer.innerHTML = activeOnly.map(s => {
        let statusBadgeClass = "pendiente";
        let statusLabel = s.status || "Pendiente";
        const st = (s.status || "").toUpperCase();
        
        if (!s.status) {
            statusBadgeClass = "completa";
            statusLabel = "ESTÁNDAR (Sin Obs)";
        } else if (st.includes("COMPLETA")) {
            statusBadgeClass = "completa";
        } else if (st.includes("NO PASO")) {
            statusBadgeClass = "incompleta";
        } else if (st.includes("ANEST")) {
            statusBadgeClass = "incompleta";
        }
        
        const isFav = isBookmarked(s.hash);
        
        return `
            <div class="patient-card glass" style="border-top: 4px solid ${statusBadgeClass === 'completa' ? 'var(--success)' : (statusBadgeClass === 'incompleta' ? 'var(--danger)' : 'var(--warning)')};" onclick="openPatientModal('${s.hash}')">
                <button class="bookmark-btn ${isFav ? 'active' : ''}" onclick="event.stopPropagation(); toggleBookmark('${s.hash}', this)">
                    <i class="${isFav ? 'fa-solid' : 'fa-regular'} fa-star"></i>
                </button>
                <div class="patient-card-header">
                    <div class="patient-name-block">
                        <h4>${s.patient}</h4>
                        <span>DNI: ${s.dni || "No informado"} | Edad: ${s.age || "-"} años</span>
                    </div>
                    <span class="status-badge ${statusBadgeClass}">${statusLabel}</span>
                </div>
                
                <div class="patient-info-list">
                    <div class="info-item">
                        <span class="info-label">Fecha y Hora</span>
                        <span class="info-value"><i class="fa-regular fa-calendar-days"></i> ${s.date} - ${s.time_slot}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Quirófano</span>
                        <span class="info-value"><i class="fa-solid fa-door-open"></i> Quirófano ${s.qx || "Local"}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Especialidad</span>
                        <span class="info-value">${s.specialty}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Cirujano</span>
                        <span class="info-value">Dr./Dra. ${s.doctor}</span>
                    </div>
                    <div class="info-item" style="grid-column: span 2;">
                        <span class="info-label">Cirugía / Procedimiento</span>
                        <span class="info-value" style="color: var(--primary); font-weight: 600;">${s.surgery || "No descripto"}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Obra Social / Cobertura</span>
                        <span class="info-value">${s.insurance}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Anestesiología / RX</span>
                        <span class="info-value">Anestesia: ${s.anesthesia || "No"} | RX: ${s.rx || "No"}</span>
                    </div>
                </div>
                
                <div class="patient-card-footer">
                    <span><i class="fa-solid fa-folder"></i> Carpeta: ${s.source_folder_name}</span>
                </div>
            </div>
        `;
    }).join("");
}

// 4. Custom Selection ("Mi Selección") Logic
window.toggleBookmark = function(hash, element) {
    const isFav = bookmarkedSurgeries.includes(hash);
    
    if (isFav) {
        bookmarkedSurgeries = bookmarkedSurgeries.filter(h => h !== hash);
        element.classList.remove("active");
        const icon = element.querySelector("i");
        if (icon) icon.className = "fa-regular fa-star";
    } else {
        bookmarkedSurgeries.push(hash);
        element.classList.add("active");
        const icon = element.querySelector("i");
        if (icon) icon.className = "fa-solid fa-star";
    }
    
    try {
        localStorage.setItem("bookmarked_surgeries", JSON.stringify(bookmarkedSurgeries));
    } catch (e) {
        console.warn("Could not save to localStorage:", e);
    }
    updateBookmarkBadges();
    
    // If we are on the selection tab, redraw immediately
    if (activeTab === "tab-selection") {
        renderBookmarks();
    } else {
        // Redraw current view to synchronize star state in other tabs
        renderSelectedDays();
        filterSearchResults();
    }
};

function isBookmarked(hash) {
    return bookmarkedSurgeries.includes(hash);
}

function updateBookmarkBadges() {
    const count = bookmarkedSurgeries.length;
    selectionBadgeDesktop.textContent = count;
    selectionBadgeMobile.textContent = count;
    
    if (count > 0) {
        selectionBadgeDesktop.style.display = "inline-block";
        selectionBadgeMobile.style.display = "flex";
    } else {
        selectionBadgeDesktop.style.display = "none";
        selectionBadgeMobile.style.display = "none";
    }
}

function renderBookmarks() {
    const bookmarkedList = database.surgeries.filter(s => bookmarkedSurgeries.includes(s.hash));
    selectionCountTitle.innerHTML = `<i class="fa-solid fa-star" style="color: var(--warning);"></i> Pacientes Seleccionados: <strong>${bookmarkedList.length}</strong>`;
    
    if (bookmarkedList.length === 0) {
        selectionResultsGrid.innerHTML = `
            <div class="empty-results">
                <i class="fa-regular fa-star" style="font-size: 32px; color: var(--text-muted); display: block; margin-bottom: 12px;"></i>
                No ha seleccionado ningún paciente aún. Marque la estrella en los listados para agregarlos aquí.
            </div>
        `;
        return;
    }
    
    renderPatientCards(bookmarkedList, selectionResultsGrid);
}

// 5. Individual Patient Profile Modal Logic
window.openPatientModal = function(hash) {
    const s = database.surgeries.find(item => item.hash === hash);
    if (!s) return;
    
    let statusClass = "pendiente";
    let statusLabel = s.status || "Pendiente de evaluación";
    const st = (s.status || "").toUpperCase();
    
    if (!s.status) {
        statusClass = "completa";
        statusLabel = "Documentación Estándar Aprobada";
    } else if (st.includes("COMPLETA")) {
        statusClass = "completa";
        statusLabel = s.status;
    } else if (st.includes("NO PASO")) {
        statusClass = "incompleta";
        statusLabel = s.status;
    } else if (st.includes("ANEST")) {
        statusClass = "incompleta";
        statusLabel = s.status;
    }
    
    modalPatientName.textContent = s.patient;
    
    modalPatientBody.innerHTML = `
        <div class="modal-section">
            <div class="modal-section-title">Datos Personales</div>
            <div class="modal-info-grid">
                <div class="modal-val-box">
                    <span class="info-label">DNI / Identificación</span>
                    <span class="info-value" style="font-size: 14px;">${s.dni || "No informado"}</span>
                </div>
                <div class="modal-val-box">
                    <span class="info-label">Edad del Paciente</span>
                    <span class="info-value" style="font-size: 14px;">${s.age || "-"} años</span>
                </div>
                <div class="modal-val-box modal-block-full">
                    <span class="info-label">Teléfono de Contacto</span>
                    <span class="info-value" style="font-size: 14px;"><i class="fa-solid fa-phone"></i> ${s.phone || "No especificado"}</span>
                </div>
            </div>
        </div>
        
        <div class="modal-section">
            <div class="modal-section-title">Programación Quirúrgica</div>
            <div class="modal-info-grid">
                <div class="modal-val-box">
                    <span class="info-label">Fecha Programada</span>
                    <span class="info-value" style="font-size: 14px;"><i class="fa-regular fa-calendar"></i> ${s.date} (${s.day})</span>
                </div>
                <div class="modal-val-box">
                    <span class="info-label">Horario / Shift</span>
                    <span class="info-value" style="font-size: 14px;"><i class="fa-regular fa-clock"></i> ${s.time_slot}</span>
                </div>
                <div class="modal-val-box">
                    <span class="info-label">Especialidad</span>
                    <span class="info-value" style="font-size: 14px;">${s.specialty}</span>
                </div>
                <div class="modal-val-box">
                    <span class="info-label">Quirófano Asignado</span>
                    <span class="info-value" style="font-size: 14px;"><span class="badge" style="background-color: var(--bg-sidebar); color: var(--text-white); font-weight: 700;">Quirófano ${s.qx || "Local"}</span></span>
                </div>
                <div class="modal-val-box modal-block-full">
                    <span class="info-label">Cirujano Responsable</span>
                    <span class="info-value" style="font-size: 15px; font-weight: 700;"><i class="fa-solid fa-user-doctor"></i> Dr./Dra. ${s.doctor}</span>
                </div>
                <div class="modal-val-box modal-block-full" style="background-color: var(--primary-light); border-color: rgba(37,99,235,0.2);">
                    <span class="info-label" style="color: var(--primary);">Cirugía a Realizar</span>
                    <span class="info-value" style="font-size: 16px; color: var(--primary); font-weight: 700;">${s.surgery || "No descripta"}</span>
                </div>
            </div>
        </div>
        
        <div class="modal-section">
            <div class="modal-section-title">Detalles Clínicos & Cobertura</div>
            <div class="modal-info-grid">
                <div class="modal-val-box modal-block-full">
                    <span class="info-label">Diagnóstico / Dolencia</span>
                    <span class="info-value">${s.ailment || "No especificado"}</span>
                </div>
                <div class="modal-val-box">
                    <span class="info-label">Obra Social / Cobertura</span>
                    <span class="info-value" style="font-weight: 700;">${s.insurance}</span>
                </div>
                <div class="modal-val-box">
                    <span class="info-label">Anestesiología & RX</span>
                    <span class="info-value">Anestesia: ${s.anesthesia || "No"} | RX: ${s.rx || "No"}</span>
                </div>
                <div class="modal-val-box">
                    <span class="info-label">Cajas / Materiales Pcte</span>
                    <span class="info-value">${s.boxes || "-"}</span>
                </div>
                <div class="modal-val-box">
                    <span class="info-label">Estado de Documentación</span>
                    <span class="status-badge ${statusClass}" style="margin-top: 6px;">${statusLabel}</span>
                </div>
            </div>
        </div>
        
        <div class="modal-section" style="margin-bottom: 0;">
            <div class="modal-section-title">Origen de la Información</div>
            <div class="modal-info-grid">
                <div class="modal-val-box modal-block-full" style="background: #f8fafc; font-size: 11px; color: var(--text-muted);">
                    <p><i class="fa-solid fa-folder"></i> Carpeta en Drive: <strong>${s.source_folder_name}</strong></p>
                    <p style="margin-top: 4px;"><i class="fa-solid fa-file-excel"></i> Planilla origen: <strong>${s.source_sheet_name}</strong></p>
                </div>
            </div>
        </div>
    `;
    
    patientModal.classList.add("active");
    document.body.style.overflow = "hidden"; // Block background scroll
};

window.closePatientModal = function() {
    patientModal.classList.remove("active");
    document.body.style.overflow = ""; // Restore scroll
};

window.handleModalOverlayClick = function(event) {
    // Close modal if clicked outside the card
    if (event.target === patientModal) {
        closePatientModal();
    }
};

// Polyfill helper in case String.prototype.includes is not supported
if (!String.prototype.includes) {
    String.prototype.includes = function(search, start) {
        if (typeof start !== 'number') {
            start = 0;
        }
        if (start + search.length > this.length) {
            return false;
        } else {
            return this.indexOf(search, start) !== -1;
        }
    };
}
