import urllib.request
import re
import json
import csv
import os
import hashlib
from datetime import datetime

# Load configuration
CONFIG_PATH = "config.json"
DATABASE_PATH = "database.json"

if not os.path.exists(CONFIG_PATH):
    print(f"Error: {CONFIG_PATH} not found. Creating default config.")
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump({"drive_folder_id": "1wBUGs04wayk7W3CneFQHr59Iz5KHiths"}, f, indent=2)

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)

DRIVE_FOLDER_ID = config.get("drive_folder_id", "1wBUGs04wayk7W3CneFQHr59Iz5KHiths")

VALID_SPECIALTIES = [
    "TYO", "GINECO", "GIINECO", "GINECOLOGIA", "GINECOLOGÍA", "GYO",
    "CX GENERAL", "CG", "CIRUGIA GENERAL", "CIRUGÍA GENERAL", "CIRUGIA", "CIRUGÍA",
    "URO", "UROLOGIA", "UROLOGÍA", "OFTALMO", "OFTALMOLOGIA", "OFTALMOLOGÍA",
    "ORL", "OTORRINO", "OTORRINOLARINGOLOGIA", "OTORRINOLARINGOLOGÍA",
    "PLASTICA", "PLÁSTICA", "CIRUGIA PLASTICA", "CIRUGÍA PLÁSTICA",
    "INFANTIL", "PEDIATRIA", "PEDIATRÍA", "CIRUGIA INFANTIL", "CIRUGÍA INFANTIL", "CIR PED",
    "VASCULAR", "NEU", "NEURO", "NEUROCIRUGIA", "NEUROCIRUGÍA", "CG CHICA"
]

def is_valid_specialty(spec):
    s = spec.strip().upper()
    if not s:
        return False
    return any(valid in s for valid in VALID_SPECIALTIES)

def normalize_specialty(spec):
    s = spec.strip().upper()
    if not s:
        return "SIN ESPECIFICAR"
    if any(x in s for x in ["GINECO", "GIINECO", "GYO"]):
        return "Ginecología y Obstetricia"
    if any(x in s for x in ["TYO", "TRAUMATO"]):
        return "Traumatología y Ortopedia"
    if any(x in s for x in ["CX GENERAL", "CG", "CIRUGIA GENERAL", "CIRUGÍA GENERAL", "CIRUGIA", "CIRUGÍA"]):
        return "Cirugía General"
    if "URO" in s:
        return "Urología"
    if "OFTAL" in s:
        return "Oftalmología"
    if "ORL" in s or "OTORRINO" in s:
        return "Otorrinolaringología"
    if "PLAST" in s:
        return "Cirugía Plástica"
    if any(x in s for x in ["INFANTIL", "PEDIAT", "CIR PED", "CG CHICA"]):
        return "Cirugía Infantil"
    if "VASCULAR" in s:
        return "Cirugía Vascular"
    if "NEU" in s:
        return "Neurocirugía"
    return s.title()

def normalize_doctor(doc):
    d = doc.strip().upper()
    if not d:
        return "SIN ESPECIFICAR"
    d = d.replace(".", "").strip()
    return d.title()

def normalize_insurance(ins):
    i = ins.strip().upper()
    if not i:
        return "PARTICULAR"
    i = re.sub(r'^[^A-Z0-9]+|[^A-Z0-9]+$', '', i)
    if "SUMAR" in i:
        return "SUMAR (Salud Pública)"
    if "OSEF" in i:
        return "OSEF (Provincial Fueguino)"
    if "OSECAC" in i:
        return "OSECAC (Comercio)"
    if "OSDE" in i:
        return "OSDE (Prepaga)"
    if "IOSFA" in i:
        return "IOSFA (Fuerzas Armadas)"
    if "UP" in i or "UNION PERSONAL" in i:
        return "Unión Personal"
    if "OSPAT" in i:
        return "OSPAT"
    if "OSME" in i:
        return "OSME"
    if "PAMI" in i:
        return "PAMI"
    if "SADAIC" in i:
        return "SADAIC"
    if "OSUTHGRA" in i or "UTHGRA" in i:
        return "UTHGRA (Hoteleros/Gastronómicos)"
    if "OSPERSAMS" in i:
        return "OSPERSAMS (Sanidad)"
    if "OSCTCP" in i or "TAXIMETRO" in i:
        return "OSCTCP (Taxistas)"
    return i.title()

