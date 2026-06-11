# Phase 1 Data Inspector — Answer Key

This answer key is for checking understanding after completing the **Data Inspector CLI** project.

Project goal:

```text
file → parsed data → structure → validation → summary
```

Use this file to compare your written answers and confirm that you understand Phase 1: files, CSV, JSON, TXT, functions, missing values, and basic validation.

---

## Q1. What does this pipeline mean?

```text
file → parsed data → structure → validation → summary
```

In the project:

- **file**: the raw `.csv`, `.json`, or `.txt` stored on disk.
- **parsed data**: Python converts the file into usable objects:
  - CSV → list of dictionaries
  - JSON → list of dictionaries
  - TXT → string content
- **structure**: the program identifies rows, columns, records, keys, lines, words, or characters.
- **validation**: the program checks for missing values, wrong JSON shape, invalid JSON, empty files, unsupported extensions, etc.
- **summary**: the program prints useful information about the data, not just the raw content.

---

## Q2. What is the difference between reading, parsing, and inspecting a file?

**Reading a file** means opening it and getting the raw content.

**Parsing a file** means converting that content into Python data structures.

Examples:

```python
file.read()          # reading text
csv.DictReader(file) # parsing CSV rows
json.load(file)      # parsing JSON
```

**Inspecting a file** means analyzing the parsed content to understand its structure and quality.

Example:

```text
Rows: 4
Columns: 3
Missing age values: 1
```

---

## Q3. Why is printing file contents a weak version of inspection?

Printing file contents is weak because it does not tell you whether the data is usable.

Inspection should answer questions like:

```text
How many rows?
What columns exist?
Are keys missing?
Are values blank?
Is the JSON shape valid?
```

Printing is display. Inspection is structural analysis.

---

## Q4. What should `detect_file_type()` return?

```python
detect_file_type("people.csv")
```

should return:

```python
"csv"
```

For:

```python
detect_file_type("people.CSV")
```

A strong implementation should also return:

```python
"csv"
```

by using lowercase normalization:

```python
extension = extension.lower()
```

Reason: file extensions may use uppercase or mixed case. A robust program should handle that.

---

## Q5. Does a `.json` extension prove the file contains valid JSON?

No. A `.json` extension does **not** prove the file contains valid JSON.

| Concept | Meaning |
|---|---|
| file extension | name label at the end of file path |
| file content | actual text/data inside the file |
| format validity | whether the content follows the rules of the format |

Example:

```text
broken.json
```

could contain:

```text
hello this is not json
```

The extension says “intended JSON.” Parsing proves whether it is valid JSON.

---

## Q6. What happens if someone renames a broken text file to `data.csv`?

The extension is detected by:

```python
detect_file_type(file_path)
```

But content problems are discovered inside:

```python
inspect_csv(file_path)
inspect_json(file_path)
inspect_txt(file_path)
```

The extension chooses the inspector; the inspector checks the actual structure.

---

## Q7. Why should `0` not count as missing?

`0` should not count as missing because it is a real value.

Examples:

```text
age = 0
quantity = 0
score = 0
```

Depending on the domain, `0` may be valid or invalid, but it is not the same as missing.

Missing means “no value was provided.”

Zero means “a value was provided, and that value is zero.”

---

## Q8. What should `is_missing()` return?

Expected results:

```python
is_missing(None)      # True
is_missing("")        # True
is_missing("   ")     # True
is_missing("0")       # False
is_missing(0)         # False
is_missing(False)     # False
```

Difference between `"0"` and `0`:

| Value | Type | Meaning |
|---|---|---|
| `"0"` | string | text containing the character zero |
| `0` | integer | numeric zero |

Both are present values, not missing values.

---

## Q9. Why put missing-value logic in one function?

Putting missing-value logic in one function is better because:

- CSV and JSON both need the same rule.
- Preview also needs the same rule.
- If the rule changes, you update one place.
- It avoids duplicated fragile logic.
- It makes the code easier to test.

This is separation of responsibility.

---

## Q10. CSV count example

Given:

