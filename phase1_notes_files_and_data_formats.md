# Phase 1 Notes — Files and Basic Data Formats

## Phase 1 Goal

The goal of Phase 1 is to understand how data is stored before using libraries like NumPy or pandas.

The main mental model is:

```text
file → parsed data → structure → validation → summary
```

This means:

1. Start with a raw file on disk.
2. Parse the file into Python objects.
3. Understand the structure of the data.
4. Validate the data for problems.
5. Produce a useful summary.

Phase 1 is not about advanced analysis. It is about understanding files, formats, and basic data structure.

---

## 1. Files

A file is data stored on disk.

Common file types in Phase 1:

| File Type | Purpose |
|---|---|
| `.txt` | plain text |
| `.csv` | table-like data |
| `.json` | structured or nested data |

A file extension gives a clue about the format, but it does not guarantee that the content is valid.

Example:

```text
data.json
```

could still contain invalid JSON.

So the program must inspect content, not trust the extension blindly.

---

## 2. Reading vs Parsing vs Inspecting

### Reading

Reading means opening a file and getting its raw content.

Example:

```python
with open("notes.txt", "r") as file:
    content = file.read()
```

### Parsing

Parsing means converting raw file content into Python data structures.

Examples:

```python
csv.DictReader(file)
json.load(file)
```

### Inspecting

Inspecting means analyzing the parsed data to understand its structure and quality.

Examples:

```text
Rows: 4
Columns: 3
Missing values:
age: 1
city: 1
```

Printing a file is not the same as inspecting it.

---

## 3. TXT Files

TXT files are plain text.

They do not naturally have rows and columns like CSV files.

For TXT files, useful inspection includes:

```text
lines
words
characters
```

Example logic:

```python
lines = content.splitlines()
words = content.split()
characters = len(content)
```

### Important methods

| Method | Meaning |
|---|---|
| `splitlines()` | splits text into lines |
| `split()` | splits text into words/tokens |
| `len(content)` | counts characters |

A TXT file containing only spaces should usually be treated as empty because it has no meaningful content.

---

## 4. CSV Files

CSV means **Comma-Separated Values**.

A CSV is table-like.

Example:

```csv
name,age,city
Ali,22,Toronto
Sara,29,Vancouver
John,35,Calgary
```

### CSV Concepts

| Concept | Meaning |
|---|---|
| row | one record/observation |
| column | one variable/field |
| header | first line containing column names |
| cell | one value at row-column intersection |

For the example above:

```text
Rows: 3
Columns: 3
Column names: name, age, city
```

---

## 5. `csv.reader` vs `csv.DictReader`

### `csv.reader`

Returns each row as a list.

Example:

```python
["Ali", "22", "Toronto"]
```

Problem: values are accessed by position.

```python
row[0]  # name
row[1]  # age
row[2]  # city
```

This is fragile because the meaning depends on column order.

### `csv.DictReader`

Returns each row as a dictionary.

Example:

```python
{"name": "Ali", "age": "22", "city": "Toronto"}
```

This is better because values are accessed by column name.

```python
row["name"]
row["age"]
row["city"]
```

### Why `DictReader` is better for the project

`csv.DictReader` is better because:

- it connects values to column names
- it makes missing-value checks easier
- it makes preview output clearer
- it prepares the mental model for pandas DataFrames
- it is less fragile than position-based indexing

---

## 6. CSV Missing Values

A CSV value should count as missing if it is:

```text
empty string
blank cell
None
spaces only
```

Example:

```csv
name,age,city
Ali,22,Toronto
Sara,,Vancouver
John,35,
```

Missing counts:

```text
name: 0
age: 1
city: 1
```

Important distinction:

```text
0 is not missing
"0" is not missing
False is not missing
```

Missing means no value was provided. Zero is a real value.

---

## 7. JSON Files

JSON means **JavaScript Object Notation**.

JSON is often used by APIs and configuration files.

Example:

```json
[
  {"name": "Ali", "age": 22, "city": "Toronto"},
  {"name": "Sara", "age": 29, "city": "Vancouver"}
]
```

In this project, valid JSON shape means:

```text
list of dictionaries
```

Each dictionary is one record.

---

## 8. JSON Records and Keys

Example:

```json
[
  {"name": "Ali", "age": 22},
  {"name": "Sara", "city": "Vancouver"},
  {"name": "John", "age": 35}
]
```

All keys are:

```text
name, age, city
```

Missing counts:

