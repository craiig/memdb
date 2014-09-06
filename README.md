memdb
=====

a memory debugging &amp; visualization toolkit

Installation
=====
To be determined

Usage
=====
0. Make a nice cup of coffee
1. Collect your memory trace, using either Svetozar's Pin-tool, or Sasha's
	Links: ...
3. If needed, convert your trace to a JSON trace format:
 * `./svetozar2json.py < trace.log > trace.json`
 * `./vivid2json.py < trace.log > trace.json`
2. `./generate_report.py -f trace.json -o output_directory`
3. Open output_directory/index.html in a browser.
4. Sip coffee and analyze the report.
5. Make changes to your program.
6. Go to step 0.
