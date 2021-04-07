# pdf-anonymize
A python program that uses Microsoft's Presidio Project to anonymize personal identifiable information in pdf and txt files.

Supported PII Identities may be found here: https://microsoft.github.io/presidio/supported_entities/

Currently supports .pdf and .txt files only. Can anonymize data in bulk inside folders.

# Installation

Make a clone of the git repository

```bash
git clone https://github.com/whyroland/anonymize-pdf.git
```

CD into the the cloned repository on your computer

Install the necessary dependencies from the requirements.txt

**IMPORTANT: Presidio is only compatable with spaCy 2.3. If you have a version of spaCy already installed, uninstall it before proceeding further**

```bash
pip freeze > requirements.txt
```

Install the model

```bash
python -m spacy download en_core_web_lg
```

# Usage

Run the script "anonymize.py" to use the program

```bash
python anonymize.py
```

**Place data you want to anonymize inside of the cloned repo folder and enter the file name to anonymize it**

# Screenshots
![menu](img/menu.png)

![bulkexample](img/bulkdata.png)

![txtsample](img/txtsample.png)

![pdfsample](img/emailsample.png)

# Future Plans

- Train the Presidio Model to identify more PIIs
