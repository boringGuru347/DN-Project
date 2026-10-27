import sys
sys.stdout.reconfigure(encoding='utf-8')
path = r'generate_lab_report_pdf.py'
with open(path, encoding='utf-8') as f:
    lines = f.readlines()
# Fix line 769 (index 768)
lines[768] = '    print("PDF generated successfully: " + OUT_PDF)\n'
with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("patched line 769")
