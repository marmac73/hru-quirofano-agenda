# Overwriting index.html with new responsive bottom nav, patient selection tab, and patient detail modal
index_html_content = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Historial de Turnos Quirúrgicos - Hospital Regional Ushuaia</title>
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    
    <!-- FontAwesome for Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <!-- Chart.js for analytics -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    
    <!-- Stylesheet -->
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="app-container">
        <!-- Sidebar (Desktop only) -->
        <aside class="app-sidebar">
            <div class="sidebar-header">
                <div class="logo-icon"><i class="fa-solid fa-hospital-user"></i></div>
                <div class="logo-text">
                    <h1>HRU Quirófano</h1>
                    <span>Historial & Gestión</span>
                </div>
            </div>
            
            <nav class="sidebar-nav">
                <button class="nav-btn active" data-tab="tab-dashboard">
                    <i class="fa-solid fa-chart-line"></i> Estadísticas
                </button>
                <button class="nav-btn" data-tab="tab-history">
                    <i class="fa-solid fa-folder-tree"></i> Historial General
                </button>
                <button class="nav-btn" data-tab="tab-search">
                    <i class="fa-solid fa-magnifying-glass"></i> Buscar Turno
                </button>
                <button class="nav-btn" data-tab="tab-selection">
                    <i class="fa-solid fa-star"></i> Mi Selección <span id="selection-badge-desktop" class="badge-count">0</span>
                </button>
            </nav>
            
            <div class="sidebar-footer">
                <div class="db-status-card">
                    <div class="db-status-header">
                        <i class="fa-solid fa-database"></i>
                        <span>Estado de Base de Datos</span>
                    </div>
                    <div id="db-status-info">
                        <p>Cargando datos...</p>
                    </div>
                    <div class="sync-instruction">
                        <p><i class="fa-solid fa-circle-info"></i> Para sincronizar nuevos datos de Google Drive, ejecute:</p>
                        <code>python update_database.py</code>
                    </div>
                </div>
            </div>
        </aside>

        <!-- Main Content Area -->
        <main class="app-content">
            <!-- Top Navbar -->
            <header class="app-header">
                <div class="header-title">
                    <h2 id="current-tab-title">Panel de Estadísticas</h2>
                    <p id="current-tab-subtitle">Resumen analítico de la programación quirúrgica</p>
                </div>
                <div class="header-actions">
                    <span class="location-badge"><i class="fa-solid fa-location-dot"></i> HRU Ushuaia</span>
                </div>
            </header>
            
            <!-- Dashboard Tab -->
            <section id="tab-dashboard" class="tab-content active">
                <div class="kpi-grid">
                    <div class="kpi-card glass">
                        <div class="kpi-icon icon-blue"><i class="fa-solid fa-user-check"></i></div>
                        <div class="kpi-info">
                            <span class="kpi-label">Cirugías Programadas</span>
                            <h3 class="kpi-value" id="kpi-active-surgeries">-</h3>
                        </div>
                    </div>
                    <div class="kpi-card glass">
                        <div class="kpi-icon icon-green"><i class="fa-solid fa-calendar-check"></i></div>
                        <div class="kpi-info">
                            <span class="kpi-label">Turnos Libres/Reservas</span>
                            <h3 class="kpi-value" id="kpi-empty-slots">-</h3>
                        </div>
                    </div>
                    <div class="kpi-card glass">
                        <div class="kpi-icon icon-orange"><i class="fa-solid fa-stethoscope"></i></div>
                        <div class="kpi-info">
                            <span class="kpi-label">Especialidad Líder</span>
                            <h3 class="kpi-value" id="kpi-top-specialty">-</h3>
                        </div>
                    </div>
                    <div class="kpi-card glass">
                        <div class="kpi-icon icon-red"><i class="fa-solid fa-user-doctor"></i></div>
                        <div class="kpi-info">
                            <span class="kpi-label">Médico Más Activo</span>
                            <h3 class="kpi-value" id="kpi-top-doctor">-</h3>
                        </div>
                    </div>
                </div>
                
                <div class="dashboard-grid">
                    <div class="chart-container glass">
                        <h4>Distribución por Especialidades Médicas</h4>
                        <div class="chart-wrapper">
                            <canvas id="specialtyChart"></canvas>
                        </div>
                    </div>
                    <div class="chart-container glass">
                        <h4>Volumen de Cirugías por Semana</h4>
                        <div class="chart-wrapper">
                            <canvas id="weeklyChart"></canvas>
                        </div>
                    </div>
                </div>
                
                <div class="dashboard-secondary-grid">
                    <div class="list-container glass">
                        <h4>Distribución por Cobertura / Obra Social</h4>
                        <div class="list-wrapper" id="insurance-list">
                            <!-- List injected dynamically -->
                        </div>
                    </div>
                    <div class="list-container glass">
                        <h4>Estado de Documentación / Preparación</h4>
                        <div class="list-wrapper" id="status-list">
                            <!-- List injected dynamically -->
                        </div>
                    </div>
                </div>
            </section>
            
            <!-- History Navigation Tab -->
            <section id="tab-history" class="tab-content">
                <div class="history-grid">
                    <div class="history-tree-card glass">
                        <h3><i class="fa-solid fa-calendar-days"></i> Navegador Temporal</h3>
                        <p class="history-tip"><i class="fa-solid fa-check-double"></i> Seleccione uno o varios días para ver y comparar agendas.</p>
                        <div class="tree-container" id="history-tree">
                            <!-- Hierarchical tree with checkboxes will be injected here -->
                        </div>
                    </div>
                    
                    <div class="history-table-card glass">
                        <div class="table-header">
                            <h3 id="history-selection-title">Agenda del Quirófano</h3>
                            <div class="header-controls">
                                <span class="badge" id="table-total-badge">0 Cirugías</span>
                                <div class="view-toggle">
                                    <button id="btn-view-grid" class="toggle-btn active"><i class="fa-solid fa-table-cells-large"></i> Grilla</button>
                                    <button id="btn-view-table" class="toggle-btn"><i class="fa-solid fa-list"></i> Tabla</button>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Visual Timeline Grid View -->
                        <div id="history-grid-view" class="history-view-panel active">
                            <div class="timeline-container" id="history-timeline-container">
                                <div class="empty-timeline-message">Marque uno o varios días en el navegador temporal para desplegar las cirugías.</div>
                            </div>
                        </div>
                        
                        <!-- Classic Table View -->
                        <div id="history-table-view" class="history-view-panel">
                            <div class="table-wrapper">
                                <table id="history-table">
                                    <thead>
                                        <tr>
                                            <th>Acciones</th>
                                            <th>Fecha</th>
                                            <th>Hora</th>
                                            <th>Quirófano</th>
                                            <th>Especialidad</th>
                                            <th>Cirujano</th>
                                            <th>Paciente / DNI</th>
                                            <th>Cirugía / Procedimiento</th>
                                            <th>Obra Social</th>
                                            <th>Observación</th>
                                        </tr>
                                    </thead>
                                    <tbody id="history-table-body">
                                        <tr>
                                            <td colspan="10" class="empty-table-message">Marque uno o varios días en el árbol de navegación temporal.</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
            
            <!-- Detailed Search Tab -->
            <section id="tab-search" class="tab-content">
                <div class="search-controls glass">
                    <div class="search-form-row">
                        <div class="form-group flex-2">
                            <label for="search-input"><i class="fa-solid fa-magnifying-glass"></i> Buscar por nombre, DNI, médico o especialidad</label>
                            <input type="text" id="search-input" placeholder="Escriba paciente, DNI, cirujano, obra social...">
                        </div>
                        <div class="form-group flex-1">
                            <label for="date-picker"><i class="fa-solid fa-calendar"></i> Selector de Fecha</label>
                            <input type="date" id="date-picker">
                        </div>
                        <div class="form-group-btn">
                            <button id="clear-search-btn" class="btn-secondary">Limpiar Filtros</button>
                        </div>
                    </div>
                </div>
                
                <div class="search-results-section">
                    <div class="results-header">
                        <h3 id="results-count-title">Todos los Turnos</h3>
                    </div>
                    <div class="patient-grid" id="search-results-grid">
                        <!-- Patient detail cards injected dynamically -->
                        <div class="empty-results">Cargando turnos quirúrgicos...</div>
                    </div>
                </div>
            </section>
            
            <!-- Custom Selection Tab -->
            <section id="tab-selection" class="tab-content">
                <div class="selection-intro glass">
                    <h3><i class="fa-solid fa-star" style="color: var(--warning);"></i> Mi Selección Quirúrgica</h3>
                    <p>Esta sección almacena su lista personalizada de pacientes marcados. Úselo para realizar el seguimiento de pacientes a su cargo, programados para su quirófano, o de interés clínico. Esta lista se almacena automáticamente en este equipo.</p>
                </div>
                
                <div class="search-results-section" style="margin-top: 32px;">
                    <div class="results-header">
                        <h3 id="selection-count-title">0 Pacientes en su Selección</h3>
                    </div>
                    <div class="patient-grid" id="selection-results-grid">
                        <div class="empty-results">No ha seleccionado ningún paciente aún. Agregue pacientes marcando el ícono de estrella <i class="fa-regular fa-star"></i> en las vistas de búsqueda o historial.</div>
                    </div>
                </div>
            </section>
        </main>
        
        <!-- Mobile Bottom Navigation Bar -->
        <nav class="mobile-nav">
            <button class="mobile-nav-btn active" data-tab="tab-dashboard">
                <i class="fa-solid fa-chart-line"></i>
                <span>Estadísticas</span>
            </button>
            <button class="mobile-nav-btn" data-tab="tab-history">
                <i class="fa-solid fa-folder-tree"></i>
                <span>Historial</span>
            </button>
            <button class="mobile-nav-btn" data-tab="tab-search">
                <i class="fa-solid fa-magnifying-glass"></i>
                <span>Buscar</span>
            </button>
            <button class="mobile-nav-btn" data-tab="tab-selection">
                <i class="fa-solid fa-star"></i>
                <span>Selección</span>
                <span id="selection-badge-mobile" class="badge-count-mobile">0</span>
            </button>
        </nav>
    </div>
    
    <!-- Detailed Patient Profile Modal -->
    <div id="patient-modal" class="modal-overlay" onclick="handleModalOverlayClick(event)">
        <div class="modal-card glass">
            <div class="modal-header">
                <div class="modal-header-title">
                    <span class="modal-subtitle"><i class="fa-solid fa-address-card"></i> Ficha Quirúrgica Individual</span>
                    <h3 id="modal-patient-name">Fidele Patricia</h3>
                </div>
                <button class="modal-close-btn" onclick="closePatientModal()"><i class="fa-solid fa-xmark"></i></button>
            </div>
            <div class="modal-body" id="modal-patient-body">
                <!-- Infomation injected dynamically -->
            </div>
        </div>
    </div>
