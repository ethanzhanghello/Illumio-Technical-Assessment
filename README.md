# 🔒 Illumio Flow Log Tagger

A Python tool to parse AWS VPC flow logs, apply semantic tags based on port/protocol mappings, and output summary reports. Built as part of a technical assessment for Illumio.

---

## 📖 Table of Contents
- [Project Description](#project-description)
- [Technologies Used](#technologies-used)
- [Requirements](#requirements)
- [Installation Instructions](#installation-instructions)
- [Usage Instructions](#usage-instructions)
- [Input Format Assumptions](#input-format-assumptions)
- [Documentation](#documentation)
- [Visuals](#visuals)
- [Support](#support)
- [Project Roadmap](#project-roadmap)
- [Project Status](#project-status)
- [Contribution Guidelines](#contribution-guidelines)
- [Acknowledgments](#acknowledgments)
- [License](#license)

---

## 📝 Project Description
Illumio Flow Log Tagger reads AWS VPC flow logs and tags each line based on a custom port/protocol lookup table. It then outputs:
- A count of tag occurrences
- A count of port/protocol combinations

This allows users to quickly understand traffic patterns and tag distributions in a structured, readable way.

> ⚠️ While the example in this repository uses files located in the `sample_data/` folder, the program works with **any compatible `.txt` and `.csv` file**. Simply provide the correct file paths when executing the script.

---

## 🛠️ Technologies Used
- Python 3.x
- Standard libraries: `csv`, `sys`, `os`, `collections`

---

## ✅ Requirements
- Python 3.6 or higher
- Basic understanding of AWS VPC flow log structure (version 2)
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

## 📚 Documentation
The code is fully documented with inline docstrings. For assumptions and design notes, refer to the README.

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
