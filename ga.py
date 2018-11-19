import fitness
import random
import threading
import queue
tocalc = queue.Queue()
pop = []
def worker():
	while 1:
		deck = tocalc.get()
		fit = fitness.fitness(deck,fitness.initGamestate())
		print(deck)
		print(str(fit))
		pop.append((deck,fit))
		tocalc.task_done()

for i in range(0,8):
	threading.Thread(target=worker).start()
def breed(mom,dad):
	ret = {}
	for i in fitness.vals:
		if(bool(random.getrandbits(1))):
			ret[i] = mom[i]
		else:
			ret[i] = dad[i]
	c = sum(ret.values())
	while(c > fitness.decksize):
		t = random.choice(fitness.vals)
		if(ret[t]):
			ret[t] -= 1
			c -= 1
	while(c < fitness.decksize):
		t = random.choice(fitness.vals)
		if ret[t] < fitness.cardmax:
			ret[t] += 1
			c += 1
	return ret

for x in range(0,20):
	deck = fitness.generateDeck()
	tocalc.put(deck)
tocalc.join()
pop = sorted(pop,key=lambda x:x[1],reverse=1)
deck = breed(pop[0][0],pop[1][0])
fit = fitness.fitness(deck,fitness.initGamestate())
print(str(fit))
input()