</body>
</html>"""

# Overwriting styles.css with responsive mobile nav, patient modal popup, bookmark buttons, and layouts
styles_css_content = """/* Core Design System Variables */
:root {
    --bg-main: #f0f3f8;
    --bg-sidebar: #0f172a;
    --text-main: #334155;
    --text-muted: #64748b;
    --text-white: #ffffff;
    --primary: #2563eb;
    --primary-light: #eff6ff;
    --primary-hover: #1d4ed8;
    --success: #10b981;
    --success-light: #ecfdf5;
    --warning: #f59e0b;
    --warning-light: #fffbeb;
    --danger: #ef4444;
    --danger-light: #fef2f2;
    --border-color: rgba(226, 232, 240, 0.8);
    --card-bg: rgba(255, 255, 255, 0.8);
    --glass-border: rgba(255, 255, 255, 0.6);
    --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.04);
    --shadow-md: 0 8px 30px rgba(0, 0, 0, 0.06);
    --shadow-lg: 0 10px 40px rgba(31, 38, 135, 0.06);
    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 16px;
    --font-heading: 'Outfit', sans-serif;
    --font-body: 'Inter', sans-serif;
    --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Reset */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: var(--font-body);
    background-color: var(--bg-main);
    color: var(--text-main);
    height: 100vh;
    overflow: hidden;
}

