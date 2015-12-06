import sys

rl = lambda: sys.stdin.readline().strip()

cases = int(rl())
for case in xrange(cases):
	crowd = rl().split()[1]
	runningTotal = 0
	invited = 0
	#shyLevel = 0
	for person in crowd:
		#print 'processing',person,'people at shyness level',shyLevel
		runningTotal += (int(person) - 1)
		if runningTotal < 0:
			#print 'inviting friend', runningTotal
			invited += 1
			runningTotal += 1
			#print 'invited friend', runningTotal
		#shyLevel+= 1
	print 'Case #{0}: {1}'.format(case+1, invited)