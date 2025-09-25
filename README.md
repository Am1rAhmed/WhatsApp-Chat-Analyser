WhatsApp Chat Analyser
======================

Description:
------------
This project analyses WhatsApp chat exports and provides insights like word clouds, emoji statistics, and URL extraction. 
It uses Python libraries such as pandas, matplotlib, seaborn, wordcloud, and Streamlit for interactive visualization.

Requirements:
-------------
- Python 3.8 or higher
- Virtual environment (.venv)
- Packages:
    pandas
    urlextract
    matplotlib
    wordcloud
    emoji
    streamlit
    preprocessor
    seaborn
    streamlit-lottie

Setup Instructions:
------------------
1. Open PowerShell or terminal in the project folder.

2. Create a virtual environment (if not already created):
   python -m venv .venv

3. Activate the virtual environment:
   - On PowerShell:
     .venv\Scripts\Activate.ps1
   - On Command Prompt:
     .venv\Scripts\activate.bat

4. Install all required packages:
   pip install -r requirements.txt
   (If you do not have requirements.txt, install manually:
   pip install pandas urlextract matplotlib wordcloud emoji streamlit preprocessor seaborn streamlit-lottie)

Running the App:
----------------
1. Make sure the virtual environment is activated.
2. Run the Streamlit app:
   python -m streamlit run whatsapp_chat_analyser.py
3. Open the URL displayed in the terminal in your browser (usually http://localhost:8501).

Notes:
------
- Make sure your project folder contains both `whatsapp_chat_analyser.py` and `helper.py`.
- Ensure that any renamed project folder uses the `.venv` inside it, or recreate the virtual environment if broken.
- The app reads WhatsApp chat export files and generates analytics including:
    - Most frequent words
    - Emoji statistics
    - URLs extracted from chat
    - WordCloud visualization
