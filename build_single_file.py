import os
import re

def build_combined_html():
    print("Iniciando empaquetado para Google Sites...")
    
    # Paths
    project_dir = os.path.dirname(os.path.abspath(__file__))
    index_path = os.path.join(project_dir, "index.html")
    styles_path = os.path.join(project_dir, "styles.css")
    database_path = os.path.join(project_dir, "database.js")
    app_path = os.path.join(project_dir, "app.js")
    output_path = os.path.join(project_dir, "combined_dashboard.html")
    
    # Read files
    if not os.path.exists(index_path):
        print("Error: No se encontró index.html")
        return
        
    with open(index_path, "r", encoding="utf-8") as f:
        html_content = f.read()
        
    css_content = ""
    if os.path.exists(styles_path):
        with open(styles_path, "r", encoding="utf-8") as f:
            css_content = f.read()
            
    db_content = ""
    if os.path.exists(database_path):
        with open(database_path, "r", encoding="utf-8") as f:
            db_content = f.read()
            
    app_content = ""
    if os.path.exists(app_path):
        with open(app_path, "r", encoding="utf-8") as f:
            app_content = f.read()

    # 1. Replace CSS stylesheet link with inline style tag
    css_link_pattern = r'<link\s+rel="stylesheet"\s+href="styles\.css"[^>]*>'
    inline_css = f"<style>\n{css_content}\n</style>"
    html_content = re.sub(css_link_pattern, inline_css, html_content)
    
    # 2. Replace script tags with inline scripts
    # Find database.js script tag (handling query params if present)
    db_script_pattern = r'<script\s+src="database\.js(?:\?v=\d+)?"></script>'
    inline_db = f"<script>\n{db_content}\n</script>"
    html_content = re.sub(db_script_pattern, inline_db, html_content)
    
    # Find app.js script tag
    app_script_pattern = r'<script\s+src="app\.js(?:\?v=\d+)?"></script>'
    inline_app = f"<script>\n{app_content}\n</script>"
    html_content = re.sub(app_script_pattern, inline_app, html_content)
    
    # Write output
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"Completado. Archivo único generado con éxito en:\n{output_path}")
    print("Tamaño del archivo: {:.2f} KB".format(os.path.getsize(output_path) / 1024))

if __name__ == "__main__":
    build_combined_html()