/* App Container Layout */
.app-container {
    display: flex;
    height: 100vh;
    width: 100vw;
}

/* Sidebar Styling (Desktop) */
.app-sidebar {
    width: 280px;
    background-color: var(--bg-sidebar);
    color: var(--text-white);
    display: flex;
    flex-direction: column;
    flex-shrink: 0;
    padding: 24px;
    z-index: 10;
    box-shadow: 4px 0 25px rgba(0, 0, 0, 0.15);
}

.sidebar-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 40px;
}

.logo-icon {
    font-size: 24px;
    color: #38bdf8;
    background: rgba(56, 189, 248, 0.1);
    padding: 10px;
    border-radius: var(--radius-md);
    border: 1px solid rgba(56, 189, 248, 0.2);
}

.logo-text h1 {
    font-family: var(--font-heading);
    font-size: 18px;
    font-weight: 700;
    letter-spacing: 0.5px;
}

.logo-text span {
    font-size: 11px;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.sidebar-nav {
    display: flex;
    flex-direction: column;
    gap: 8px;
    flex: 1;
}

.nav-btn {
    background: none;
    border: none;
    color: #94a3b8;
    padding: 14px 16px;
    border-radius: var(--radius-md);
    font-family: var(--font-body);
    font-size: 14px;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 12px;
    cursor: pointer;
    text-align: left;
    transition: var(--transition);
    position: relative;
    min-height: 48px; /* Touch target */
}

.nav-btn i {
    font-size: 18px;
    width: 20px;
    text-align: center;
}

.nav-btn:hover {
    color: var(--text-white);
    background-color: rgba(255, 255, 255, 0.05);
}

.nav-btn.active {
    color: var(--text-white);
    background-color: var(--primary);
    box-shadow: 0 4px 20px rgba(37, 99, 235, 0.3);
}

/* Badge Count in Navigation */
.badge-count {
    background: var(--warning);
    color: var(--bg-sidebar);
    font-size: 11px;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 10px;
    position: absolute;
    right: 16px;
}

/* Sidebar Database Status */
.db-status-card {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: var(--radius-md);
    padding: 16px;
}

.db-status-header {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    font-weight: 600;
    color: #38bdf8;
    margin-bottom: 10px;
}

#db-status-info p {
    font-size: 11px;
    color: #94a3b8;
    line-height: 1.5;
}

