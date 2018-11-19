import fitness
import random
import threading
import queue
tocalc = queue.Queue()
popedit = queue.Queue(maxsize=1)
pop = []
popsize = 20
def worker():
	while 1:
		deck = tocalc.get()
		fit = fitness.fitness(deck,fitness.initGamestate())
		popedit.put(1)
		if len(pop) < popsize:
			pop.append((deck,fit))
		else:
			if pop[popsize-1][1]:
				pop[invertedWeightedPopRandom()] = (deck,fit)
			else:
				pop[popsize-1] = (deck,fit)
		pop.sort(key=lambda x:x[1],reverse=1)
		popedit.get()
		tocalc.task_done()

for i in range(0,8):
	threading.Thread(target=worker).start()
	
def weightedPopRandom():
	c = sum(i[1] for i in pop)
	t = random.random() * c
	i = 0
	c -= pop[i][1]
	while c > 0:
		i += 1
		if i == popsize:
			i = 0
		c -= pop[i][1]
	return pop[i]

def invertedWeightedPopRandom():
	print("stuck in here?")
	tmp = []
	for i in range(0,popsize):
		tmp.append(1/pop[i][1])
	c = sum(tmp)
	t = random.random() * c
	i = popsize - 1
	while c > 0:
		i -= 1
		if not i:
			i = popsize - 1
		c -= pop[i][1]
	return i
	
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

def mutate(init):
	ret = dict(init)
	t = random.choice(fitness.vals)
	while not ret[t]:
		t = random.choice(fitness.vals)
	ret[t] -= 1
	t = random.choice(fitness.vals)
	while ret[t] == fitness.cardmax:
		t = random.choice(fitness.vals)
	ret[t] += 1
	return ret
	
for x in range(0,20):
	deck = fitness.generateDeck()
	tocalc.put(deck)
tocalc.join()
print("Max:",pop[0])
print("Min:",pop[popsize-1])
print("Avg weight:",sum(i[1] for i in pop)/popsize)
for x in range(1,101):
	deck = breed(weightedPopRandom()[0],weightedPopRandom()[0])
	tocalc.put(deck)
	deck = mutate(random.choice(pop)[0])
	tocalc.put(deck)
	tocalc.join()
	print("After generation",x)
	print("Max:",pop[0])
	print("Min:",pop[popsize-1])
	print("Avg weight:",sum(i[1] for i in pop)/popsize)
	
input()
