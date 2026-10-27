import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'generate_lab_report_pdf.py'
with open(path, encoding='utf-8') as f:
    lines = f.readlines()

# Find the refs block and replace lines 728-740
new_refs = [
    '    refs = [\n',
    "        '[1] N. Moustafa and J. Slay, UNSW-NB15: a comprehensive data set for network "\
    "intrusion detection systems, in <i>Proc. IEEE MilCIS</i>, 2015.',\n",
    "        '[2] P. Phalaagae, A. M. Zungeru, A. Yahya, B. Sigweni and S. Rajalakshmi, "\
    "A Hybrid CNN-LSTM Model With Attention Mechanism for Improved Intrusion Detection "\
    "in Wireless IoT Sensor Networks, <i>IEEE Access</i>, 2025.',\n",
    "        '[3] Edge-AI Enabled Hybrid Deep Learning Framework for Botnet Intrusion "\
    "Detection in Modern IoT-Driven Cyber Ecosystems, <i>IEEE ICERECT</i>, 2025.',\n",
    "        '[4] F. Pedregosa et al., Scikit-learn: Machine Learning in Python, "\
    "<i>Journal of Machine Learning Research</i>, vol. 12, pp. 2825-2830, 2011.',\n",
    "        '[5] V. N. Vapnik, <i>The Nature of Statistical Learning Theory</i>, "\
    "Springer, 1995.',\n",
    '    ]\n',
]

# lines are 0-indexed; file lines 728-740 = indices 727-739
start = 727  # 0-indexed = line 728
end   = 740  # 0-indexed = line 740 (inclusive, i.e., up to but not including 740)

new_lines = lines[:start] + new_refs + lines[end:]
with open(path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Done. Total lines:", len(new_lines))