```text
name: 0
age: 1
city: 2
```

Why?

- `name` exists in all records
- `age` is missing for Sara
- `city` is missing for Ali and John

---

## 9. Why JSON Is Harder Than CSV

JSON is harder to inspect because:

1. JSON can have inconsistent keys.
2. JSON can be nested.
3. JSON can have many possible top-level shapes.
4. JSON values can be different types.
5. JSON may be valid but not match the structure your program expects.

Examples of unsupported JSON shapes for this project:

```json
{"name": "Ali", "age": 22}
```

This is a dictionary, not a list of dictionaries.

```json
[1, 2, 3]
```

This is a list, but not a list of dictionaries.

```json
["Ali", "Sara", "John"]
```

This is also a list, but not a list of records.

---

## 10. Missing Key vs Empty Value

These are different:

```json
{"name": "Sara"}
```

If `age` is expected, then `age` is a missing key.

```json
{"name": "Sara", "age": ""}
```

Here, `age` exists, but the value is empty.

Both count as missing data, but they are structurally different.

| Case | Meaning |
|---|---|
| missing key | field is absent |
| empty value | field exists but has no useful value |

---

## 11. The `is_missing()` Function

A good missing-value helper:

```python
def is_missing(value):
    if value is None:
        return True

    if isinstance(value, str) and value.strip() == "":
        return True

    return False
```

This returns `True` for:

```python
None
""
"   "
```

It returns `False` for:

```python
0
"0"
False
"Ali"
```

### Why this should be a separate function

Because the same logic is needed in:

```text
CSV inspection
JSON inspection
preview printing
missing-value counting
```

If the logic is repeated everywhere, the program becomes harder to maintain.

---

## 12. Preview Function

The preview function shows the first few records.

Example:

```text
Preview:
1. name=Ali, age=22, city=Toronto
2. name=Sara, age=MISSING, city=Vancouver
3. name=John, age=35, city=MISSING
```

A good preview should show `MISSING` instead of a blank value because blank output is ambiguous.

Blank could mean:

```text
missing value
printing bug
spacing issue
empty string
missing key
```

`MISSING` makes the problem explicit.

---

## 13. File-Type Detection

The `detect_file_type(file_path)` function should return:

```python
"csv"
"json"
"txt"
None
```

Example:

```python
detect_file_type("people.csv")   # "csv"
detect_file_type("data.json")    # "json"
detect_file_type("notes.txt")    # "txt"
detect_file_type("image.png")    # None
```

A strong version should handle uppercase extensions:

```python
detect_file_type("people.CSV")   # "csv"
```

by normalizing the extension to lowercase.

---

## 14. Error Handling

The project should handle these errors:

| Problem | Expected Response |
|---|---|
| no file path | print helpful error |
| file does not exist | print `Error: File not found.` |
| unsupported file type | reject clearly |
| empty file | print `Error: File is empty.` |
| invalid JSON | print `Error: Invalid JSON format.` |
| wrong JSON shape | print `Error: JSON must be a list of dictionaries.` |

Error handling matters because real files are messy.

A program that only works on perfect files is weak.

---

## 15. `main()` Function

The `main()` function controls the program flow.

It should:

1. Read command-line arguments.
2. Check whether a file path was provided.
3. Check whether the file exists.
4. Detect file type.
5. Call the correct inspection function.
6. Stop clearly when there is an error.

`main()` should not contain all CSV, JSON, and TXT parsing logic.

That logic belongs in:

```python
inspect_csv()
inspect_json()
inspect_txt()
```

---

## 16. Inspection Functions

### `inspect_txt(file_path)`

Should:

```text
open file
read content
check empty
count lines
count words
count characters
print summary
```

### `inspect_csv(file_path)`

Should:

```text
open CSV file
parse with csv.DictReader
get columns
read rows
count rows
count columns
print preview
count missing values
```

### `inspect_json(file_path)`

Should:

```text
open JSON file
parse with json.load
catch invalid JSON
check list of dictionaries shape
collect all keys
count records
print preview
count missing keys and values
```

---

## 17. Why Functions Matter

Functions make the program easier to:

```text
read
test
debug
extend
reuse
```

Good function separation:

```python
detect_file_type()
is_missing()
inspect_csv()
inspect_json()
inspect_txt()
print_preview()
main()
```

Each function should have one clear responsibility.

---

## 18. Important Edge Cases

### Header-only CSV

```csv
name,age,city
```

This is not a physically empty file. It has columns but no data rows.

