import sys
sys.stdout.reconfigure(encoding='utf-8')
path = r'generate_lab_report_pdf.py'
with open(path, encoding='utf-8') as f:
    content = f.read()
content = content.replace('print(f"\\n\\u2705 PDF generated: {OUT_PDF}")', 'print("PDF generated: " + OUT_PDF)')
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("patched")
