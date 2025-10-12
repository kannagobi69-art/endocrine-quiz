PROJECT OVERVIEW

This system provides an interactive quiz platform for nursing students, allowing them to practice unit-wise or randomized multiple-choice questions with immediate feedback, explanations, and review options.
The quiz database is automatically generated from a CSV file using a Python converter.

Endocrine Quiz/
│
├── index.html          → Main webpage  
├── style.css           → Main design and layout  
├── responsive.css      → Mobile optimization styling  
├── script.js           → Interactive quiz logic  
├── questions.js        → Auto-generated questions file  
├── mcqs.csv            → Editable question database  
├── csv_to_questions.py → Python converter (CSV → JS)  
├── run_converter.bat   → One-click auto converter  
└── README.txt          → Documentation (this file)

🚀 HOW TO UPDATE QUESTIONS

1️⃣ Open mcqs.csv in Excel or Google Sheets.

Columns required:
Section, Question, A, B, C, D, Correct, Explanation

2️⃣ Add or edit questions as needed.

Include your new sections (e.g., “Scenario-Based”, “Clinical Practice”).

Ensure each question has all four options filled.

3️⃣ Save as UTF-8 encoded CSV.

In Excel:
File → Save As → Save as type: All Files → Encoding: UTF-8

4️⃣ Run the converter.

Double-click run_converter.bat.

The script will automatically generate a new questions.js file.

🐍 PYTHON INSTALLATION & REQUIRED PACKAGES

If you’re setting this up for the first time or on a new computer:

1️⃣ Install Python

Download from: https://www.python.org/downloads/

During installation, check the box: ✅ “Add Python to PATH”

2️⃣ Verify installation

Open Command Prompt → type:
python --version
You should see something like:
Python 3.12.3

3️⃣ Install the required package (chardet)

In Command Prompt, type:

python -m pip install chardet


This library auto-detects the CSV file’s encoding (UTF-8, Latin-1, etc.).

4️⃣ Run the converter

Double-click run_converter.bat again.

You’ll see messages like:

Detected encoding: Windows-1252
✅ Wrote 670 questions to questions.js

🎯 MAIN FEATURES

✅ Automatic section detection and question shuffling
✅ Real-time feedback with correct answer display
✅ Review screen showing explanations after each quiz
✅ Attempt history saved in browser (via localStorage)
✅ Section-wise performance summary
✅ Mobile and tablet responsive design
✅ Offline operation (no internet required)
✅ Modern soft pastel UI (nursing-themed)
✅ Prepared by K. Kannan (School of Nursing)

📱 MOBILE OPTIMIZATION

Auto-resizes layout for all screen sizes.

Includes instruction: “Move the screen upward to view your questions” for mobile users.

Buttons and fonts are touch-friendly.

🧠 ADDING SCENARIO-BASED QUESTIONS

1️⃣ Add your case or clinical scenario questions at the end of mcqs.csv.
2️⃣ Ensure each has a section name like “Scenario-Based Questions”.
3️⃣ Add detailed explanations in the Explanation column.
4️⃣ Run run_converter.bat again — new sections appear automatically.
⚙️ TROUBLESHOOTING
| Problem                            | Likely Cause               | Solution                                       |
| ---------------------------------- | -------------------------- | ---------------------------------------------- |
| Apostrophes show as `�`            | CSV not saved as UTF-8     | Re-save file in UTF-8 format                   |
| Python error: `UnicodeDecodeError` | CSV encoding issue         | Use `chardet` (auto-detects encoding)          |
| “No module named chardet”          | Missing package            | Run `python -m pip install chardet`            |
| New section not showing            | Wrong header or blank cell | Verify column names and values                 |
| Home or Review not working         | Old JS files               | Replace with latest script.js and questions.js |

💾 BACKUP & HOSTING OPTIONS

You can host this project:

On Vercel (recommended for free deployment)

On GitHub Pages (static site)

Embedded inside Blogspot using <iframe>

Example:

<iframe src="https://endocrine-quiz.vercel.app"
        width="100%" height="800" style="border:none;"></iframe>

🧮 EDUCATIONAL VALUE

This project demonstrates:

Integration of Python → JavaScript data automation

Use of CSV files for scalable content

Proper UTF-8 encoding practices

Real-time interactive assessment design

Mobile learning (m-learning) implementation for nursing education

✨ FUTURE IMPROVEMENTS

🔊 Add voice narration (text-to-speech)

🏫 Class-based result storage (Google Sheets sync)

🖼️ Image-based questions

📊 Leaderboard and scoring reports

💾 PDF export of attempt results

👩‍🏫 Prepared and Maintained by

K. Kannan, M.Sc (N)
School of Nursing
Dedicated to advancing digital learning in nursing education.