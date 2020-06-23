1. `export GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials`
2. Get the data from big-querydb: `python big-query.py`
3. Process the data to a proper CSV: `python process_blocks.py`
4. Run your analysis on the CSV `python analysis.py`