#db-status-info strong {
    color: var(--text-white);
}

.sync-instruction {
    margin-top: 12px;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    padding-top: 10px;
}

.sync-instruction p {
    font-size: 9.5px;
    color: #64748b;
    margin-bottom: 6px;
}

.sync-instruction code {
    display: block;
    background: #020617;
    color: #38bdf8;
    font-family: monospace;
    font-size: 10px;
    padding: 6px;
    border-radius: 4px;
    overflow-x: auto;
}

/* Main Content Area */
.app-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    padding-bottom: 0;
}

.app-header {
    height: 70px;
    background-color: rgba(255, 255, 255, 0.5);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-bottom: 1px solid var(--border-color);
    padding: 0 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-shrink: 0;
}

.header-title h2 {
    font-family: var(--font-heading);
    font-size: 20px;
    font-weight: 700;
    color: var(--bg-sidebar);
}

.header-title p {
    font-size: 12px;
    color: var(--text-muted);
}

.location-badge {
    background-color: var(--primary-light);
    color: var(--primary);
    font-size: 12px;
    font-weight: 600;
    padding: 6px 12px;
    border-radius: 20px;
    display: flex;
    align-items: center;
    gap: 6px;
}

/* Tab Contents Container */
.tab-content {
    display: none;
    flex: 1;
    overflow-y: auto;
    padding: 32px;
}

.tab-content.active {
    display: block;
}

/* Glassmorphism Panel styles */
.glass {
    background-color: var(--card-bg);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--glass-border);
    box-shadow: var(--shadow-md);
    border-radius: var(--radius-lg);
    transition: var(--transition);
}

.glass:hover {
    box-shadow: var(--shadow-lg);
    border-color: rgba(255, 255, 255, 0.8);
}

/* 1. Dashboard Tab Styles */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 24px;
    margin-bottom: 32px;
}

.kpi-card {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 24px;
}

.kpi-icon {
    width: 48px;
    height: 48px;
    border-radius: var(--radius-md);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
}

.icon-blue {
    background-color: var(--primary-light);
    color: var(--primary);
}

.icon-green {
    background-color: var(--success-light);
    color: var(--success);
}

.icon-orange {
    background-color: var(--warning-light);
    color: var(--warning);
}

.icon-red {
    background-color: var(--danger-light);
    color: var(--danger);
}

.kpi-info {
    display: flex;
    flex-direction: column;
}

.kpi-label {
    font-size: 12px;
    color: var(--text-muted);
    font-weight: 500;
}

.kpi-value {
    font-family: var(--font-heading);
    font-size: 24px;
    font-weight: 800;
    color: var(--bg-sidebar);
    margin-top: 2px;
}

.dashboard-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
    margin-bottom: 32px;
}

.chart-container {
    padding: 24px;
}

.chart-container h4 {
    font-family: var(--font-heading);
    font-size: 16px;
    font-weight: 600;
    color: var(--bg-sidebar);
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.chart-wrapper {
    position: relative;
    height: 250px;
    width: 100%;
}

.dashboard-secondary-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
}

.list-container {
    padding: 24px;
}

.list-container h4 {
    font-family: var(--font-heading);
    font-size: 16px;
    font-weight: 600;
    color: var(--bg-sidebar);
    margin-bottom: 16px;
}

.list-wrapper {
    display: flex;
    flex-direction: column;
    gap: 12px;
    max-height: 250px;
    overflow-y: auto;
    padding-right: 6px;
}

/* Custom scrollbars */
.list-wrapper::-webkit-scrollbar,
.tree-container::-webkit-scrollbar,
.table-wrapper::-webkit-scrollbar,
.timeline-container::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}

.list-wrapper::-webkit-scrollbar-track,
.tree-container::-webkit-scrollbar-track,
.table-wrapper::-webkit-scrollbar-track,
.timeline-container::-webkit-scrollbar-track {
    background: transparent;
}

.list-wrapper::-webkit-scrollbar-thumb,
.tree-container::-webkit-scrollbar-thumb,
.table-wrapper::-webkit-scrollbar-thumb,
.timeline-container::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 3px;
}

.list-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 14px;
    background: rgba(255, 255, 255, 0.5);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    font-size: 13px;
}

.list-item-name {
    font-weight: 500;
}

.list-item-value {
    font-weight: 600;
    background: var(--primary-light);
    color: var(--primary);
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 11px;
}

