import sys
import math
rl = lambda: sys.stdin.readline().strip()

cases = int(rl())
for case in xrange(cases):
	dudes = int(rl())
	peeps = [int(x) for x in rl().split()]
	#print 'dudes:', dudes, 'peeps:', peeps
	

	keepLooping = True
	penalty = 0
	totalMin = -1
	while keepLooping:
		#print 'for peeps:', peeps, 'with penalty', penalty
		bestWhenDoNothing = max(peeps)+penalty
		if totalMin == -1:
			totalMin = bestWhenDoNothing

		
		maxIndex = peeps.index(max(peeps))
		peeps.append(int(math.floor(peeps[maxIndex] / 2.0)))
		peeps[maxIndex] = int(math.ceil(peeps[maxIndex] / 2.0))


		penalty += 1
		bestWhenDoSomething = max(peeps)+penalty
		#print 'creating new peeps:', peeps, 'with penalty', penalty
		
		#print 'finding min of do nothing:', bestWhenDoNothing, 'and do something', bestWhenDoSomething
		answer = min([bestWhenDoSomething, bestWhenDoNothing])
		#print 'min of this round:', answer, 'vs best so far', totalMin
		if max(peeps) <= 3:
			keepLooping = False
		if answer < totalMin:
			totalMin = answer
		#print ''
		


	print 'Case #{0}: {1}'.format(case+1, totalMin)
	#print '\n**********************************'
		