```csv
name,age,city
Ali,22,Toronto
Sara,,Vancouver
John,35,
```

Counts:

```text
Rows: 3
Columns: 3
Column names: name, age, city
```

Missing values:

```text
name: 0
age: 1
city: 1
```

Explanation:

- Sara has missing `age`.
- John has missing `city`.
- No missing `name`.

---

## Q11. Why use `csv.DictReader` instead of `csv.reader`?

`csv.DictReader` is better than `csv.reader` because it maps each row to column names.

With `csv.reader`, a row looks like:

```python
["Ali", "22", "Toronto"]
```

You must remember:

```text
index 0 = name
index 1 = age
index 2 = city
```

With `csv.DictReader`, a row looks like:

```python
{"name": "Ali", "age": "22", "city": "Toronto"}
```

This is better because:

- values are accessed by meaning, not position
- missing values can be checked by column name
- preview output can use key-value pairs
- it resembles a table/DataFrame mental model
- it is less fragile if column order changes

---

## Q12. What does one row from `csv.DictReader` look like?

For:

```csv
name,age,city
Ali,22,Toronto
```

one row from `csv.DictReader` is approximately:

```python
{"name": "Ali", "age": "22", "city": "Toronto"}
```

Important: CSV values are usually read as strings, so `"22"` is not automatically the integer `22`.

---

## Q13. Why does `csv.DictReader` prepare you for pandas?

`csv.DictReader` teaches the mental model:

```text
column name → value
record/row → collection of column values
list of rows → table-like structure
```

A pandas DataFrame also uses named columns and row records, but adds stronger features later:

```text
index
column dtypes
vectorized operations
missing-value handling
fast filtering/grouping
```

---

## Q14. What is wrong with this code?

```python
with open(file_path, "r") as file:
    reader = csv.DictReader(file)

rows = list(reader)
```

`rows = list(reader)` happens **after** the `with` block ends. At that point, the file is closed.

The reader still depends on the open file, so reading outside the `with` block can fail.

Correct pattern:

```python
with open(file_path, "r") as file:
    reader = csv.DictReader(file)
    rows = list(reader)
```

---

## Q15. What if a CSV has headers but no data rows?

For:

```csv
name,age,city
```

A defensible answer:

```text
Rows: 0
Columns: 3
Column names: name, age, city
```

This file is not completely empty; it has a header/schema but no data records.

For a beginner project, it is also acceptable to report:

```text
Error: File has no data rows.
```

Best answer: distinguish between:

```text
physically empty file → no content at all
header-only CSV → schema exists but no records
```

---

## Q16. Why is JSON harder to inspect than CSV?

JSON is harder to inspect than CSV because:

1. JSON can have inconsistent keys across records.
2. JSON can be nested.
3. JSON can have different top-level shapes:
   - object
   - list
   - list of objects
   - list of numbers
4. JSON values can have mixed types:
   - strings
   - numbers
   - booleans
   - null
   - lists
   - dictionaries

CSV is usually flatter: rows and columns.

---

## Q17. Why require JSON to be a list of dictionaries?

The JSON inspector requires a **list of dictionaries** because the project treats JSON records like table rows.

Valid:

```json
[
  {"name": "Ali", "age": 22},
  {"name": "Sara", "age": 29}
]
```

Each dictionary is one record.

Rejected:

```json
{"name": "Ali", "age": 22}
```

because it is a single dictionary, not a dataset of records. It does not match the expected shape for this project.

---

## Q18. Why reject `[1, 2, 3]`?

Reject:

```json
[1, 2, 3]
```

because it is a list, but not a list of dictionaries.

Each item is a number, not a record with keys and values.

The inspector expects:

```text
record = dictionary
dataset = list of dictionaries
```

---

## Q19. JSON missing-count example

Given:

```json
[
  {"name": "Ali", "age": 22},
  {"name": "Sara", "city": "Vancouver"},
  {"name": "John", "age": 35}
]
```

All keys:

```text
name, age, city
```

Missing counts:

```text
name: 0
age: 1
city: 2
```

Explanation:

