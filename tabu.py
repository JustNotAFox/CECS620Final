import fitness
import threading
import queue
tocalc = queue.Queue()
edit = queue.Queue(maxsize=1)
optima = []
tabu = {}
current = ({},0)
def worker():
	global current
	while 1:
		deck = tocalc.get()
		fit = fitness.fitness(deck,fitness.initGamestate())
		edit.put(1)
		if fit > current[1]:
			current = (deck,fit)
		edit.get()
		tocalc.task_done()

for i in range(0,8):
	threading.Thread(target=worker).start()
def tabuRound():
	c = 0
	while current[1] == 0 and c < 100:
		deck = fitness.generateDeck()
		tabu[str(i[1] for i in sorted(deck.items(),key=lambda x:x[0]))] = 1
		tocalc.put(deck)
		tocalc.join()
		c += 1
	if c == 100 and current[1] == 0:
		print("gg, skipped")
		return
	flag = 1
	while flag:
		for i in fitness.vals:
			if deck[i]:
				for v in fitness.vals:
					if deck[v] < fitness.cardmax:
						deck[i] -= 1
						deck[v] += 1
						if not tabu[str(j[1] for j in sorted(deck.items(),key=lambda x:x[0]))]:
							tabu[str(j[1] for j in sorted(deck.items(),key=lambda x:x[0]))] = 1
							tocalc.put(dict(deck))
						deck[i] += 1
						deck[v] -= 1
		tocalc.join()
		if current[0] == deck:
			flag = 0
		else:
			deck = current[0]
for i in range(0,100):
	print(i)
	current = ({},0)
	tabuRound()
	optima.append(current)
print(str(max(optima,key=lambda x:x[1])))
input()