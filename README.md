# The Redactor

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
This will redact names, dates, phones, address and any text that contains the concept name or related content to the concept from the input .txt files and creates outputs for each of those files with a .censored extension.


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


## Flag Parameters and Definitions

### --names

Description: Identifies and redacts personal names from text, covering common name formats in email headers, capitalized names, and names within email addresses.

Patterns Used:
Capitalized Names: Detects names with capitalization patterns, such as "John Doe."
Email Header Names: Matches names from common email fields (e.g., “From,” “To”) using regex.
Email Local Part Names: Redacts names in email addresses like "jane.doe@example.com" by separating components in the local part.

### --dates
Description: Redacts various date formats (e.g., “March 5, 1985,” “05/12/2020,” “12-31-1999”) by recognizing both numeric and written formats.

Patterns Used:
Written Dates: Recognizes dates written out with months (e.g., “January 1, 2020”).
Numeric Dates: Detects numeric formats such as MM/DD/YYYY, DD-MM-YYYY, and other standard variations.

### --phones
Description: Identifies phone numbers in various formats and redacts them, including formats with country codes, hyphens, parentheses, spaces, and dot separators.

Patterns Used:
US Formats: Matches numbers with or without country codes, parentheses around area codes, and hyphens or spaces as separators (e.g., “+1 (123) 456-7890”).
Continuous Digits: Also detects numbers in formats without separators (e.g., “1234567890”).

### --address
Description: Detects and redacts physical (postal) addresses based on standard address components like street numbers, street names, and common address suffixes.

Patterns Used:
Single-line Addresses: Matches conventional address formats like "123 Main St." with flexibility for common address components (e.g., "Avenue," "Blvd").
Multi-line Addresses: Recognizes addresses spanning multiple lines (e.g., with city and state on separate lines).

### --concept
Description: Redacts any sentence or segment in text containing specified keywords or phrases. Concepts can be entered multiple times to include multiple keywords.

Detection Strategy:
Keyword Matching: Uses regex to find exact matches for the specified concept(s) and applies redaction to the entire sentence containing the concept.
Repeated Concepts: Multiple --concept flags may be used to handle more than one thematic redaction requirement.

### --stats
Description: Specifies where to output redaction statistics (stderr, stdout, or a specific file path).

Output Details:
Redaction Counts: Provides counts of each entity type redacted in each processed file.
Position Information: Includes starting and ending indices of redacted text, helpful for debugging or auditing.

## Definition of a Concept

What is a Concept in this project?

In this project, a concept is defined as any word or phrase representing an idea or theme that requires redaction. This differs from other redaction criteria, like names or dates, because it represents a broader thematic category rather than a specific entity type. For example, if the concept "kids" is specified, any mention of information related to children, even if indirect or implied, should be redacted.

### Creating the Context of a Concept
To effectively capture and redact concepts within a contextual scope:

Keyword Matching: Exact keyword matching identifies instances of the concept in text. Each keyword is searched within sentences, and the entire sentence containing the keyword is redacted.
Sentence Segmentation: Using sentence segmentation ensures that any relevant contextual information related to the concept is also redacted. For instance, if "kids" appears within a sentence, the whole sentence will be redacted to avoid leaving any related information that might provide indirect reference.
Multiple Keywords: The --concept flag allows for repeated entries, enabling users to specify multiple keywords representing different aspects of the concept. Each keyword specified will be processed independently to maximize coverage.
Justification for Method
This approach ensures contextually accurate redactions without needing advanced natural language understanding. By redacting entire sentences containing concept keywords, the code:

Minimizes the risk of leaving sensitive thematic information unredacted.
Ensures broader contextual compliance with the redaction requirements for themes that can be nuanced or implied in language.

## Stats Output Format
The --stats flag specifies where the summary of the redaction process should be written. The summary can be directed to a file, stderr, or stdout, and provides detailed statistics to help track redacted items within the document(s).

### Supported Output Locations
File: If a file name is provided, the stats summary will be written to that file.
stderr and stdout: Redirects the stats summary to standard error or standard output.
Stats Format
The stats output includes:

### Total Counts: Number of each type of sensitive entity redacted (e.g., names, dates, phones, addresses, concepts).
Detailed Entry Per File: For each processed file, the stats display the types and counts of entities censored and the starting and ending index of each redacted item within the text

### Explanation
Each file entry in the stats output details:

Filename: The name of the file that was processed.
Types and Counts: For each entity type (e.g., Names, Dates), the number of redactions is provided.
Position Tracking: Each redacted item’s start and end indices are recorded, helping to verify the exact portions of text that were censored.


## Test Case Overview

This project aims to redact sensitive information from text files, such as names, phone numbers, dates, addresses, and specific concepts (e.g., "kids", "prison"). The test suite ensures that the redaction functionality works as expected across different components, validating accuracy, consistency, and robust error handling.

## Test Cases