- `name` exists in all 3 records.
- `age` is missing for Sara.
- `city` is missing for Ali and John.

---

## Q20. Why is `keys = list(records[0].keys())` weak?

This is weak:

```python
keys = list(records[0].keys())
```

because it only uses the first record’s keys.

Example failure:

```json
[
  {"name": "Ali"},
  {"name": "Sara", "age": 29},
  {"name": "John", "city": "Calgary"}
]
```

Using only the first record gives:

```text
name
```

But the full dataset has:

```text
name, age, city
```

A better approach collects keys from every record.

---

## Q21. Missing key vs empty value

Difference:

```json
{"name": "Sara"}
```

Here, `age` is a **missing key** if `age` is expected.

```json
{"name": "Sara", "age": ""}
```

Here, `age` key exists, but the value is empty.

Both count as missing data for `age`, but they are not structurally the same:

| Case | Meaning |
|---|---|
| missing key | field absent |
| empty value | field present but blank |

---

## Q22. Why count lines, words, and characters for TXT?

TXT files do not have a formal row/column structure.

So we inspect text using:

```text
lines
words
characters
```

Rows and columns are table concepts. TXT is plain unstructured text.

---

## Q23. `splitlines()` vs `split()`

```python
content.splitlines()
```

splits text into lines.

Example:

```text
Line 1
Line 2
```

becomes:

```python
["Line 1", "Line 2"]
```

```python
content.split()
```

splits text into words/tokens separated by whitespace.

Example:

```text
hello world
```

becomes:

```python
["hello", "world"]
```

---

## Q24. Should a TXT file containing only spaces be empty?

Yes. A TXT file containing only spaces should be considered empty for inspection purposes.

Reason:

```python
content.strip() == ""
```

means there is no meaningful text content.

The file has characters physically, but no useful data.

---

## Q25. Which errors belong in `main()` vs inspection functions?

`main()` should handle high-level program flow errors, such as:

```text
no file path provided
unsupported file type
file does not exist
choosing the correct inspector
```

Inspection functions should handle format-specific problems, such as:

```text
invalid JSON
wrong JSON shape
empty content
CSV structure issues
TXT content counting
```

A good design keeps `main()` as the dispatcher, not the worker.

---

## Q26. Why catch `json.JSONDecodeError` inside `inspect_json()`?

We catch:

```python
json.JSONDecodeError
```

inside `inspect_json()` because this error happens when parsing JSON content:

```python
json.load(file)
```

It is JSON-specific, so the JSON inspector is the natural place to handle it.

---

## Q27. What if the user provides no file path?

If the user runs:

```bash
python data_inspector.py
```

the program should print:

```text
Error: Please provide a file path.
Example: python data_inspector.py people.csv
```

Then stop.

---

## Q28. What if the user gives an unsupported file?

If the user runs:

```bash
python data_inspector.py image.png
```

the program should print:

```text
Error: Unsupported file type.
Supported types: .csv, .json, .txt
```

Then stop.

---

## Q29. What if the file does not exist?

If the user runs:

```bash
python data_inspector.py missing.csv
```

the program should print:

```text
Error: File not found.
```

This should usually be detected in `main()` before calling the inspector, using something like:

```python
os.path.exists(file_path)
```

or handled with `FileNotFoundError`.

---

## Q30. Why is `print_preview()` useful for both CSV and JSON?

`print_preview(records, keys, limit=3)` is useful for both CSV and JSON because both are represented as:

```text
list of dictionaries
```

CSV with `DictReader`:

```python
{"name": "Ali", "age": "22"}
```

JSON record:

```python
{"name": "Ali", "age": 22}
```

So the same preview logic can work for both.

---

## Q31. Preview example

Given:

```python
record = {"name": "Sara", "city": "Vancouver"}
keys = ["name", "age", "city"]
```

Preview should show:

```text
name=Sara, age=MISSING, city=Vancouver
```

Because `age` is missing.

---

## Q32. Why show `MISSING` instead of a blank?

Missing preview values should show:

```text
MISSING
```

instead of blank because blank output is ambiguous.

