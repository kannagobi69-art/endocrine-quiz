#!/usr/bin/env python3
"""
csv_to_questions.py
- Auto-detects headers (flexible)
- Adds 'explanation' (blank if missing)
- Cleans leading numbers from questions
- ALWAYS shuffles options A-D for each question and updates the correct key
- Writes questions.js with `const questions = [...]` and empty `sections` map
"""
import csv
import json
import os
import uuid
import random
import re

CSV_FILE = 'mcqs.csv'
OUT_FILE = 'questions.js'

def normalize(h):
    return h.strip().lower().replace(' ', '_')

def find_fieldmap(fieldnames):
    lower = [fn.strip() for fn in fieldnames]
    m = {}
    def find_any(possible):
        for p in possible:
            for fn in fieldnames:
                if p.lower() == fn.strip().lower():
                    return fn
        return None
    m['section'] = find_any(['section','topics','topic'])
    m['question'] = find_any(['question','stem','prompt'])
    m['option_a'] = find_any(['option a','option_a','a','a)','a.','optiona','opt_a'])
    m['option_b'] = find_any(['option b','option_b','b','b)','b.','optionb','opt_b'])
    m['option_c'] = find_any(['option c','option_c','c','c)','c.','optionc','opt_c'])
    m['option_d'] = find_any(['option d','option_d','d','d)','d.','optiond','opt_d'])
    m['correct'] = find_any(['correct answer','correct','answer','correct_answer'])
    m['explanation'] = find_any(['explanation','rationale','ans_explain'])
    return m

def clean_question_text(text):
    if not text:
        return ''
    s = text.strip()
    s = re.sub(r'^\s*(q\s*\d+[:\.\)]\s*)', '', s, flags=re.I)
    s = re.sub(r'^\s*\d+[:\.\)]\s*', '', s)
    return s.strip()
def read_and_convert(csv_file):
    import chardet  # auto detect encoding if installed
    if not os.path.exists(csv_file):
        print(f"CSV file '{csv_file}' not found.")
        return []

    # --- Step 1: try auto-detect ---
    try:
        raw_data = open(csv_file, 'rb').read(2048)
        try:
            import chardet
            detected = chardet.detect(raw_data)
            enc = detected['encoding'] or 'utf-8'
            print(f"Detected encoding: {enc}")
        except Exception:
            enc = 'utf-8'
    except:
        enc = 'utf-8'

    # --- Step 2: open safely ---
    try:
        csvfile = open(csv_file, newline='', encoding=enc, errors='replace')
    except Exception as e:
        print(f"⚠️ Primary read failed ({e}), retrying Latin-1...")
        csvfile = open(csv_file, newline='', encoding='latin1', errors='replace')

    reader = csv.DictReader(csvfile)
    fieldnames = reader.fieldnames or []
    mapping = find_fieldmap(fieldnames)

    questions_out = []
    sections_set = set()
    rownum = 1

    for row in reader:
        rownum += 1
        section = row.get(mapping['section'], '') if mapping['section'] else ''
        qtext = row.get(mapping['question'], '') if mapping['question'] else ''
        a = row.get(mapping['option_a'], '') if mapping['option_a'] else ''
        b = row.get(mapping['option_b'], '') if mapping['option_b'] else ''
        c = row.get(mapping['option_c'], '') if mapping['option_c'] else ''
        d = row.get(mapping['option_d'], '') if mapping['option_d'] else ''
        correct_raw = row.get(mapping['correct'], '') if mapping['correct'] else ''
        explanation = row.get(mapping['explanation'], '') if mapping['explanation'] else ''

        section = section.strip() or 'General'
        qtext = clean_question_text(qtext)
        a, b, c, d = a.strip(), b.strip(), c.strip(), d.strip()
        correct_raw = (correct_raw or '').strip()
        explanation = (explanation or '').strip()

        if not qtext or not (a and b and c and d):
            print(f"⚠️ Skipping incomplete question at row {rownum}")
            continue

        def strip_label(s):
            return re.sub(r'^[A-Da-d][\)\.\-]\s*', '', s).strip()
        a, b, c, d = map(strip_label, [a,b,c,d])

        options = [{'key':'A','text':a},{'key':'B','text':b},{'key':'C','text':c},{'key':'D','text':d}]
        correct_letter = re.sub(r'[^A-Da-d]', '', correct_raw.upper())[:1] or 'A'
        correct_text = next((o['text'] for o in options if o['key']==correct_letter), a)
        random.shuffle(options)
        assigned, correct_after = {}, None
        for i, o in enumerate(options):
            key = ['A','B','C','D'][i]
            assigned[key] = o['text']
            if o['text'].strip().lower() == correct_text.strip().lower():
                correct_after = key

        qobj = {
            'id': str(uuid.uuid4()),
            'section': section,
            'question': qtext,
            'options': assigned,
            'correct': correct_after or 'A',
            'explanation': explanation or ''
        }
        questions_out.append(qobj)
        sections_set.add(section)

    return questions_out, sorted(list(sections_set))


def write_js(questions, sections):
    data = {
        'questions': questions,
        'sections': {s: {'name': s, 'description': f'Questions about {s}'} for s in sections}
    }
    js = "// Auto-generated questions.js — run csv_to_questions.py to regenerate\n"
    js += "const questions = " + json.dumps(questions, indent=2, ensure_ascii=False) + ";\n\n"
    js += "const sections = " + json.dumps(data['sections'], indent=2, ensure_ascii=False) + ";\n\n"
    js += "if (typeof module !== 'undefined' && module.exports) { module.exports = { questions, sections }; }\n"
    with open(OUT_FILE, 'w', encoding='utf-8') as f:
        f.write(js)
    print(f"✅ Wrote {len(questions)} questions to {OUT_FILE}")

if __name__ == '__main__':
    qlist, sects = read_and_convert(CSV_FILE)
    if not qlist:
        print("No valid questions parsed — check the CSV.")
    else:
        write_js(qlist, sects)
