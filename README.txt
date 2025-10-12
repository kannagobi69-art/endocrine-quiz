====================================================
   🩺  SCHOOL OF NURSING - ENDROCRINE QUIZ SYSTEM
====================================================

Prepared by:  K. KANNAN  
Edition:      Final Interactive Version (2025)  
Theme:        Pink → Peach Gradient (Friendly Classroom Vibe)

----------------------------------------------------
📁  FOLDER STRUCTURE (Keep all these files together)
----------------------------------------------------
D:\Endocrine Quiz\
│
├── mcqs.csv                ← Your master question file (editable in Excel)
├── csv_to_questions.py     ← Python converter (builds questions.js)
├── questions.js            ← Auto-generated file (no need to edit manually)
├── index.html              ← The main quiz webpage
├── script.js               ← Quiz logic (dynamic, review, explanations)
├── style.css               ← Visual design (pink–peach theme, circular options)
└── run_converter.bat       ← Double-click to update questions & open quiz
    ↑
    Use this file every time you modify your mcqs.csv

----------------------------------------------------
🧠  PURPOSE OF EACH FILE
----------------------------------------------------
✅ mcqs.csv
   - This is your main question bank.
   - You can open it in Excel and add/edit/delete questions.
   - Each row should have:
       Section | Question | Option A | Option B | Option C | Option D | Correct | Explanation
   - The "Explanation" column is optional; left blank if not needed.

✅ csv_to_questions.py
   - Converts mcqs.csv into questions.js automatically.
   - Cleans question text (removes numbers like "Q1. 23").
   - Randomly shuffles options (A, B, C, D) each time you run it.
   - Keeps correct answers and explanations accurate after shuffle.
   - Adds an empty "explanation" field automatically if not present.

✅ questions.js
   - Auto-generated JavaScript question database.
   - You should never edit this manually.
   - It is used by script.js to display questions in the quiz.

✅ index.html
   - The main webpage of your quiz system.
   - Displays: Start screen, Quiz interface, Results, Review Answers, and History.
   - Tagline: “Prepared by K. Kannan” in stylish font.

✅ script.js
   - Core logic of your quiz:
       • Loads questions dynamically
       • Shows one question at a time
       • Displays correct/wrong answers instantly
       • Supports keyboard answers (A/B/C/D + Enter)
       • Adds “Review Answers” button on the Results page
       • Allows explanations to show after each question
       • Saves history in localStorage (for tracking past attempts)

✅ style.css
   - Visual style: Pink → Peach gradient theme.
   - Adds circular A/B/C/D option badges (colored).
   - Smooth animations, hover effects, and readable text.
   - Improved contrast for attempt history.

✅ run_converter.bat
   - The simplest way to update your quiz.
   - What it does:
       1. Runs csv_to_questions.py automatically.
       2. Shuffles options and regenerates questions.js.
       3. Opens your quiz (index.html) in your browser.
       4. Opens your folder for quick access.
   - Double-click this file every time after you edit mcqs.csv.

----------------------------------------------------
🚀  HOW TO UPDATE QUESTIONS
----------------------------------------------------
1️⃣  Open mcqs.csv in Excel.
2️⃣  Add or edit questions (ensure all 4 options are filled).
3️⃣  Save and close the file.
4️⃣  Double-click run_converter.bat.
5️⃣  Wait for it to say:
       ✅ Conversion complete! questions.js successfully updated.
6️⃣  The quiz webpage (index.html) will open automatically.
7️⃣  Start the quiz and enjoy the new shuffled version!

----------------------------------------------------
🎯  MAIN FEATURES
----------------------------------------------------
⭐  Clean interface with pastel pink–peach gradient
⭐  Stylish “Prepared by K. Kannan” tagline
⭐  Circular A/B/C/D option badges (color-coded)
⭐  Automatic option shuffle (every time you run converter)
⭐  Correct answer + explanation displayed instantly
⭐  Review Answers screen (after finishing the quiz)
⭐  Attempt History (stored locally on computer)
⭐  Works completely offline (no internet needed)
⭐  Fully compatible with any browser (Chrome, Edge, Firefox)

----------------------------------------------------
❓  FREQUENTLY ASKED QUESTIONS
----------------------------------------------------
Q: Should I delete questions.js before converting?
A: No. The converter overwrites it automatically.

Q: Can I edit questions.js manually?
A: Not recommended. Always edit mcqs.csv and re-run the converter.

Q: What if Python is not installed?
A: Install Python 3.x from https://www.python.org/downloads/
   Make sure to tick “Add Python to PATH” during installation.

Q: How do I add explanations later?
A: Add a new column “Explanation” in mcqs.csv if not already present.
   Type short notes in each row. Run the converter again.

Q: Can this quiz run on other computers?
A: Yes! Copy the entire “Endocrine Quiz” folder to another PC.
   Just ensure Python is installed there to regenerate questions.js.

----------------------------------------------------
🩵  NOTES & MAINTENANCE
----------------------------------------------------
• Keep a backup of mcqs.csv (your original question data).
• Run run_converter.bat every time you make changes.
• The converter shuffles options randomly each time for fairness.
• Explanations stay linked correctly after every shuffle.
• The quiz stores history only on your local device.

----------------------------------------------------
📣  CREDITS
----------------------------------------------------
System Design  :  K. Kannan  
Development    :  ChatGPT (OpenAI GPT-5)  
Version        :  2025 Interactive Edition

----------------------------------------------------
📅  Last Updated:  October 2025
====================================================