.status-item {
    display: flex;
    flex-direction: column;
    gap: 6px;
    padding: 10px 14px;
    background: rgba(255, 255, 255, 0.5);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    font-size: 13px;
}

.status-item-header {
    display: flex;
    justify-content: space-between;
    font-weight: 500;
}

.status-progress-bar {
    height: 6px;
    background: #e2e8f0;
    border-radius: 3px;
    overflow: hidden;
}

.status-progress-fill {
    height: 100%;
    background: var(--primary);
    border-radius: 3px;
}

/* 2. History Navigation Tab Styles */
.history-grid {
    display: grid;
    grid-template-columns: 310px 1fr;
    gap: 24px;
    align-items: start;
    height: 100%;
}

.history-tree-card {
    padding: 20px;
    height: 620px;
    display: flex;
    flex-direction: column;
}

.history-tree-card h3 {
    font-family: var(--font-heading);
    font-size: 16px;
    font-weight: 600;
    color: var(--bg-sidebar);
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.history-tip {
    font-size: 10.5px;
    color: var(--text-muted);
    margin-bottom: 16px;
    line-height: 1.4;
}

.tree-container {
    flex: 1;
    overflow-y: auto;
    padding-right: 6px;
}

.tree-node {
    margin-left: 12px;
}

.tree-node-title {
    padding: 8px 10px;
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    border-radius: var(--radius-sm);
    display: flex;
    align-items: center;
    gap: 8px;
    transition: var(--transition);
    user-select: none;
    min-height: 40px; /* Touch friendly */
}

.tree-node-title:hover {
    background-color: var(--primary-light);
    color: var(--primary);
}

.tree-node.expanded > .tree-node-children {
    display: block;
}

.tree-node-children {
    display: none;
    border-left: 1px dashed #cbd5e1;
    margin-left: 6px;
    padding-left: 6px;
}

.tree-node-title i {
    font-size: 12px;
    width: 14px;
    text-align: center;
    color: var(--text-muted);
}

.tree-node-title.selected {
    background-color: var(--primary-light);
    color: var(--primary);
    font-weight: 600;
}

.tree-node-title.selected i {
    color: var(--primary);
}

/* Checkboxes in Tree Navigation */
.tree-cb {
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 1.5px solid var(--text-muted);
    cursor: pointer;
    flex-shrink: 0;
    accent-color: var(--primary);
}

.history-table-card {
    padding: 24px;
    height: 620px;
    display: flex;
    flex-direction: column;
}

.table-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 18px;
    flex-wrap: wrap;
    gap: 12px;
}

.table-header h3 {
    font-family: var(--font-heading);
    font-size: 16px;
    font-weight: 600;
    color: var(--bg-sidebar);
}

.header-controls {
    display: flex;
    align-items: center;
    gap: 16px;
}

.view-toggle {
    display: flex;
    background: #e2e8f0;
    padding: 3px;
    border-radius: var(--radius-md);
}

.toggle-btn {
    border: none;
    background: none;
    font-family: var(--font-body);
    font-size: 11px;
    font-weight: 600;
    color: var(--text-muted);
    padding: 8px 14px;
    border-radius: 8px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 6px;
    transition: var(--transition);
    min-height: 36px;
}

.toggle-btn.active {
    background: #ffffff;
    color: var(--primary);
    box-shadow: var(--shadow-sm);
}

.badge {
    background-color: var(--primary-light);
    color: var(--primary);
    font-size: 12px;
    font-weight: 600;
    padding: 6px 12px;
    border-radius: 12px;
}

/* View panel toggle */
.history-view-panel {
    display: none;
    flex: 1;
    overflow: hidden;
}

.history-view-panel.active {
    display: flex;
    flex-direction: column;
}

/* Quirófanos visual grid timeline style */
.timeline-container {
    flex: 1;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 24px;
    padding-right: 6px;
}

/* Multi-Day Stack Header in Visual Grid */
.timeline-day-section {
    display: flex;
    flex-direction: column;
    gap: 16px;
    border: 1px solid var(--border-color);
    background: rgba(255, 255, 255, 0.2);
    border-radius: var(--radius-lg);
    padding: 16px;
}

.timeline-day-title {
    font-family: var(--font-heading);
    font-size: 16px;
    font-weight: 800;
    color: var(--primary);
    display: flex;
    align-items: center;
    gap: 8px;
    padding-bottom: 8px;
    border-bottom: 2px solid var(--primary-light);
}

.timeline-row {
    background: rgba(255, 255, 255, 0.6);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.timeline-row-header {
    font-family: var(--font-heading);
    font-size: 14px;
    font-weight: 700;
    color: var(--bg-sidebar);
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid var(--border-color);
    padding-bottom: 6px;
}

.timeline-grid-layout {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
}

.quirofano-card {
    background: #ffffff;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    padding: 14px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    transition: var(--transition);
    box-shadow: var(--shadow-sm);
    cursor: pointer;
    position: relative;
}

.quirofano-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
    border-color: var(--primary);
}