def normalize_qx(qx):
    q = qx.strip().upper()
    if not q:
        return ""
    if q in ["1", "Q1"]:
        return "Q1"
    if q in ["2", "Q2"]:
        return "Q2"
    if q in ["3", "Q3"]:
        return "Q3"
    if q in ["4", "Q4"]:
        return "Q4"
    return q

def normalize_time_slot(slot):
    s = slot.strip()
    if s == "1":
        return "08 a 10 hs"
    if s == "2":
        return "10 a 12 hs"
    if s == "3":
        return "12 a 14 hs"
    if "08" in s and "10" in s:
        return "08 a 10 hs"
    if "10" in s and "12" in s:
        return "10 a 12 hs"
    if "12" in s and "14" in s:
        return "12 a 14 hs"
    if "LOCAL" in s.upper():
        return "Locales"
    if "ENDOSCOP" in s.upper():
        return "Endoscopia"
    return s

def clean_day_name(day):
    d = day.strip()
    num_match = re.search(r'\d+', d)
    num_suffix = f" {num_match.group(0)}" if num_match else ""
    d_lower = d.lower()
    if "lun" in d_lower:
        return "Lunes" + num_suffix
    if "mar" in d_lower:
        return "Martes" + num_suffix
    if "mi" in d_lower or "mí" in d_lower or "mÃ" in d_lower or "mie" in d_lower:
        return "Miércoles" + num_suffix
    if "jue" in d_lower:
        return "Jueves" + num_suffix
    if "vie" in d_lower:
        return "Viernes" + num_suffix
    return d

def normalize_text(text):
    if not text:
        return ""
    t = re.sub(r'\s+', ' ', str(text)).strip().upper()
    replacements = (
        ("Á", "A"), ("É", "E"), ("Í", "I"), ("Ó", "O"), ("Ú", "U"),
        ("á", "A"), ("é", "E"), ("í", "I"), ("ó", "O"), ("ú", "U"),
        ("Ñ", "N"), ("ñ", "N")
    )
    for a, b in replacements:
        t = t.replace(a, b)
    return t

def normalize_dni(dni):
    if not dni:
        return ""
    digits = re.sub(r'[^\d]', '', str(dni))
    return digits if len(digits) >= 6 else ""

def get_patient_key(r):
    date_val = r.get('date', '').strip()
    is_empty = r.get('is_empty_slot', False) or not r.get('patient', '').strip()
    
    if is_empty:
        doc = normalize_text(r.get('doctor', ''))
        spec = normalize_text(r.get('specialty', ''))
        slot = normalize_text(r.get('time_slot', ''))
        qx = normalize_text(r.get('qx', ''))
        sheet_id = r.get('source_sheet_id', '')
        return f"EMPTY|{date_val}|{slot}|{qx}|{doc}|{spec}|{sheet_id}"
        
    dni = normalize_dni(r.get('dni', ''))
    patient_name = normalize_text(r.get('patient', ''))
    
    if dni:
        return f"PATIENT_DNI|{date_val}|{dni}"
    else:
        doc = normalize_text(r.get('doctor', ''))
        return f"PATIENT_NAME|{date_val}|{patient_name}|{doc}"

def merge_records(existing, incoming):
    merged = dict(existing)
    
    # Priority for qx: if incoming has QX and existing does not, take incoming
    if not merged.get('qx') and incoming.get('qx'):
        merged['qx'] = incoming['qx']
        
    # Priority for time_slot: standard time slots (e.g. "08 a 10 hs") preferred over numbers or unknown
    if "a" in incoming.get('time_slot', '') and "a" not in merged.get('time_slot', ''):
        merged['time_slot'] = incoming['time_slot']
    elif not merged.get('time_slot') and incoming.get('time_slot'):
        merged['time_slot'] = incoming['time_slot']
        
    # Fill in missing fields
    for field in ['surgery', 'ailment', 'dni', 'phone', 'age', 'insurance', 'anesthesia', 'boxes', 'rx', 'status', 'doctor', 'specialty']:
        val_exist = str(merged.get(field, '')).strip()
        val_in = str(incoming.get(field, '')).strip()
        if not val_exist and val_in:
            merged[field] = incoming[field]
        elif len(val_in) > len(val_exist) and field in ['surgery', 'ailment', 'boxes', 'status']:
            merged[field] = incoming[field]
            
    merged['is_empty_slot'] = not bool(merged.get('patient', '').strip())
    merged['hash'] = hashlib.sha256(get_patient_key(merged).encode('utf-8')).hexdigest()
    return merged

