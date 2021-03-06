memdb
=====

a memory debugging &amp; visualization toolkit

Lots of programs have logically correct behavior, but suffer from issues relating to the memory system of the machines that cause unnecessary performance bottlenecks. For instance, badly ordered memory allocations can limit the data locality of a program, or variables that are shared poorly across threads will limit parallel scalability. This tool is designed to let a programmer diagnose and fix memory related performance issues.

Installation
=====
 * For HTML templates: `pip install jinja2`
 * For image generation: `pip install pillow`
 * Requires an internet connection to load D3.

Usage
=====
0. Make a nice cup of coffee
1. Collect your memory trace, using either Svetozar's Pin-tool, or Vividperf
 * https://github.com/fedorova/vividperf
2. If needed, convert your trace to a JSON trace format:
 * `./svetozar2json.py < trace.log > trace.json`
 * `./vivid2json.py < trace.log > trace.json`
3. Run the tool to identify the function you wish to profile: 
 * `./memdb.py -f trace.json`
4. Re-run the tool with the output directory and function specified: 
 * `./memdb.py -f test/pagerank.json -o outputdir -func functionsignature`
5. Open outputdir/index.html in a browser.
6. Sip coffee and browse the report.
7. Make thoughtful changes to your program.
8. Go to step 1.

Building Examples
====
Sometimes you just want to see how things are supposed to work:

```
	cd test/
	make clean all
```

Todo
====
 * Better looking HTML reports (Bootstrap?)
 * Support python setup.py?
 * Implement vivid2json.py
 * Visualize un-accessed allocations
 * Improve description of spatial locality d3 visualization
 * Improve pintools to capture/print file:line, function entrance


Trace Format
====
The trace format is in JSON, so is very flexible with regards to what attributes and trace events can be represented and used by an informed tool. Here is an example of each event in the most current outputs that can be used as reference to develop new analysis tools or implement format converters.

The only critical aspect is that each line contain an "event" key, so that all parsers can determine the event type of each line.
```
../dump_format.py < quadtree.json 
{"event": "function-begin", "name": "main"}
{"event": "allocation", "alloc-size": "80", "alloc-base": "0xcb3010", "type": "malloc", "alloc-tag": "1"}
{"event": "memory-access", "function": "_ZN14brandonpelfrey8QuadtreeC1ERK4Vec2S3_", "region-base": "0xcb3010", "pc": "0x40231b", "region-size": "80", "address": "0xcb3010", "type": "write", "region-tag": "1"}
{"event": "function-end", "name": "main"}

```