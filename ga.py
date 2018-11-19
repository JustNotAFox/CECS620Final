import fitness
pop = []
for x in range(0,20):
	deck = fitness.generateDeck()
	print(str(deck))
	fit = fitness.fitness(deck,fitness.initGamestate())
	print("Deck",str(x+1),"fitness",str(fit))
	pop.append((deck,fit))
pop = sorted(pop,key=lambda x:x[1],reverse=1)
print(pop)
input()