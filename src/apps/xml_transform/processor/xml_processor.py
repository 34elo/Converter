import xml.etree.ElementTree as ET
from datetime import datetime


def parse(path):
    """Парсит XML файл и возвращает список элементов."""
    tree = ET.parse(path)
    items = []
    
    def extract(element, prefix=''):
        for child in element:
            tag_path = f'{prefix}/{child.tag}' if prefix else child.tag
            if child.text and child.text.strip():
                items.append((tag_path, child.text.strip()))
            extract(child, tag_path)
    
    extract(tree.getroot())
    return items


def transform(input_path, params):
    """Преобразует XML из формата 1 в формат 2."""
    tree = ET.parse(input_path)
    root = tree.getroot()
    
    lp_tin = root.find('.//LP_info').get('LP_TIN') if root.find('.//LP_info') is not None else ''
    
    pack_contents = []
    for pc in root.findall('.//pack_content'):
        pack_code = pc.find('pack_code')
        pack_code_text = pack_code.text.strip() if pack_code is not None and pack_code.text else ''
        
        cis_list = []
        for cis in pc.findall('cis'):
            if cis.text and cis.text.strip():
                cis_list.append(cis.text.strip())
        
        if pack_code_text or cis_list:
            pack_contents.append({
                'pack_code': pack_code_text,
                'cis': cis_list
            })
    
    from datetime import datetime
    now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+03:00')
    
    new_root = ET.Element('unit_pack')
    new_root.set('document_id', params.get('document_id', ''))
    new_root.set('VerForm', params.get('ver_form', ''))
    new_root.set('file_date_time', params.get('file_date_time', now))
    new_root.set('VerProg', params.get('ver_prog', ''))
    
    doc = ET.SubElement(new_root, 'Document')
    doc.set('operation_date_time', params.get('operation_date_time', now))
    doc.set('document_number', params.get('document_number', ''))
    
    org = ET.SubElement(doc, 'organisation')
    id_info = ET.SubElement(org, 'id_info')
    lp_info = ET.SubElement(id_info, 'LP_info')
    lp_info.set('org_name', params.get('org_name', ''))
    lp_info.set('LP_TIN', lp_tin)
    lp_info.set('RRC', params.get('rrc', ''))
    
    address = ET.SubElement(org, 'Address')
    location = ET.SubElement(address, 'location_address')
    location.set('country_code', params.get('country_code', ''))
    location.set('text_address', params.get('text_address', ''))
    
    contacts = ET.SubElement(org, 'contacts')
    contacts.set('phone_number', params.get('phone_number', ''))
    contacts.set('email', params.get('email', ''))
    
    for pc_data in pack_contents:
        pc_elem = ET.SubElement(doc, 'pack_content')
        
        pack_code_elem = ET.SubElement(pc_elem, 'pack_code')
        pack_code_elem.text = f'<![CDATA[{pc_data["pack_code"]}]]>'
        
        for cis_text in pc_data['cis']:
            cis_elem = ET.SubElement(pc_elem, 'cis')
            cis_elem.text = f'<![CDATA[{cis_text}]]>'
    
    ET.indent(new_root, space='    ')
    
    xml_str = ET.tostring(new_root, encoding='unicode')
    xml_str = '<?xml version="1.0" encoding="UTF-8"?>\n' + xml_str
    
    return xml_str


def write_file(path, content):
    """Сохраняет XML контент в файл."""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