def fetch_html(folder_id):
    url = f"https://drive.google.com/drive/folders/{folder_id}"
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    )
    try:
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching folder {folder_id}: {e}")
        return ""

def parse_items(html):
    pos = 0
    callbacks = []
    while True:
        idx = html.find("AF_initDataCallback(", pos)
        if idx == -1:
            break
        start_idx = idx + len("AF_initDataCallback(")
        paren_count = 1
        current_pos = start_idx
        while paren_count > 0 and current_pos < len(html):
            char = html[current_pos]
            if char == '(':
                paren_count += 1
            elif char == ')':
                paren_count -= 1
            current_pos += 1
        callbacks.append(html[start_idx:current_pos-1])
        pos = current_pos

    items = {}
    for cb in callbacks:
        id_matches = re.finditer(r'\[null,\s*"([a-zA-Z0-9-_]{28,45})"\s*\]', cb)
        for m in id_matches:
            item_id = m.group(1)
            if item_id in items:
                continue
            start_pos = m.end()
            snippet = cb[start_pos : start_pos + 2500]
            mime_match = re.search(r'"(application/vnd\.google-apps\.[a-z\-]+|application/[a-zA-Z0-9\-\.\+]+|image/[a-z]+|text/[a-z]+)"', snippet)
            mime_type = mime_match.group(1) if mime_match else "unknown"
            
            name_match = re.search(r'\[\[\["([^"]+)"', snippet)
            name = "unknown"
            if name_match:
                name = name_match.group(1)
            else:
                candidates = re.findall(r'"([^"\\]*(?:\\.[^"\\]*)*)"', snippet)
                for cand in candidates:
                    try:
                        cand_clean = cand.encode('utf-8').decode('unicode-escape', errors='ignore')
                    except Exception:
                        cand_clean = cand
                    cand_clean = re.sub(r'\\u([0-9a-fA-F]{4})', lambda x: chr(int(x.group(1), 16)), cand_clean)
                    if cand_clean and not cand_clean.startswith("application/") and cand_clean not in [
                        "Download", "More actions", "Shared folder", "Size not available", 
                        "Modified", "Modified by me", "Owner", "me", "Date modified", "Name", "Type"
                    ]:
                        name = cand_clean
                        break
            try:
                name_decoded = name.encode('utf-8').decode('unicode-escape')
            except Exception:
                name_decoded = name
            name_decoded = re.sub(r'\\u([0-9a-fA-F]{4})', lambda x: chr(int(x.group(1), 16)), name_decoded)
            
            if mime_type != "unknown" or name_decoded != "unknown":
                items[item_id] = {
                    'id': item_id,
                    'name': name_decoded,
                    'mimeType': mime_type
                }
    return list(items.values())

def crawl_folder_recursive(folder_id, folder_name="Root", visited=None, sheets_found=None):
    if visited is None:
        visited = set()
    if sheets_found is None:
        sheets_found = []
        
    if folder_id in visited:
        return sheets_found
    visited.add(folder_id)
    
    print(f"Crawling folder: {folder_name} ({folder_id})...")
    html = fetch_html(folder_id)
    if not html:
        return sheets_found
        
    items = parse_items(html)
    for item in items:
        is_folder = "folder" in item['mimeType']
        is_sheet = "spreadsheet" in item['mimeType']
        
        if is_folder:
            crawl_folder_recursive(item['id'], item['name'], visited, sheets_found)
        elif is_sheet:
            sheets_found.append({
                'id': item['id'],
                'name': item['name'],
                'folder_name': folder_name
            })
            print(f"  Found Sheet: {item['name']} in {folder_name}")
            
    return sheets_found