The test suite is organized to validate individual functionalities in the redactor system, such as merging overlapping redaction spans, redacting specific types of sensitive information (names, dates, phones, addresses), and handling concepts for broader redaction purposes. Each test case targets a specific function or redaction type, verifying correct detection, processing, and statistical tracking of redacted items. This ensures that the redactor accurately censors sensitive content across different inputs and formats, with tests for both successful processing and error handling to maintain reliability and robustness.

The tests are located in the tests/ directory, and each function is tested individually. You can run all the tests using pytest, and each function has been tested with both normal inputs and edge cases.

### 1. `test_merge_overlapping_spans.py`
   - **Purpose**: Tests the merging logic for overlapping, adjacent, and mixed spans in text.
   - **Goal**: Ensures that overlapping spans are merged correctly to prevent redundant redaction, maintaining the integrity of the final redacted text.

### 2. `test_output_redaction_stats.py`
   - **Purpose**: Verifies the accurate output of redaction statistics.
   - **Goal**: Checks that the counts of redacted entities (names, dates, phones, etc.) are output to `stdout`, `stderr`, or a file as specified. Ensures comprehensive and error-free reporting of statistics.

### 3. `test_process_text_file.py`
   - **Purpose**: Simulates the redaction of a sample text file.
   - **Goal**: Tests the end-to-end process, ensuring that the file is read, redacted, and written correctly. Also verifies proper error handling, especially for write permissions, with clear error reporting.

### 4. `test_redact_email_text.py`
   - **Purpose**: Focuses on redacting names in email headers (e.g., "From", "To" fields).
   - **Goal**: Confirms that names in email fields are correctly detected and redacted, with accurate updating of redaction statistics.

### 5. `test_redact_entities_hf.py`
   - **Purpose**: Tests entity redaction using a mocked Hugging Face NER pipeline.
   - **Goal**: Validates the Hugging Face model's integration with the redactor for redacting entities like names and locations, ensuring accurate detection, redaction, and stats.

### 6. `test_redact_entities_regex.py`
   - **Purpose**: Tests regex-based redaction functionality for names, phones, dates, and addresses.
   - **Goal**: Ensures regex patterns match sensitive information correctly, redacting accurately while maintaining consistent statistics and output.

### 7. `test_redact_entities_spacy.py`
   - **Purpose**: Tests the SpaCy-based redactor across various entity types.
   - **Goal**: Verifies SpaCy's capability to accurately redact names, dates, and addresses. Tests both individual and combined entity redaction, ensuring comprehensive coverage.

### 8. `test_redact_sentences_with_concepts.py`
   - **Purpose**: Verifies the redaction of sentences containing specific concepts (e.g., themes like "kids" or "prison").
   - **Goal**: Tests for concept redaction with cases of single and multiple concepts, case insensitivity, multi-sentence redaction, and newline-delimited inputs, ensuring accurate redaction and stats.


## Bugs and Assumptions

### Bugs

Inconsistent Concept Detection: In some cases, the --concept flag may not capture sentences with indirect references to a concept due to limitations in semantic matching. Only explicit mentions or close variations of the concept may be detected.

Overlapping Redaction Issues: Certain overlapping entities (e.g., an address containing a name) may lead to multiple redaction marks, potentially duplicating statistics for the same entity. This can cause inflated counts for certain types of redactions in the stats output.

Complex Address Formats: Uncommon address structures (e.g., international formats or abbreviations) may not be fully detected by the regex patterns. The code currently supports standard US formats, which may lead to incomplete redaction for unfamiliar structures.

Statistical Inconsistencies: In rare cases where multiple entity detection methods (SpaCy, Hugging Face, regex) overlap, the count may reflect additional entities, leading to discrepancies in the final statistics output.

Output Directory Errors: If permissions are insufficient for writing files to the output directory, the program will fail but may not provide detailed feedback. This may obscure the actual cause if users encounter permission errors.

The output_redaction_stats function directly increments redaction counts without checking for duplicates. This might cause inaccurate counts, especially if an entity is identified multiple times by different models.

### Assumptions

File Format Consistency: The project assumes consistent text formatting for input files (e.g., email headers, address structures). Significant changes to file structure could lead to inaccurate entity detection and require modifications to the regex and entity patterns.

Concept Redaction Sensitivity: The --concept flag assumes direct keyword-based detection for specified concepts. It does not include complex semantic analysis, so indirect or loosely related terms may not be redacted.

Encoding Compatibility: The project assumes that all input files are UTF-8 encoded. Files with other encoding formats may result in decoding errors, and users should convert files to UTF-8 beforehand.

Local and Phone Number Formats: The current implementation focuses on standard US phone number and address formats. International formats are not explicitly supported, which may lead to partial or missed redactions for non-standard formats.

Stats Output Destination: It is assumed that the specified --stats argument is a valid and writable path (stdout, stderr, or file path). The program does not validate this extensively, so incorrect paths may cause the output to fail silently.
