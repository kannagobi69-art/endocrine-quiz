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
    # return dict mapping expected logical names to actual header
    lower = [fn.strip() for fn in fieldnames]
    m = {}
    def find_any(possible):
        for p in possible:
            for fn in fieldnames:
                if p.lower() == fn.strip().lower():
                    return fn
        return None
    # Accept many variants
    m['section'] = find_any(['section', 'topics', 'topic'])
    m['question'] = find_any(['question', 'stem', 'prompt'])
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
    # remove BOM and trim
    s = text.strip()
    # remove leading numeric labels like "23. " or "Q1. 23 " or "1)  " or "Q1) "
    s = re.sub(r'^\s*(q\s*\d+[:\.\)]\s*)', '', s, flags=re.I)
    s = re.sub(r'^\s*\d+[:\.\)]\s*', '', s)  # leading digits with dot/parenthesis
    s = s.strip()
    return s

def read_and_convert(csv_file):
    if not os.path.exists(csv_file):
        print(f"CSV file '{csv_file}' not found.")
        return []

    with open(csv_file, 'r', encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        mapping = find_fieldmap(fieldnames)

        questions_out = []
        sections_set = set()
        rownum = 1
        for row in reader:
            rownum += 1
            # fetch fields safely
            section = row.get(mapping['section'], '') if mapping['section'] else ''
            qtext = row.get(mapping['question'], '') if mapping['question'] else ''
            a = row.get(mapping['option_a'], '') if mapping['option_a'] else ''
            b = row.get(mapping['option_b'], '') if mapping['option_b'] else ''
            c = row.get(mapping['option_c'], '') if mapping['option_c'] else ''
            d = row.get(mapping['option_d'], '') if mapping['option_d'] else ''
            correct_raw = row.get(mapping['correct'], '') if mapping['correct'] else ''
            explanation = row.get(mapping['explanation'], '') if mapping['explanation'] else ''

            # Clean strings
            section = section.strip() or 'General'
            qtext = clean_question_text(qtext)
            a = a.strip()
            b = b.strip()
            c = c.strip()
            d = d.strip()
            correct_raw = (correct_raw or '').strip()
            explanation = (explanation or '').strip()

            # If options are in the format "A) text" remove "A) " prefix
            def strip_leading_label(s):
                return re.sub(r'^[A-Da-d][\)\.\-]\s*', '', s).strip()
            a = strip_leading_label(a)
            b = strip_leading_label(b)
            c = strip_leading_label(c)
            d = strip_leading_label(d)

            # Validate presence
            if not qtext or not (a and b and c and d):
                print(f"⚠️ Skipping incomplete question at row {rownum}")
                continue

            # Build option list and shuffle
            options_list = [
                {'key': 'A', 'text': a},
                {'key': 'B', 'text': b},
                {'key': 'C', 'text': c},
                {'key': 'D', 'text': d},
            ]
            # determine correct text before shuffle
            correct_letter = ''
            if correct_raw:
                # accept "A" or "A)" or full text: if letter present use it, else try to match by text
                m = re.match(r'^[A-Da-d]$', correct_raw)
                if m:
                    correct_letter = correct_raw.upper()
                else:
                    # if it's something like "B) " or "B. " pick letter
                    m2 = re.match(r'^([A-Da-d])[\)\.\-]?', correct_raw)
                    if m2:
                        correct_letter = m2.group(1).upper()
                    else:
                        # try to match by option text (case-insensitive)
                        for o in options_list:
                            if o['text'].lower() == correct_raw.lower():
                                correct_letter = o['key']
                                break
            # default: assume A if nothing clear (but we prefer to skip if unknown)
            if not correct_letter:
                # Try to infer if correct_raw is single letter in text, else assume A (less ideal)
                correct_letter = 'A' if correct_raw == '' else correct_raw[:1].upper()

            # Find the correct text value
            correct_text = None
            for o in options_list:
                if o['key'] == correct_letter:
                    correct_text = o['text']
                    break
            # If we didn't find correct_text, try to match by content
            if not correct_text and correct_raw:
                for o in options_list:
                    if correct_raw.strip().lower() == o['text'].strip().lower():
                        correct_text = o['text']
                        break
            if not correct_text:
                # fallback: assume A
                correct_text = options_list[0]['text']

            # shuffle options_list
            random.shuffle(options_list)

            # reassign keys A-D after shuffle
            assigned = {}
            correct_key_after = None
            keys = ['A','B','C','D']
            for idx, o in enumerate(options_list):
                k = keys[idx]
                assigned[k] = o['text']
                if o['text'].strip().lower() == correct_text.strip().lower():
                    correct_key_after = k

            # Build final question object
            qobj = {
                'id': str(uuid.uuid4()),
                'section': section,
                'question': qtext,
                'options': {
                    'A': assigned['A'],
                    'B': assigned['B'],
                    'C': assigned['C'],
                    'D': assigned['D']
                },
                'correct': correct_key_after or 'A',
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
    # produce JS content
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
