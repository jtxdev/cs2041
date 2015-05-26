#!/usr/bin/python

import sys, re, collections
start=sys.argv[1]
finish=sys.argv[2]

distance=collections.defaultdict(dict)
unprocessed_towns=collections.defaultdict(dict)
for line in sys.stdin:
	m = re.match(r'(\w+)\s+([a-zA-z-]+)\s+(\d+)', line)
	if (m):
		distance[m.group(1)][m.group(2)] = int(m.group(3))
		distance[m.group(2)][m.group(1)] = int(m.group(3))
		unprocessed_towns[m.group(1)][m.group(2)] = int(m.group(3))
		unprocessed_towns[m.group(2)][m.group(1)] = int(m.group(3))

shortest_journey=collections.defaultdict(int)
route=collections.defaultdict(str)
current_town = start
while (current_town and current_town != finish):
	del unprocessed_towns[current_town]
	for town in unprocessed_towns:
		try: distance[current_town][town] > 0
		except KeyError: 
			continue
		d = shortest_journey[current_town] + distance[current_town][town]
		if (shortest_journey[town] != 0) and (shortest_journey[town] < d): continue
		shortest_journey[town] = d
		route[town] = route[current_town] + " " + current_town
	min_distance = 1e99
	current_town = ""
	for town in unprocessed_towns:
		if shortest_journey[town] == 0: continue
		if shortest_journey[town] > min_distance: continue
		min_distance = shortest_journey[town]
		current_town = town
if shortest_journey[finish] == 0:
    print "No route from $start to $finish.";
else:
    print "Shortest route is length = " + str(shortest_journey[finish]) + ":" + route[finish] + finish + "."