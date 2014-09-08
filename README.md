memdb
=====

a memory debugging &amp; visualization toolkit

Installation
=====
 * For HTML templates: `pip install jinja2`
 * For image generation: `pip install pillow`

Usage
=====
0. Make a nice cup of coffee
1. Collect your memory trace, using either Svetozar's Pin-tool, or Vividperf
	Links: ...
2. If needed, convert your trace to a JSON trace format:
 * `./svetozar2json.py < trace.log > trace.json`
 * `./vivid2json.py < trace.log > trace.json`
3. Run the tool to identify the function you wish to profile: `./memdb.py -f trace.json`
4. Re-run the tool with the output directory and function specified: `./memdb.py -f test/pagerank.json -o outputdir -func functionsignature`
5. Open outputdir/index.html in a browser.
6. Sip coffee and browse the report.
7. Make thoughtful changes to your program.
8. Go to step 1.

Todo
====
 * Interactive visualizations based on D3
 * Support python setup.py?
 * Implement vivid2json.py