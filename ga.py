import fitness
pop = []
for x in range(0,20):
	deck = fitness2.generateDeck()
	fit = fitness2.fitness(deck,fitness2.initGamestate())
	print("Deck",str(x+1),"fitness",str(fit))
	pop.append((deck,fit))
pop = sorted(pop,key=lambda x:x[1],reverse=1)
print(pop)
input()