.quirofano-card.empty {
    border: 1px dashed #cbd5e1;
    background: rgba(248, 250, 252, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-muted);
    font-style: italic;
    font-size: 12px;
    min-height: 90px;
    box-shadow: none;
    cursor: default;
}

.quirofano-card.empty:hover {
    transform: none;
    box-shadow: none;
    border-color: #cbd5e1;
}

.quirofano-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-right: 28px; /* space for bookmark button */
}

.qx-tag {
    background: var(--bg-sidebar);
    color: var(--text-white);
    font-size: 9.5px;
    font-weight: 700;
    padding: 2px 6px;
    border-radius: 4px;
}

.quirofano-card-body {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.quirofano-patient {
    font-size: 13px;
    font-weight: 700;
    color: var(--bg-sidebar);
}

.quirofano-surgery {
    font-size: 11px;
    font-weight: 600;
    color: var(--primary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.quirofano-details {
    font-size: 10.5px;
    color: var(--text-muted);
}

.quirofano-status {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 10px;
    font-weight: 600;
}

.status-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
}

.status-dot.green { background-color: var(--success); }
.status-dot.yellow { background-color: var(--warning); }
.status-dot.red { background-color: var(--danger); }

/* Bookmark/Star Button style */
.bookmark-btn {
    position: absolute;
    top: 12px;
    right: 12px;
    background: none;
    border: none;
    color: var(--text-muted);
    font-size: 16px;
    cursor: pointer;
    padding: 4px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: var(--transition);
    z-index: 5;
    width: 32px;
    height: 32px;
}

.bookmark-btn:hover {
    background-color: var(--primary-light);
    color: var(--warning);
}

.bookmark-btn.active {
    color: var(--warning);
    animation: pulseStar 0.3s ease-out;
}

@keyframes pulseStar {
    0% { transform: scale(1); }
    50% { transform: scale(1.3); }
    100% { transform: scale(1); }
}

/* Non standard row (Locales, Endoscopias) full width list */
.non-standard-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 16px;
}

.empty-timeline-message {
    text-align: center;
    color: var(--text-muted);
    padding: 80px;
    font-style: italic;
    background: rgba(255, 255, 255, 0.4);
    border: 1px dashed var(--glass-border);
    border-radius: var(--radius-lg);
}

/* Classic Table */
.table-wrapper {
    flex: 1;
    overflow: auto;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
}

table {
    width: 100%;
    border-collapse: collapse;
    font-size: 12.5px;
    text-align: left;
}

th {
    background: #f8fafc;
    color: var(--text-muted);
    font-weight: 600;
    padding: 12px 16px;
    position: sticky;
    top: 0;
    border-bottom: 1px solid var(--border-color);
    z-index: 1;
}

td {
    padding: 12px 16px;
    border-bottom: 1px solid var(--border-color);
    background: #ffffff;
}

tr:hover td {
    background: var(--primary-light);
}

tr.row-clickable {
    cursor: pointer;
}

.empty-table-message {
    text-align: center;
    color: var(--text-muted);
    padding: 40px !important;
    font-style: italic;
}

/* Status markers in tables */
.status-badge {
    display: inline-block;
    padding: 3px 8px;
    border-radius: 20px;
    font-size: 10px;
    font-weight: 600;
    text-transform: uppercase;
}

.status-badge.completa {
    background-color: var(--success-light);
    color: var(--success);
    border: 1px solid rgba(16, 185, 129, 0.2);
}

.status-badge.pendiente {
    background-color: var(--warning-light);
    color: var(--warning);
    border: 1px solid rgba(245, 158, 11, 0.2);
}

.status-badge.incompleta {
    background-color: var(--danger-light);
    color: var(--danger);
    border: 1px solid rgba(239, 68, 68, 0.2);
}

/* Row reserved style */
.row-reserved-slot td {
    background-color: var(--primary-light);
}

/* 3. Search and Detailed View Tab */
.search-controls {
    padding: 24px;
    margin-bottom: 30px;
}

.search-form-row {
    display: flex;
    align-items: flex-end;
    gap: 20px;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.flex-1 { flex: 1; }
.flex-2 { flex: 2; }

.form-group label {
    font-size: 12px;
    font-weight: 600;
    color: var(--bg-sidebar);
    display: flex;
    align-items: center;
    gap: 6px;
}

.form-group input {
    height: 48px; /* Touch target optimized */
    border: 1px solid #cbd5e1;
    border-radius: var(--radius-md);
    padding: 0 16px;
    font-family: var(--font-body);
    font-size: 14px;
    color: var(--text-main);
    background-color: #ffffff;
    transition: var(--transition);
    outline: none;
}

.form-group input:focus {
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
}

.form-group-btn button {
    height: 48px; /* Touch target optimized */
    border: 1px solid #cbd5e1;
    background: #ffffff;
    padding: 0 24px;
    border-radius: var(--radius-md);
    cursor: pointer;
    font-weight: 600;
    font-size: 14px;
    font-family: var(--font-body);
    transition: var(--transition);
}

.form-group-btn button:hover {
    background: var(--danger-light);
    color: var(--danger);
    border-color: var(--danger);
}

.results-header {
    margin-bottom: 16px;
}

.results-header h3 {
    font-family: var(--font-heading);
    font-size: 16px;
    font-weight: 600;
    color: var(--bg-sidebar);
}

/* Patient selection introduction card */
.selection-intro {
    padding: 24px;
}

.selection-intro h3 {
    font-family: var(--font-heading);
    font-size: 18px;
    font-weight: 700;
    color: var(--bg-sidebar);
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.selection-intro p {
    font-size: 13px;
    color: var(--text-muted);
    line-height: 1.5;
}

/* Patient grid and cards */
.patient-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 24px;
}

.patient-card {
    padding: 20px;
    border-radius: var(--radius-lg);
    background: var(--card-bg);
    border: 1px solid var(--glass-border);
    display: flex;
    flex-direction: column;
    gap: 14px;
    position: relative;
    cursor: pointer;
    transition: var(--transition);
    box-shadow: var(--shadow-sm);
}

.patient-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
    border-color: var(--primary);
}

.patient-card-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    border-bottom: 1px solid var(--border-color);
    padding-bottom: 12px;
    padding-right: 28px; /* space for bookmark */
}

