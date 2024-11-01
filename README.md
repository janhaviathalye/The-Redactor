# cis6930fa24-project1

Project 1 - CIS 6930: Data Engineering Fall 2024

Name: Janhavi Athalye

# Project Description

Overview

In today's digital world, sensitive information is frequently shared in various forms, such as legal documents, medical records, and emails. To protect personal data and comply with privacy standards, redacting sensitive information from such documents is critical. Manual redaction, however, is time-consuming and costly. This project, The Redactor, leverages modern Natural Language Processing (NLP) techniques to automate the redaction process, offering a customizable, efficient solution to detect and redact sensitive information in plain text documents.

Key Features

The Redactor allows users to define which types of sensitive information to censor, including names, dates, phone numbers, addresses, and even broader concepts like "kids" or "prison." The tool is capable of processing various document types (police reports, court transcripts, etc.) and efficiently identifies and censors specified sensitive entities.


# How to install
Ensure you have pipenv installed otherwise install it using the following command.

```
pip install pipenv
```
The following command can also be used.

```
pipenv install -e
```

## How to run

To run the project, execute the following command after activating the pipenv environment:

```
pipenv run python redactor.py --input '*.txt' \
                    --names --dates --phones --address\
                    --concept 'kids' \
                    --output 'files/' \
                    --stats stderr
```
An example command for running the project:

```
pipenv run python redactor.py --input '*.txt' \
                    --names --dates --phones --address\
                    --concept 'Goal' \
                    --output 'files/' \
                    --stats stderr

```
This will download the incident PDF, extract the data, store it in a SQLite database, and print a summary of the incident types and their occurrences.


To run the test cases, execute the following command:
```
pipenv run python -m pytest
```


## Functions

1. **`merge_overlapping_spans(spans)`**
   - Merges overlapping or adjacent character spans to create continuous redaction spans without gaps.

2. **`redact_sentences_with_concepts(text, concepts)`**
   - Identifies sentences containing specified concepts (themes) for redaction, such as "kids" or "prison."

3. **`redact_entities_spacy(text, targets, stats)`**
   - Uses SpaCy’s NER pipeline to detect and redact entities (e.g., names, dates) according to specified targets.

4. **`redact_entities_hf(text, targets, stats)`**
   - Uses a Hugging Face NER model to detect and redact entities in the text, including names and locations.

5. **`redact_email_text(text, targets, stats)`**
   - Extracts and redacts names found in email headers and addresses in the text to ensure sensitive information is removed.

6. **`redact_entities_regex(text, targets, stats)`**
   - Uses regular expressions to identify and redact entities such as names, phone numbers, dates, and addresses.

7. **`output_redaction_stats(stats, destination)`**
   - Outputs redaction statistics, including counts of each type of redaction, to the specified destination (e.g., `stderr`, `stdout`, or a file).

8. **`process_text_file(file_path, args, stats)`**
   - Handles the redaction process for a single text file, including reading the file, applying redactions, and writing the censored content to an output file.

9. **`main()`**
   - Parses command-line arguments, initializes stats, creates output directories, and processes each input file according to the provided flags and options.

## Test Cases

This project includes several test cases designed to verify the correctness and functionality of key functions, such as downloading the incident PDF, extracting data, creating and populating the SQLite database, and querying the database for incident summaries. These tests ensure that each component works as expected and can handle edge cases such as missing data, incorrect formatting, and multiple-line fields.

The tests are located in the tests/ directory, and each function is tested individually. You can run all the tests using pytest, and each function has been tested with both normal inputs and edge cases.

#### test_fetchincidents.py <br />

Purpose: Tests the fetchincidents() function to ensure that it can successfully download a PDF file from the provided URL.

Test Case:

The test case mocks the URL and simulates downloading the data. The response is a mock object that mimics a real PDF download.
It verifies that the function correctly handles the HTTP request and retrieves data.

#### test_extractincidents.py <br />

Purpose: Tests the extractincidents() function, which processes the PDF and extracts the necessary fields like date/time, incident number, location, nature, and ORI.

Test Case:

The test case mocks a PDF file with sample incident data. It verifies that the extractincidents() function correctly parses the PDF and extracts the expected fields.
It also checks that the function can handle multi-line fields and extracts the correct data from each row.

#### test_createdb.py <br />

Purpose: Tests the createdb() function to ensure that a fresh SQLite database is created, and the schema is correctly set up.

Test Case:

The test case checks whether the database file is correctly created in the resources/ directory.
It verifies that the incidents table exists with the correct schema, and no old data remains after creating a new database.

#### test_populatedb.py <br />

Purpose: Tests the populatedb() function, which takes the extracted data and inserts it into the SQLite database.

Test Case:

The test case verifies that the extracted data is correctly inserted into the incidents table.
It checks that the number of records in the table matches the number of incidents passed to the function.


#### test_status.py <br />

Purpose: Tests the status() function, which queries the database and prints a summary of the incident types and their counts.

Test Case:

The test case populates the database with mock data and verifies that the status() function correctly queries the data, sorts the results alphabetically, and prints the correct counts.
It also ensures that the output is formatted correctly, with fields separated by pipes (|) and each row followed by a newline.



## Bugs and Assumptions
Multiple Line Cells: In some cases, cells (like location or nature) may span multiple lines. The code handles this by merging lines that do not start with a new record's date.

PDF Formatting: The Norman Police Department might change the PDF format at any time. The code currently assumes that the format remains consistent (fields are always in the same order).

Network Issues: The project does not currently handle network-related errors, such as the URL being unreachable or the file being moved/removed from the Norman PD website.
