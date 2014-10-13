//outputs memory allocations and memory accesses that have alloc-location information
//useful for focusing on references to dynamically allocated memory
//
//rough benchmarks put the JS version at twice as fast as python (wow!)
//requires npm install split

//usage: node filter_allocs.js < file.gz > output.json

var zlib = require('zlib');
var split = require('split');
var fs = require('fs');

//var inp = fs.createReadStream('../test/wiredtiger/ldb-readrandom-24t.json.gz');
var inp = process.stdin;

inp.pipe(zlib.createGunzip()).pipe(split()).on('data', function(line){
	e = JSON.parse(line)
	//console.log(line)
	//console.log(obj)
	//console.log("-----")

	if(e['event'] == "allocation"){
		console.log(line);
	}
	if(e['event'] == 'memory-access'){
		if(e['alloc-location'] != "<unknown>"){
			console.log(line);
			process.exit(0);
		}
	}
})