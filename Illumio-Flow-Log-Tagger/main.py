import csv
from collections import Counter
import sys
import os

# Protocol mapping
PROTOCOL_MAP = {
    "6": "tcp",
    "17": "udp",
    "1": "icmp"
}

def load_lookup_table(filepath):
    """
    Loads the port/protocol-to-tag mappings from a CSV file.

    Args:
        filepath (str): Path to the CSV lookup table file.

    Returns:
        dict: Dictionary mapping (dstport, protocol) to tag.
    """
    lookup = {}
    try:
        with open(filepath, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                port = row['dstport'].strip()
                protocol = row['protocol'].strip().lower()
                tag = row['tag'].strip()
                lookup[(port, protocol)] = tag
    except FileNotFoundError:
        print(f"Lookup file not found: {filepath}")
        sys.exit(1)
    except KeyError as e:
        print(f"Missing expected column in lookup file: {e}")
        sys.exit(1)
    return lookup

def parse_flow_log(filepath):
    """
    Parses the flow log file (AWS VPC flow logs v2) and yields destination port and protocol.

    Args:
        filepath (str): Path to the flow log text file.

    Yields:
        tuple: (dstport, protocol) for each valid flow log entry.
    """
    try:
        with open(filepath, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) < 8:
                    continue
                dstport = parts[6].strip()
                protocol_num = parts[7].strip()
                protocol = PROTOCOL_MAP.get(protocol_num, protocol_num).lower()
                yield dstport, protocol
    except FileNotFoundError:
        print(f"Flow log file not found: {filepath}")
        sys.exit(1)

def tag_flows(flow_entries, lookup_table):
    """
    Tags each flow entry using the lookup table and counts tag and port/protocol frequencies.

    Args:
        flow_entries (iterable): Iterable of (dstport, protocol) tuples.
        lookup_table (dict): Mapping of (dstport, protocol) to tag.

    Returns:
        tuple: (tag_counter, port_proto_counter), each a Counter object.
    """
    tag_counter = Counter()
    port_proto_counter = Counter()

    for dstport, protocol in flow_entries:
        key = (dstport, protocol.lower())
        tag = lookup_table.get(key, 'Untagged')

        tag_counter[tag] += 1
        port_proto_counter[(dstport, protocol)] += 1

    return tag_counter, port_proto_counter

def write_tag_counts(tag_counter, output_path):
    """
    Writes the tag counts to a CSV file.

    Args:
        tag_counter (Counter): Counter of tag frequencies.
        output_path (str): File path for the output CSV.
    """
    with open(output_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Tag", "Count"])
        for tag, count in sorted(tag_counter.items()):
            writer.writerow([tag, count])

def write_port_proto_counts(counter, output_path):
    """
    Writes the port/protocol combination counts to a CSV file.

    Args:
        counter (Counter): Counter of (port, protocol) combinations.
        output_path (str): File path for the output CSV.
    """
    with open(output_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Port", "Protocol", "Count"])
        for (port, protocol), count in sorted(counter.items()):
            writer.writerow([port, protocol, count])

def main():
    """
    Creates an output directory and processes AWS VPC flow log data to tag network traffic
    based on port/protocol combinations defined in a lookup table.
    """
    if len(sys.argv) != 3:
        print("Usage: python main.py <flow_log.txt> <lookup_table.csv>")
        return

    flow_log_path = sys.argv[1]
    lookup_table_path = sys.argv[2]

    if not os.path.exists("output"):
        os.makedirs("output")

    lookup_table = load_lookup_table(lookup_table_path)
    flow_entries = parse_flow_log(flow_log_path)
    tag_counter, port_proto_counter = tag_flows(flow_entries, lookup_table)

    write_tag_counts(tag_counter, 'output/tag_counts.csv')
    write_port_proto_counts(port_proto_counter, 'output/port_protocol_counts.csv')

    print("Processing complete. Output written to 'output/' directory.")

if __name__ == '__main__':
    main()