Blank could mean:

```text
empty string
missing key
printing bug
spacing problem
```

`MISSING` makes the data-quality issue explicit.

---

## Q33. Why use separate inspection functions?

Separate functions are better because each format has different logic:

```text
CSV → headers, rows, columns
JSON → list of dictionaries, keys, shape validation
TXT → lines, words, characters
```

One huge function would be harder to:

```text
read
test
debug
extend
reuse
```

This is separation of concerns.

---

## Q34. What is the responsibility of `main()`?

`main()` should:

```text
read command-line arguments
check that a file path was provided
check whether the file exists
detect file type
call the correct inspection function
handle high-level flow
```

`main()` should **not** contain all CSV/JSON/TXT parsing logic. That belongs in the inspection functions.

---

## Q35. What changes if XML support is added?

If adding XML support, change:

- `detect_file_type()` to recognize `.xml`
- add `inspect_xml(file_path)`
- update `main()` to call `inspect_xml()`
- update supported file type message

Stay the same:

- command-line structure
- high-level `main()` dispatcher pattern
- error-handling idea
- helper ideas like preview/missing logic where applicable

---

## Q36. What should happen with an empty CSV file?

For an empty CSV file with no content, print:

```text
Error: File is empty.
```

If it has only headers but no rows, better answer:

```text
Rows: 0
Columns: <number>
Column names: ...
```

or:

```text
Error: File has no data rows.
```

But do not confuse header-only with physically empty.

---

## Q37. What should happen with `[]` JSON?

For:

```json
[]
```

It is valid JSON and the correct broad shape, because it is a list.

But it contains no records.

Best output:

```text
Error: File is empty.
```

More precise:

```text
Error: JSON contains no records.
```

It is not invalid JSON. It is empty data.

---

## Q38. What should happen with `[{}, {}]` JSON?

For:

```json
[
  {},
  {}
]
```

It is valid JSON and technically a list of dictionaries.

It has:

```text
Records: 2
Keys: none / empty key set
```

This is a weird but valid shape. A strong program should report that there are no keys/fields.

Possible output:

```text
Records: 2
Keys: none
Missing values: none
```

Or:

```text
Error: JSON records contain no keys.
```

But do not call it invalid JSON.

---

## Q39. What if a CSV row has extra values beyond the header?

CSV:

```csv
name,age
Ali,22,Toronto
```

There is an extra value beyond the header.

`csv.DictReader` may store extra values under the key `None` by default.

Possible parsed row:

```python
{"name": "Ali", "age": "22", None: ["Toronto"]}
```

This can affect inspection because extra data exists but has no column name. A stronger inspector should detect unexpected extra fields.

---

## Q40. What if a CSV row has fewer values than the header?

CSV:

```csv
name,age,city
Ali,22
```

The `city` value is missing.

`csv.DictReader` will likely produce:

```python
{"name": "Ali", "age": "22", "city": None}
```

So `city` should count as missing.

---

## Q41. Why is `"22"` ambiguous for type inference?

`"22"` is ambiguous because it is physically a string from the file, but semantically it may represent an integer.

CSV reads values as text first. Type inference guesses whether a string can be interpreted as a number.

So:

```text
stored form: string
possible meaning: integer
```

---

## Q42. Why should type inference ignore missing values?

Type inference should ignore missing values because missingness is not the semantic type of the column.

Example:

```text
22, 35, "", 41
```

The column is still mostly integer-like. The blank value should count as missing, not force the whole column to become string.

---

## Q43. What type is `22, 35, unknown, 41`?

For:

```text
22, 35, unknown, 41
```

A reasonable inference is:

```text
string
```

because `"unknown"` is a non-numeric value.

A more nuanced answer:

- If `"unknown"` is treated as a missing marker, infer `integer`.
- If `"unknown"` is treated as a real value, infer `string`.

Best answer: your inference depends on the rules you define for missing tokens.

---

## Q44. Why export `summary_report.txt`?

Exporting `summary_report.txt` is useful because:

```text
the result persists after the program ends
someone else can review it
it can be attached to reports
it supports automation
it creates an audit trail
```

In real workflows, terminal output alone is not enough.

---

## Q45. How is a list of dictionaries similar to a pandas DataFrame?

A list of dictionaries is similar to a pandas DataFrame because:

```python
[
  {"name": "Ali", "age": 22},
  {"name": "Sara", "age": 29}
]
```

resembles:

```text
rows = dictionaries
columns = keys
cell values = dictionary values
dataset = list of records
```

This is table-like.

---

## Q46. Where does the list-of-dictionaries analogy break?

The analogy breaks because pandas adds:

| Feature | List of dictionaries | DataFrame |
|---|---|---|
| index | no formal index | explicit index |
| column dtypes | mixed/implicit | column-level dtypes |
| vectorized operations | manual loops | column operations |
| missing values | inconsistent keys/None/"" | standardized missing handling |
| performance | slow for large numeric work | optimized operations |

A DataFrame is not merely a list of dictionaries. It is a labeled, column-oriented data structure.

---

## Q47. Why is a list of dictionaries not ideal for serious numerical work?

A list of dictionaries is not ideal for serious numerical work because:

```text
values are scattered across Python objects
operations usually require loops
types are not enforced per column
memory overhead is high
no native vectorized operations
```

NumPy arrays are structured and homogeneous, making element-wise operations and aggregations efficient.

The better answer is not only “faster.” It is:

```text
better structure → consistent type → vectorized computation
```

---

## Q48. What does this project teach that helps with NumPy?

This project helps with NumPy because it teaches:

```text
structured data
rows vs columns
missing values
data validation before computation
why lists become limiting
why consistent structure matters
```

NumPy will take the next step:

```text
structured numerical data → arrays → vectorized operations
```

---

## Q49. What does this project teach that helps with pandas?

This project helps with pandas because it teaches:

```text
records
keys as columns
rows as observations
missing values
CSV loading
JSON-like table data
summary reports
```

Pandas will automate and improve many things you manually built:

```text
read_csv()
DataFrame shape
columns
isna()
head()
dtypes
summary statistics
```

---

## Q50. Explain the full Data Inspector architecture

A strong architecture explanation:

1. **User runs command**

```bash
python data_inspector.py people.csv
```

2. **`main()` checks command-line input**

It checks whether the user provided a file path.

3. **`main()` checks file existence**

If the file does not exist, it prints:

```text
Error: File not found.
```

4. **File type is detected**

`detect_file_type(file_path)` checks the extension and returns:

```text
csv, json, txt, or None
```

5. **Correct inspector is called**

`main()` calls:

```python
inspect_csv(file_path)
inspect_json(file_path)
inspect_txt(file_path)
```

depending on the detected type.

6. **Inspector opens and parses**

- CSV uses `csv.DictReader`
- JSON uses `json.load`
- TXT uses `file.read`

7. **Structure is measured**

- CSV: rows, columns, column names
- JSON: records, all keys
- TXT: lines, words, characters

8. **Missing values are detected**

`is_missing(value)` checks:

```text
None
empty string
spaces only
```

CSV and JSON use this to count missing values.

9. **Preview is printed**

`print_preview(records, keys, limit=3)` prints the first records and shows `MISSING` for absent or blank values.

10. **Errors are handled**

Examples:

```text
missing file
empty file
invalid JSON
wrong JSON shape
unsupported file type
```

11. **Final report shows**

The report summarizes file type, structure, preview, and missing-value counts.

That proves the project is inspecting the data, not merely printing it.

---

# Scoring Guide

| Score | Meaning |
|---:|---|
| 45–50 correct | Phase 1 is solid. Move to Phase 2. |
| 35–44 correct | Mostly ready, but review weak areas. |
| 25–34 correct | You built it, but understanding is incomplete. |
| Under 25 | Rebuild the project without looking at code. |

Most important questions:

```text
Q1, Q5, Q7, Q11, Q16, Q19, Q20, Q25, Q33, Q45–Q50
```

If those are weak, do not move to Phase 2 yet.