A strong program should distinguish:

```text
empty file
header-only CSV
normal CSV
```

### Empty JSON list

```json
[]
```

This is valid JSON, but it contains no records.

It should be treated as empty data, not invalid JSON.

### JSON list of empty dictionaries

```json
[
  {},
  {}
]
```

This is technically a list of dictionaries, but there are no keys.

A strong program should report that the records contain no fields.

### CSV row with extra value

```csv
name,age
Ali,22,Toronto
```

`csv.DictReader` may store the extra value under key `None`.

This is a structural issue worth detecting in a stronger version.

### CSV row with fewer values

```csv
name,age,city
Ali,22
```

The missing `city` should count as missing.

---

## 19. Type Inference Stretch Goal

Type inference means guessing whether values represent:

```text
integer
float
boolean
string
missing
```

Example:

```text
"22" → integer
"3.14" → float
"true" → boolean
"" → missing
"Ali" → string
```

Important idea:

CSV values start as strings. Type inference guesses the semantic type.

Example:

```text
"22"
```

Stored form: string  
Possible meaning: integer

Missing values should usually be ignored when deciding the main type of a column.

---

## 20. Exporting a Summary Report

Exporting a report to:

```text
summary_report.txt
```

is useful because:

```text
the result is saved
someone else can review it
it supports automation
it creates an audit trail
terminal output disappears after the program ends
```

This matters in real data workflows.

---

## 21. How This Prepares for NumPy

This project prepares for NumPy because it teaches:

```text
structured data
rows and columns
missing values
validation before computation
why plain Python lists become limiting
why consistent structure matters
```

NumPy will focus on:

```text
arrays
shape
dtype
indexing
slicing
vectorized operations
numerical summaries
```

---

## 22. How This Prepares for Pandas

This project prepares for pandas because pandas automates many things you manually built.

Manual Phase 1 skill:

```python
csv.DictReader()
```

Pandas version:

```python
pd.read_csv()
```

Manual Phase 1 skill:

```text
count rows and columns
```

Pandas version:

```python
df.shape
```

Manual Phase 1 skill:

```text
count missing values
```

Pandas version:

```python
df.isna().sum()
```

Manual Phase 1 skill:

```text
preview first records
```

Pandas version:

```python
df.head()
```

---

## 23. List of Dictionaries vs DataFrame

A list of dictionaries:

```python
[
    {"name": "Ali", "age": 22},
    {"name": "Sara", "age": 29}
]
```

is similar to a DataFrame because:

```text
each dictionary is like a row
each key is like a column
each value is like a cell
```

But the analogy breaks because pandas adds:

```text
index
column data types
vectorized operations
standard missing-value tools
better performance
built-in summaries and filtering
```

A DataFrame is not just a list of dictionaries. It is a more powerful labeled data structure.

---

## 24. Final Architecture Summary

The Data Inspector architecture:

1. User runs:

```bash
python data_inspector.py people.csv
```

2. `main()` checks whether a path was provided.

3. `main()` checks whether the file exists.

4. `detect_file_type()` checks the extension.

5. `main()` calls the right inspector:

```python
inspect_csv()
inspect_json()
inspect_txt()
```

6. The inspector opens and parses the file.

7. The inspector measures the structure:

```text
rows/columns
records/keys
lines/words/characters
```

8. Missing values are detected using:

```python
is_missing()
```

9. Preview is printed using:

```python
print_preview()
```

10. Errors are handled clearly.

11. The final output summarizes the file’s structure and quality.

---

## 25. Phase 1 Completion Standard

You are done with Phase 1 if you can build the Data Inspector from a blank file and explain:

```text
why each function exists
how CSV parsing works
how JSON parsing works
how TXT inspection works
how missing values are detected
how errors are handled
how preview works
how this prepares for NumPy and pandas
```

If you only copied the solution, you are not done.

If you can rebuild it, debug it, and explain it, Phase 1 is complete.

---

## Final Hard Questions

Before moving to Phase 2, answer these:

1. Why is `csv.DictReader` better than `csv.reader` for this project?
2. Why is JSON harder to inspect than CSV?
3. What is the difference between a missing key and an empty value?
4. Why should `0` not count as missing?
5. Why should `is_missing()` be a separate function?
6. Does a file extension prove the file content is valid?
7. How does a list of dictionaries prepare you for pandas?
8. Where does the list-of-dictionaries analogy break?
9. Why is inspection more than printing?
10. What would change if the file had 1 million rows?