.patient-name-block h4 {
    font-family: var(--font-heading);
    font-size: 15px;
    font-weight: 700;
    color: var(--bg-sidebar);
}

.patient-name-block span {
    font-size: 11px;
    color: var(--text-muted);
}

.patient-info-list {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px 16px;
    font-size: 12px;
}

.info-item {
    display: flex;
    flex-direction: column;
    gap: 3px;
}

.info-label {
    font-size: 10px;
    color: var(--text-muted);
    font-weight: 500;
    text-transform: uppercase;
}

.info-value {
    font-weight: 600;
    color: var(--text-main);
}

.patient-card-footer {
    border-top: 1px solid var(--border-color);
    padding-top: 12px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 11px;
    color: var(--text-muted);
}

.patient-card-footer i {
    margin-right: 4px;
}

.empty-results {
    grid-column: 1 / -1;
    text-align: center;
    color: var(--text-muted);
    padding: 60px;
    font-style: italic;
    background: var(--card-bg);
    border: 1px dashed var(--glass-border);
    border-radius: var(--radius-lg);
}

/* 4. Mobile Bottom Navigation Bar Styling */
.mobile-nav {
    display: none; /* Desktop default hidden */
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    height: 64px;
    background-color: var(--bg-sidebar);
    color: var(--text-white);
    justify-content: space-around;
    align-items: center;
    box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.15);
    z-index: 100;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.mobile-nav-btn {
    border: none;
    background: none;
    color: #94a3b8;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 4px;
    flex: 1;
    height: 100%;
    cursor: pointer;
    font-family: var(--font-body);
    transition: var(--transition);
    position: relative;
}

.mobile-nav-btn i {
    font-size: 20px;
}

.mobile-nav-btn span {
    font-size: 10px;
    font-weight: 500;
}

.mobile-nav-btn.active {
    color: #38bdf8;
}

/* Mobile Badge Count style */
.badge-count-mobile {
    background: var(--warning);
    color: var(--bg-sidebar);
    font-size: 9px;
    font-weight: 700;
    width: 16px;
    height: 16px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    position: absolute;
    top: 6px;
    right: calc(50% - 18px);
}

/* 5. Detailed Patient Profile Modal Overlay style */
.modal-overlay {
    display: none; /* hidden by default */
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(15, 23, 42, 0.75);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    z-index: 1000;
    align-items: center;
    justify-content: center;
    padding: 20px;
}

