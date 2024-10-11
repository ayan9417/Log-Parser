## Flow Log Processor

This project processes flow logs and tags them based on a lookup table of ports and protocols.

### Files

- **flow_logs.txt**: Contains the flow log entries.
- **lookup_table.csv**: Contains the port-protocol to tag mapping.
- **flow_log_processor.py**: The Python script to process the logs.
- **requirements.txt**: Lists the required Python packages (`pandas`).

### Instructions

1. **Install Requirements**:

   Run the following to install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Script**:

   Run the Python script to process the logs:

   ```bash
   python flow_log_processor.py
   ```

3. **Output**:

   The result will be saved in `output.txt` with the counts of tags and port/protocol combinations.