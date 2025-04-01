# 🔒 Illumio Flow Log Tagger

A Python tool to parse AWS VPC flow logs, apply tags based on port and protocol mappings, and output summary reports.

---

## 📖 Table of Contents
- [Project Description](#project-description)
- [Technologies Used](#technologies-used)
- [Requirements](#requirements)
- [Installation Instructions](#installation-instructions)
- [Usage Instructions](#usage-instructions)
- [Testing & Validation](#tesing-&-validation)
- [Input Format Assumptions](#input-format-assumptions)
- [Documentation](#documentation)
- [Visuals](#visuals)
- [Support](#support)
- [Acknowledgments](#acknowledgments)

---

## 📝 Project Description
Illumio Flow Log Tagger reads AWS VPC flow logs and tags each line based on a port/protocol lookup table. It then outputs:
- A count of each tag occurrence
- A count of unique port/protocol combinations

> ⚠️ Although the example in this repository uses files located in the `sample_data/` folder, the program works with **any compatible `.txt` and `.csv` file**. You just have to provide the correct file paths when executing the script.

---

## 🛠️ Technologies Used
- Python 3.x
- Standard libraries: `csv`, `sys`, `os`, `collections`

---

## ✅ Requirements
- Python 3.6 or higher
- ASCII or UTF-8 encoded input files

---

## ⚙️ Installation Instructions
Clone the repo and navigate to the folder:

```bash
git clone https://github.com/YOUR_USERNAME/illumio-flow-log-tagger.git
cd illumio-flow-log-tagger
```

No installation of extra packages is required.

---

## 🚀 Usage Instructions
Run the script using:

```bash
python main.py path/to/your_flow_logs.txt path/to/your_tag_lookup.csv
```

To test with the provided sample data:

```bash
python main.py sample_data/sample_logs.txt sample_data/tag_lookup.csv
```

> The `output/` folder will be created automatically if it doesn’t exist. Results are written to:
- `output/tag_counts.csv`
- `output/port_protocol_counts.csv`

---

## ⚠️ Input Format Assumptions
- Only supports AWS VPC **default flow log format, version 2**
- Flow log must be a space-separated `.txt` file
- Tag lookup table must be a `.csv` file with headers: `dstport,protocol,tag`
- Protocols are matched using numeric codes:
  - `6` → tcp
  - `17` → udp
  - `1` → icmp
- Matching is **case-insensitive**
- Entries not matched in the lookup table will be tagged as `Untagged`

---

## ✅ Testing & Validation

Test cases:

### 1. Reordered/Extra Fields
Tested log entries with additional or noisy fields at the end. ✅ Verified the parser correctly extracted the `dstport` and `protocol` regardless of extra tokens.

### 2. Malformed Input Lines
Tested flow logs with missing required fields to check for safe failure. ✅ Skipped incomplete or malformed lines without crashing.

### 3. Case-Insensitive Matching
Lookup table used mixed-case protocols (e.g., `TCP`, `Udp`). ✅ The program normalized casing and matched protocols correctly.

### 4. Tag Conflict Handling
The same port was used with both `tcp` and `udp` protocols mapped to different tags. ✅ Tag assignment was accurate based on both port and protocol.

### 5. Empty Input Files
Tested with empty flow log and tag mapping files. ✅ Output files were generated correctly

---

## 🖼️ Visuals
**Sample Output (`tag_counts.csv`)**:
```
Tag,Count
Untagged,8
email,3
sv_P1,2
sv_P2,1
```

**Sample Output (`port_protocol_counts.csv`)**:
```
Port,Protocol,Count
443,tcp,1
25,tcp,2
110,tcp,1
... (truncated)
```

---

## 🆘 Support
For questions, contact: [ezhang06@berkeley.edu](mailto:ezhang06@berkeley.edu)

---

## 🙏 Acknowledgments
- Special thanks to Illumio for this challenge.

---