.modal-overlay.active {
    display: flex;
    animation: modalFadeIn 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes modalFadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

.modal-card {
    width: 100%;
    max-width: 620px;
    background-color: rgba(255, 255, 255, 0.85);
    border: 1px solid var(--glass-border);
    border-radius: var(--radius-lg);
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    transform: scale(0.95);
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.modal-overlay.active .modal-card {
    transform: scale(1);
}

.modal-header {
    padding: 24px;
    border-bottom: 1px solid var(--border-color);
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: rgba(255, 255, 255, 0.5);
}

.modal-header-title {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.modal-subtitle {
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    color: var(--primary);
    letter-spacing: 0.5px;
}

#modal-patient-name {
    font-family: var(--font-heading);
    font-size: 22px;
    font-weight: 800;
    color: var(--bg-sidebar);
}

.modal-close-btn {
    border: none;
    background: #e2e8f0;
    color: var(--text-main);
    width: 36px;
    height: 36px;
    border-radius: 50%;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    transition: var(--transition);
}

.modal-close-btn:hover {
    background-color: var(--danger-light);
    color: var(--danger);
}

.modal-body {
    padding: 24px;
    overflow-y: auto;
    max-height: 70vh;
}

/* Modal specific listings */
.modal-section {
    margin-bottom: 24px;
}

.modal-section-title {
    font-family: var(--font-heading);
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    color: var(--text-muted);
    border-bottom: 1px solid var(--border-color);
    padding-bottom: 6px;
    margin-bottom: 12px;
}

.modal-info-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
}

.modal-block-full {
    grid-column: span 2;
}

.modal-val-box {
    background: #ffffff;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    padding: 12px;
}

.modal-badge-container {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-top: 8px;
}

/* Animations */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.tab-content.active {
    animation: fadeIn 0.4s ease-out;
}

/* Responsive adjust */
@media (max-width: 1024px) {
    .dashboard-grid, .dashboard-secondary-grid {
        grid-template-columns: 1fr;
    }
    
    .history-grid {
        grid-template-columns: 1fr;
    }
    
    .history-tree-card {
        height: auto;
        max-height: 350px;
    }
    
    .history-table-card {
        height: auto;
        min-height: 450px;
    }
    
    .timeline-grid-layout {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 768px) {
    body {
        /* Prevent scroll bouncing */
        overscroll-behavior-y: contain;
    }

    .app-container {
        flex-direction: column;
    }
    
    /* Hide desktop sidebar on mobile */
    .app-sidebar {
        display: none;
    }
    
    /* Make mobile navigation bar visible */
    .mobile-nav {
        display: flex;
    }
    
    /* Padding bottom of main container to not overlap mobile bottom nav */
    .app-content {
        padding-bottom: 64px;
    }
    
    .app-header {
        padding: 0 16px;
        height: 60px;
    }
    
    .header-title h2 {
        font-size: 17px;
    }
    
    .tab-content {
        padding: 16px;
    }
    
    .search-controls {
        padding: 16px;
        margin-bottom: 20px;
    }
    
    .search-form-row {
        flex-direction: column;
        align-items: stretch;
        gap: 12px;
    }
    
    .form-group-btn button {
        width: 100%;
        margin-top: 8px;
    }
    
    .patient-grid {
        grid-template-columns: 1fr;
    }
    
    .modal-info-grid {
        grid-template-columns: 1fr;
    }
    
    .modal-block-full {
        grid-column: span 1;
    }
}
"""

# Overwriting app.js with improved UX selections, corrected JavaScript, multi-day tree menu, bookmarks, and patient profile modal
app_js_content = """// State Variables
let database = { last_updated: "", surgeries: [] };
let activeTab = "tab-dashboard";
let historyViewMode = "grid"; // "grid" or "table"
let selectedTreeDays = []; // Array of checked day strings
let bookmarkedSurgeries = JSON.parse(localStorage.getItem("bookmarked_surgeries") || "[]");

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
document.addEventListener("DOMContentLoaded", () => {
    setupTabNavigation();
    setupViewToggle();
    loadDatabase();
    setupSearchFilters();
});

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
    const lastUpdated = database.last_updated ? new Date(database.last_updated) : null;
    const formattedDate = lastUpdated 
        ? lastUpdated.toLocaleString("es-AR", { dateStyle: 'short', timeStyle: 'short' })
        : "Nunca";
        
    document.getElementById("db-status-info").innerHTML = `
        <p>Registros Históricos: <strong>${totalRecords}</strong></p>
        <p>Última Sincronización: <strong>${formattedDate}</strong></p>
    `;
}

// Helper to split date into Year, Month, Day
function parseDateParts(dateStr) {
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
    
    localStorage.setItem("bookmarked_surgeries", JSON.stringify(bookmarkedSurgeries));
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
"""

import os

# Overwrite index.html
with open("index.html", "w", encoding="utf-8") as f:
    f.write(index_html_content)
print("index.html written successfully.")

# Overwrite styles.css
with open("styles.css", "w", encoding="utf-8") as f:
    f.write(styles_css_content)
print("styles.css written successfully.")

# Overwrite app.js
with open("app.js", "w", encoding="utf-8") as f:
    f.write(app_js_content)
print("app.js written successfully.")

print("All dashboard components rewritten for Mobile, Checkboxes, Bookmarks and Modal Ficha Quirúrgica!")
