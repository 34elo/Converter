def generate(values, action_id, version, inn):
    """Генерирует XML из списка значений."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append(f'<disaggregation action_id="{action_id}" version="{version}">')
    lines.append(f'    <trade_participant_inn>{inn}</trade_participant_inn>')
    lines.append('    <packings_list>')

    for value in values:
        lines.append('        <packing>')
        lines.append(f'            <kitu><![CDATA[{value}]]></kitu>')
        lines.append('        </packing>')

    lines.append('    </packings_list>')
    lines.append('</disaggregation>')
    return '\n'.join(lines)