def download_and_parse_sheet(sheet_id, name, folder_name):
    export_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    req = urllib.request.Request(
        export_url,
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            csv_content = response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Error downloading sheet {name} ({sheet_id}): {e}")
        return []
        
    reader = csv.reader(csv_content.splitlines())
    rows = list(reader)
    
    # Find the header row
    header_row_idx = -1
    for i, r in enumerate(rows):
        if any(cell.strip().upper() == "ESPECIALIDAD" for cell in r):
            header_row_idx = i
            break
            
    if header_row_idx == -1:
        print(f"Warning: Header row not found in sheet: {name}")
        return []
        
    header = rows[header_row_idx]
    date_val = header[0].strip() if header[0] else "unknown_date"
    
    if not re.match(r'\d{1,2}/\d{1,2}/\d{4}', date_val):
        for r in rows:
            for cell in r:
                date_match = re.search(r'(\d{1,2}/\d{1,2}/\d{4})', str(cell))
                if date_match:
                    date_val = date_match.group(1)
                    break
            if date_val != "unknown_date":
                break

    parsed_records = []
    current_time_slot = "unknown"
    
    for r_idx in range(header_row_idx + 1, len(rows)):
        row = rows[r_idx]
        while len(row) < len(header):
            row.append("")
            
        first_cell = row[0].strip() if len(row) > 0 else ""
        
        if first_cell:
            if "LOCAL" in first_cell.upper():
                current_time_slot = "Locales"
            elif "ENDOSCOP" in first_cell.upper():
                current_time_slot = "Endoscopia"
            elif any(x in first_cell for x in ["08 a 10", "10 a 12", "12 a 14", "08 a 12"]):
                current_time_slot = first_cell
            elif first_cell in ["1", "2", "3"]:
                current_time_slot = normalize_time_slot(first_cell)
            elif re.match(r'\d{1,2}/\d{1,2}/\d{4}', first_cell):
                pass
            elif first_cell.upper() in ["LUNES", "MARTES", "MIÉRCOLES", "MIERCOLES", "JUEVES", "VIERNES"]:
                pass
            else:
                current_time_slot = first_cell
                
        specialty = row[2].strip() if len(row) > 2 else ""
        doctor = row[3].strip() if len(row) > 3 else ""
        patient = row[4].strip() if len(row) > 4 else ""
        phone = row[5].strip() if len(row) > 5 else ""
        age = row[6].strip() if len(row) > 6 else ""
        dni = row[7].strip() if len(row) > 7 else ""
        ailment = row[8].strip() if len(row) > 8 else ""
        surgery = row[9].strip() if len(row) > 9 else ""
        anesthesia = row[10].strip() if len(row) > 10 else ""
        boxes = row[11].strip() if len(row) > 11 else ""
        insurance = row[12].strip() if len(row) > 12 else ""
        rx = row[13].strip() if len(row) > 13 else ""
        
        obs = []
        for cell_idx in range(14, len(row)):
            cell_val = row[cell_idx].strip()
            if cell_val:
                obs.append(cell_val)
        status = " ".join(obs) if obs else ""
        
        if specialty.upper() == "ESPECIALIDAD" or patient.upper() == "PACIENTE" or doctor.upper() == "MEDICO":
            continue
        if "IMPORTANTE:" in first_cell.upper() or "IMPORTANTE:" in patient.upper():
            continue
        if "RECUERDEN LA CIRCULAR" in patient.upper() or "RECUERDEN" in specialty.upper() or "CIRCULAR" in specialty.upper():
            continue
        if "PRIORIDAD CIRUGIAS" in first_cell.upper() or "PRIORIDAD CIRUGIAS" in patient.upper() or "PRIORIDAD" in specialty.upper():
            continue
        if "ACUERDE CON ESTE AREA" in patient.upper():
            continue
            
        if not specialty and not doctor:
            continue
            
        if "TURNO" in specialty.upper() or "MAÑANA" in specialty.upper() or "TARDE" in specialty.upper() or "LOCALES" in specialty.upper() or "ENDOSCOPIA" in specialty.upper():
            continue
            
        if not is_valid_specialty(specialty) and not doctor:
            continue

        slot_norm = normalize_time_slot(current_time_slot)
        record = {
            'date': date_val,
            'day': clean_day_name(name.split(" ")[0]),
            'time_slot': slot_norm,
            'qx': normalize_qx(row[1].strip() if len(row) > 1 else ""),
            'specialty': normalize_specialty(specialty),
            'doctor': normalize_doctor(doctor),
            'patient': patient,
            'phone': phone,
            'age': age,
            'dni': dni,
            'ailment': ailment,
            'surgery': surgery,
            'anesthesia': anesthesia,
            'boxes': boxes,
            'insurance': normalize_insurance(insurance),
            'rx': rx,
            'status': status,
            'is_empty_slot': not patient,
            'source_sheet_id': sheet_id,
            'source_sheet_name': name,
            'source_folder_name': folder_name
        }
        record['hash'] = hashlib.sha256(get_patient_key(record).encode('utf-8')).hexdigest()
        
        parsed_records.append(record)
        
    return parsed_records

def main():
    print(f"Starting database sync from Google Drive Folder ID: {DRIVE_FOLDER_ID}")
    
    # 1. Crawl all sheets
    sheets = crawl_folder_recursive(DRIVE_FOLDER_ID, "Turnos Quirurgicos")
    print(f"Crawl complete. Found {len(sheets)} sheet files to import.")
    
    # 2. Parse all surgeries from sheets
    new_records = []
    for idx, sheet in enumerate(sheets):
        print(f"[{idx+1}/{len(sheets)}] Processing sheet: {sheet['name']} in {sheet['folder_name']}...")
        sheet_records = download_and_parse_sheet(sheet['id'], sheet['name'], sheet['folder_name'])
        new_records.extend(sheet_records)
        print(f"  Parsed {len(sheet_records)} surgeries.")
        
    print(f"Total surgeries parsed from Google Drive: {len(new_records)}")
    
    # 3. Load existing database
    existing_db = {'last_updated': '', 'surgeries': []}
    if os.path.exists(DATABASE_PATH):
        try:
            with open(DATABASE_PATH, "r", encoding="utf-8") as db_f:
                existing_db = json.load(db_f)
            print(f"Loaded existing database with {len(existing_db.get('surgeries', []))} records.")
        except Exception as e:
            print(f"Warning: Could not read existing database: {e}. Starting fresh.")
            
    # Build dictionary of existing records mapped by patient identity key
    db_map = {}
    for r in existing_db.get('surgeries', []):
        pkey = get_patient_key(r)
        if pkey not in db_map:
            r['hash'] = hashlib.sha256(pkey.encode('utf-8')).hexdigest()
            db_map[pkey] = r
        else:
            db_map[pkey] = merge_records(db_map[pkey], r)
        
    # 4. Merge new records using patient identity key
    added_count = 0
    updated_count = 0
    
    for r in new_records:
        pkey = get_patient_key(r)
        r['hash'] = hashlib.sha256(pkey.encode('utf-8')).hexdigest()
        
        if pkey not in db_map:
            db_map[pkey] = r
            added_count += 1
        else:
            db_map[pkey] = merge_records(db_map[pkey], r)
            updated_count += 1
            
    # 5. Save database
    consolidated_records = list(db_map.values())
    
    # Sort chronologically by date
    def parse_date(date_str):
        try:
            parts = date_str.split('/')
            if len(parts) == 3:
                return int(parts[2]), int(parts[1]), int(parts[0])
        except Exception:
            pass
        return (9999, 12, 31)
        
    consolidated_records.sort(key=lambda x: (parse_date(x['date']), x['time_slot']))
    
    output_db = {
        'last_updated': datetime.now().isoformat(),
        'surgeries': consolidated_records
    }
    
    with open(DATABASE_PATH, "w", encoding="utf-8") as db_f:
        json.dump(output_db, db_f, ensure_ascii=False, indent=2)
        
    # Save as JS variable for CORS-free file:// access
    with open("database.js", "w", encoding="utf-8") as js_f:
        js_f.write("window.SURGICAL_DATABASE = ")
        json.dump(output_db, js_f, ensure_ascii=False, indent=2)
        js_f.write(";\n")
        
    print("\n" + "="*50)
    print("DATABASE UPDATED SUCCESSFULLY!")
    print(f"Total surgeries in history: {len(consolidated_records)}")
    print(f"New surgeries added: {added_count}")
    print(f"Surgeries updated: {updated_count}")
    print(f"Saved to: {DATABASE_PATH}")
    print("="*50 + "\n")

if __name__ == "__main__":
    main()
