import random
import threading
vals = ["tendrils", "darkrit", "lotus", "morph", "probe", "wraith", "cabalrit", "nightwhisper", "riteflame", "star", "sphere", "wildcantor", "spiritguide", "visionsbeyond", "esg", "volc", "badlands", "usea", "signblood", "desprit", "pyrerit", "grape"]
decksize = 10
cardmax = 1
def generateDeck():
	ret = {}
	for i in vals:
		ret[i] = 0
	c = 0
	while c < decksize:
		t = random.choice(vals)
		if ret[t] < cardmax:
			ret[t] += 1
			c += 1
	return ret

def initGamestate():
	ret = {}
	ret["u"] = 0
	ret["b"] = 0
	ret["r"] = 0
	ret["g"] = 0
	ret["mana"] = 0
	ret["storm"] = 0
	ret["life"] = 10
	ret["health"] = 20
	ret["hand"] = 7
	ret["land"] = 1
	ret["grave"] = 0
	ret["riteflame"] = 0
	return ret

def lotus(deck, gamestate, inter):
	tmpDeck = dict(deck)
	tmpGamestate = dict(gamestate)
	tmpDeck["lotus"] -= 1
	tmpGamestate["storm"] += 1
	tmpGamestate["hand"] -= 1
	tmpGamestate["mana"] += 1
	tmpGamestate["u"] += 1
	tmpGamestate["b"] += 1
	tmpGamestate["r"] += 1
	tmpGamestate["grave"] += 1
	inter["lotus"] = fitness(tmpDeck,tmpGamestate)

def tendrils(deck,gamestate,inter):
	tmpGamestate = dict(gamestate)
	tmpGamestate["storm"] += 1
	tmpGamestate["life"] -= tmpGamestate["storm"] * 2
	if tmpGamestate["life"] <= 0:
		inter["tendrils"] = 1
	else:
		tmpDeck = dict(deck)
		tmpDeck["tendrils"] -= 1
		tmpGamestate["hand"] -= 1
		tmpGamestate["b"] -= 2
		tmpGamestate["mana"] -= 4
		tmpGamestate["health"] += 2 * tmpGamestate["storm"]
		if tmpGamestate["u"] > tmpGamestate["mana"]:
			tmpGamestate["u"] = tmpGamestate["mana"]
		if tmpGamestate["b"] > tmpGamestate["mana"]:
			tmpGamestate["b"] = tmpGamestate["mana"]
		if tmpGamestate["r"] > tmpGamestate["mana"]:
			tmpGamestate["r"] = tmpGamestate["mana"]
		if tmpGamestate["g"] > tmpGamestate["mana"]:
			tmpGamestate["g"] = tmpGamestate["mana"]
		tmpGamestate["grave"] += 1
		inter["tendrils"] = fitness(tmpDeck,tmpGamestate)

def darkrit(deck,gamestate,inter):
	tmpDeck = dict(deck)
	tmpGamestate = dict(gamestate)
	tmpDeck["darkrit"] -= 1
	tmpGamestate["storm"] += 1
	tmpGamestate["hand"] -= 1
	tmpGamestate["b"] += 2
	tmpGamestate["mana"] += 2
	tmpGamestate["grave"] += 1
	if tmpGamestate["u"] > tmpGamestate["mana"] - 3:
		tmpGamestate["u"] = tmpGamestate["mana"] - 3
	if tmpGamestate["r"] > tmpGamestate["mana"] - 3:
		tmpGamestate["r"] = tmpGamestate["mana"] - 3
	if tmpGamestate["g"] > tmpGamestate["mana"] - 3:
		tmpGamestate["g"] = tmpGamestate["mana"] - 3
	inter["darkrit"] = fitness(tmpDeck,tmpGamestate)

def riteflame(deck,gamestate,inter):
	tmpDeck = dict(deck)
	tmpGamestate = dict(gamestate)
	tmpDeck["riteflame"] -= 1
	tmpGamestate["riteflame"] += 1
	tmpGamestate["storm"] += 1
	tmpGamestate["hand"] -= 1
	tmpGamestate["r"] += tmpGamestate["riteflame"]
	tmpGamestate["mana"] += tmpGamestate["riteflame"]
	tmpGamestate["grave"] += 1
	if tmpGamestate["u"] > tmpGamestate["mana"] - (1 + tmpGamestate["riteflame"]):
		tmpGamestate["u"] = tmpGamestate["mana"] - (1 + tmpGamestate["riteflame"])
	if tmpGamestate["b"] > tmpGamestate["mana"] - (1 + tmpGamestate["riteflame"]):
		tmpGamestate["b"] = tmpGamestate["mana"] - (1 + tmpGamestate["riteflame"])
	if tmpGamestate["g"] > tmpGamestate["mana"] - (1 + tmpGamestate["riteflame"]):
		tmpGamestate["g"] = tmpGamestate["mana"] - (1 + tmpGamestate["riteflame"])
	inter["riteflame"] = fitness(tmpDeck,tmpGamestate)

def morph(deck,gamestate,inter):
	tmpDeck = dict(deck)
	tmpGamestate = dict(gamestate)
	tmpDeck["morph"] -= 1
	tmpGamestate["storm"] += 1
	if tmpGamestate["g"]:
		tmpGamestate["r"] += 2
		tmpGamestate["g"] -= 1
	else:
		tmpGamestate["r"] += 1
	tmpGamestate["b"] += 2
	tmpGamestate["u"] += 2
	tmpGamestate["grave"] += 1
	if tmpGamestate["u"] > tmpGamestate["mana"]:
		tmpGamestate["u"] = tmpGamestate["mana"]
	if tmpGamestate["b"] > tmpGamestate["mana"]:
		tmpGamestate["b"] = tmpGamestate["mana"]
	if tmpGamestate["r"] > tmpGamestate["mana"]:
		tmpGamestate["r"] = tmpGamestate["mana"]
	inter["morph"] = fitness(tmpDeck,tmpGamestate)

def wildcantor(deck,gamestate,inter):
	tmpDeck = dict(deck)
	tmpGamestate = dict(gamestate)
	tmpDeck["wildcantor"] -= 1
	tmpGamestate["storm"] += 1
	tmpGamestate["hand"] -= 1
	tmpGamestate["b"] += 1
	tmpGamestate["u"] += 1
	if tmpGamestate["g"]:
		tmpGamestate["g"] -= 1
		tmpGamestate["r"] += 1
	tmpGamestate["grave"] += 1
	if tmpGamestate["u"] > tmpGamestate["mana"]:
		tmpGamestate["u"] = tmpGamestate["mana"]
	if tmpGamestate["b"] > tmpGamestate["mana"]:
		tmpGamestate["b"] = tmpGamestate["mana"]
	inter["wildcantor"] = fitness(tmpDeck,tmpGamestate)

def star(deck,gamestate,inter):
	tmpDeck = dict(deck)
	tmpGamestate = dict(gamestate)
	tmpDeck["star"] -= 1
	tmpGamestate["storm"] += 1
	tmpGamestate["r"] += 1
	tmpGamestate["b"] += 1
	tmpGamestate["u"] += 1
	tmpGamestate["mana"] -= 1
	if tmpGamestate["u"] > tmpGamestate["mana"]:
		tmpGamestate["u"] = tmpGamestate["mana"]
	if tmpGamestate["b"] > tmpGamestate["mana"]:
		tmpGamestate["b"] = tmpGamestate["mana"]
	if tmpGamestate["r"] > tmpGamestate["mana"]:
		tmpGamestate["r"] = tmpGamestate["mana"]
	if tmpGamestate["g"] > tmpGamestate["mana"]:
		tmpGamestate["g"] = tmpGamestate["mana"]
	inter["star"] = fitness(tmpDeck,tmpGamestate)

def sphere(deck,gamestate,inter):
	tmpDeck = dict(deck)
	tmpGamestate = dict(gamestate)
	tmpDeck["sphere"] -= 1
	tmpGamestate["storm"] += 1
	tmpGamestate["r"] += 1
	tmpGamestate["b"] += 1
	tmpGamestate["u"] += 1
	tmpGamestate["mana"] -= 1
	tmpGamestate["grave"] += 1
	if tmpGamestate["u"] > tmpGamestate["mana"]:
		tmpGamestate["u"] = tmpGamestate["mana"]
	if tmpGamestate["b"] > tmpGamestate["mana"]:
		tmpGamestate["b"] = tmpGamestate["mana"]
	if tmpGamestate["r"] > tmpGamestate["mana"]:
		tmpGamestate["r"] = tmpGamestate["mana"]
	if tmpGamestate["g"] > tmpGamestate["mana"]:
		tmpGamestate["g"] = tmpGamestate["mana"]
	inter["sphere"] = fitness(tmpDeck,tmpGamestate)

def probe(deck,gamestate,inter):
	tmpDeck = dict(deck)
	tmpGamestate = dict(gamestate)
	tmpDeck["probe"] -= 1
	tmpGamestate["storm"] += 1
	tmpGamestate["grave"] += 1
	tmpGamestate["health"] -= 2
	inter["probe"] = fitness(tmpDeck,tmpGamestate)

def signblood(deck,gamestate,inter):
	tmpDeck = dict(deck)
	tmpGamestate = dict(gamestate)
	tmpDeck["signblood"] -= 1
	tmpGamestate["storm"] += 1
	tmpGamestate["grave"] += 1
	if tmpGamestate["life"] <= 2:
		tmpGamestate["life"] -= 2
		tmpGamestate["hand"] -= 1
	else:
		tmpGamestate["health"] -= 2
		tmpGamestate["hand"] += 1
	tmpGamestate["b"] -= 2
	tmpGamestate["mana"] -= 2
	if tmpGamestate["u"] > tmpGamestate["mana"]:
		tmpGamestate["u"] = tmpGamestate["mana"]
	if tmpGamestate["b"] > tmpGamestate["mana"]:
		tmpGamestate["b"] = tmpGamestate["mana"]
	if tmpGamestate["r"] > tmpGamestate["mana"]:
		tmpGamestate["r"] = tmpGamestate["mana"]
	if tmpGamestate["g"] > tmpGamestate["mana"]:
		tmpGamestate["g"] = tmpGamestate["mana"]
	inter["signblood"] = fitness(tmpDeck,tmpGamestate)

def visionsbeyond(deck,gamestate,inter):
	tmpDeck = dict(deck)
	tmpGamestate = dict(gamestate)
	tmpDeck["visionsbeyond"] -= 1
	tmpGamestate["storm"] += 1
	if tmpGamestate["grave"] >= 20:
		tmpGamestate["hand"] += 2
	tmpGamestate["grave"] += 1
	tmpGamestate["u"] -= 1
	tmpGamestate["mana"] -= 1
	if tmpGamestate["b"] > tmpGamestate["mana"]:
		tmpGamestate["b"] = tmpGamestate["mana"]
	if tmpGamestate["r"] > tmpGamestate["mana"]:
		tmpGamestate["r"] = tmpGamestate["mana"]
	if tmpGamestate["g"] > tmpGamestate["mana"]:
		tmpGamestate["g"] = tmpGamestate["mana"]
	inter["visionsbeyond"] = fitness(tmpDeck,tmpGamestate)

def nightwhisper(deck,gamestate,inter):
	tmpDeck = dict(deck)
	tmpGamestate = dict(gamestate)
	tmpDeck["nightwhisper"] -= 1
	tmpGamestate["storm"] += 1
	tmpGamestate["grave"] += 1
	tmpGamestate["hand"] += 1
	tmpGamestate["health"] -= 2
	tmpGamestate["b"] -= 1
	tmpGamestate["mana"] -= 2
	if tmpGamestate["u"] > tmpGamestate["mana"]:
		tmpGamestate["u"] = tmpGamestate["mana"]
	if tmpGamestate["b"] > tmpGamestate["mana"]:
		tmpGamestate["b"] = tmpGamestate["mana"]
	if tmpGamestate["r"] > tmpGamestate["mana"]:
		tmpGamestate["r"] = tmpGamestate["mana"]
	if tmpGamestate["g"] > tmpGamestate["mana"]:
		tmpGamestate["g"] = tmpGamestate["mana"]
	inter["nightwhisper"] = fitness(tmpDeck,tmpGamestate)

def wraith(deck,gamestate,inter):
	tmpDeck = dict(deck)
	tmpGamestate = dict(gamestate)
	tmpDeck["wraith"] -= 1
	tmpGamestate["grave"] += 1
	tmpGamestate["health"] -= 2
	inter["wraith"] = fitness(tmpDeck,tmpGamestate)

def spiritguide(deck,gamestate,inter):
	tmpDeck = dict(deck)
	tmpGamestate = dict(gamestate)
	tmpDeck["spiritguide"] -= 1
	tmpGamestate["hand"] -= 1
	tmpGamestate["r"] += 1
	tmpGamestate["mana"] += 1
	inter["spiritguide"] = fitness(tmpDeck,tmpGamestate)

def esg(deck,gamestate,inter):
	tmpDeck = dict(deck)
	tmpGamestate = dict(gamestate)
	tmpDeck["esg"] -= 1
	tmpGamestate["hand"] -= 1
	tmpGamestate["g"] += 1
	tmpGamestate["mana"] += 1
	inter["esg"] = fitness(tmpDeck,tmpGamestate)

def cabalrit(deck,gamestate,inter):
	tmpDeck = dict(deck)
	tmpGamestate = dict(gamestate)
	tmpDeck["cabalrit"] -= 1
	tmpGamestate["storm"] += 1
	tmpGamestate["b"] -= 1
	tmpGamestate["mana"] -= 2
	if tmpGamestate["u"] > tmpGamestate["mana"]:
		tmpGamestate["u"] = tmpGamestate["mana"]
	if tmpGamestate["b"] > tmpGamestate["mana"]:
		tmpGamestate["b"] = tmpGamestate["mana"]
	if tmpGamestate["r"] > tmpGamestate["mana"]:
		tmpGamestate["r"] = tmpGamestate["mana"]
	if tmpGamestate["g"] > tmpGamestate["mana"]:
		tmpGamestate["g"] = tmpGamestate["mana"]
	if tmpGamestate["grave"] >= 7:
		tmpGamestate["b"] += 5
		tmpGamestate["mana"] += 5
	else:
		tmpGamestate["b"] += 3
		tmpGamestate["mana"] += 3
	tmpGamestate["grave"] += 1
	tmpGamestate["hand"] -= 1
	inter["cabalrit"] = fitness(tmpDeck,tmpGamestate)

def volc(deck,gamestate,inter):
	tmpDeck = dict(deck)
	tmpGamestate = dict(gamestate)
	tmpDeck["volc"] -= 1
	tmpGamestate["hand"] -= 1
	tmpGamestate["r"] += 1
	tmpGamestate["u"] += 1
	tmpGamestate["mana"] += 1
	tmpGamestate["land"] -= 1
	inter["volc"] = fitness(tmpDeck,tmpGamestate)

def badlands(deck,gamestate,inter):
	tmpDeck = dict(deck)
	tmpGamestate = dict(gamestate)
	tmpDeck["badlands"] -= 1
	tmpGamestate["hand"] -= 1
	tmpGamestate["r"] += 1
	tmpGamestate["b"] += 1
	tmpGamestate["mana"] += 1
	tmpGamestate["land"] -= 1
	inter["badlands"] = fitness(tmpDeck,tmpGamestate)

def usea(deck,gamestate,inter):
	tmpDeck = dict(deck)
	tmpGamestate = dict(gamestate)
	tmpDeck["usea"] -= 1
	tmpGamestate["hand"] -= 1
	tmpGamestate["b"] += 1
	tmpGamestate["u"] += 1
	tmpGamestate["mana"] += 1
	tmpGamestate["land"] -= 1
	inter["usea"] = fitness(tmpDeck,tmpGamestate)

def desprit(deck,gamestate,inter):
	tmpDeck = dict(deck)
	tmpGamestate = dict(gamestate)
	tmpDeck["desprit"] -= 1
	tmpGamestate["hand"] -= 1
	tmpGamestate["storm"] += 1
	tmpGamestate["r"] += 2
	tmpGamestate["mana"] += 1
	tmpGamestate["grave"] += 1
	if tmpGamestate["r"] > tmpGamestate["mana"]:
		tmpGamestate["r"] = tmpGamestate["mana"]
	if tmpGamestate["b"] > tmpGamestate["mana"] - 3:
		tmpGamestate["b"] = tmpGamestate["mana"] - 3
	if tmpGamestate["u"] > tmpGamestate["mana"] - 3:
		tmpGamestate["u"] = tmpGamestate["mana"] - 3
	if tmpGamestate["g"] > tmpGamestate["mana"] - 3:
		tmpGamestate["g"] = tmpGamestate["mana"] - 3
	inter["desprit"] = fitness(tmpDeck,tmpGamestate)
	
def pyrerit(deck,gamestate,inter):
	tmpDeck = dict(deck)
	tmpGamestate = dict(gamestate)
	tmpDeck["pyrerit"] -= 1
	tmpGamestate["hand"] -= 1
	tmpGamestate["storm"] += 1
	tmpGamestate["r"] += 2
	tmpGamestate["mana"] += 1
	tmpGamestate["grave"] += 1
	if tmpGamestate["r"] > tmpGamestate["mana"]:
		tmpGamestate["r"] = tmpGamestate["mana"]
	if tmpGamestate["b"] > tmpGamestate["mana"] - 3:
		tmpGamestate["b"] = tmpGamestate["mana"] - 3
	if tmpGamestate["u"] > tmpGamestate["mana"] - 3:
		tmpGamestate["u"] = tmpGamestate["mana"] - 3
	if tmpGamestate["g"] > tmpGamestate["mana"] - 3:
		tmpGamestate["g"] = tmpGamestate["mana"] - 3
	inter["pyrerit"] = fitness(tmpDeck,tmpGamestate)

def grape(deck,gamestate,inter):
	tmpGamestate = dict(gamestate)
	tmpGamestate["storm"] += 1
	tmpGamestate["life"] -= tmpGamestate["storm"]
	if(tmpGamestate["life"] > 0):
		tmpDeck = dict(deck)
		tmpDeck["grape"] -= 1
		tmpGamestate["r"] -= 1
		tmpGamestate["mana"] -= 2
		if tmpGamestate["r"] > tmpGamestate["mana"]:
			tmpGamestate["r"] = tmpGamestate["mana"]
		if tmpGamestate["u"] > tmpGamestate["mana"]:
			tmpGamestate["u"] = tmpGamestate["mana"]
		if tmpGamestate["b"] > tmpGamestate["mana"]:
			tmpGamestate["b"] = tmpGamestate["mana"]
		if tmpGamestate["g"] > tmpGamestate["mana"]:
			tmpGamestate["g"] = tmpGamestate["mana"]
		tmpGamestate["hand"] -= 1
		tmpGamestate["grave"] += 1
		inter["grape"] = fitness(tmpDeck,tmpGamestate)
	else:
		inter["grape"] = 1
	
def fitness(deck, gamestate):
	threads = []
	inter = {}
	c = sum(deck.values())
	if gamestate["hand"] == 0 or gamestate["hand"] > c:
		return 0

	if deck["badlands"] and gamestate["land"]:
		badlands(deck,gamestate,inter)

	if deck["usea"] and gamestate["land"]:
		usea(deck,gamestate,inter)

	if deck["volc"] and gamestate["land"]:
		volc(deck,gamestate,inter)

	if deck["lotus"]:
		#threads.append(threading.Thread(target=lotus,args=(deck,gamestate,inter)))
		lotus(deck,gamestate,inter)

	if deck["tendrils"] and gamestate["b"] >= 2 and gamestate["mana"] >= 4:
		#threads.append(threading.Thread(target=tendrils,args=(deck,gamestate,inter)))
		tendrils(deck,gamestate,inter)

	if deck["darkrit"] and gamestate["b"]:
		#threads.append(threading.Thread(target=darkrit,args=(deck,gamestate,inter)))
		darkrit(deck,gamestate,inter)

	if deck["riteflame"] and gamestate["r"]:
		#threads.append(threading.Thread(target=riteflame,args=(deck,gamestate,inter)))
		riteflame(deck,gamestate,inter)

	if deck["morph"] and (gamestate["r"] or gamestate["g"]) and gamestate["mana"] >= 2:
		#threads.append(threading.Thread(target=morph,args=(deck,gamestate,inter)))
		morph(deck,gamestate,inter)

	if deck["wildcantor"] and (gamestate["r"] or gamestate["g"]):
		#threads.append(threading.Thread(target=wildcantor,args=(deck,gamestate,inter)))
		wildcantor(deck,gamestate,inter)


	if deck["star"] and gamestate["mana"] >= 2:
		#threads.append(threading.Thread(target=star,args=(deck,gamestate,inter)))
		star(deck,gamestate,inter)

	if deck["sphere"] and gamestate["mana"] >= 2:
		#threads.append(threading.Thread(target=sphere,args=(deck,gamestate,inter)))
		sphere(deck,gamestate,inter)

	if deck["probe"] and gamestate["health"] >= 3:
		#threads.append(threading.Thread(target=probe,args=(deck,gamestate,inter)))
		probe(deck,gamestate,inter)

	if deck["visionsbeyond"] and gamestate["u"]:
		#threads.append(threading.Thread(target=visionsbeyond,args=(deck,gamestate,inter)))
		visionsbeyond(deck,gamestate,inter)

	if deck["nightwhisper"] and gamestate["b"] and gamestate["mana"] >= 2 and gamestate["health"] >= 3:
		#threads.append(threading.Thread(target=nightwhisper,args=(deck,gamestate,inter)))
		nightwhisper(deck,gamestate,inter)

	if deck["wraith"] and gamestate["health"] >= 3:
		#threads.append(threading.Thread(target=wraith,args=(deck,gamestate,inter)))
		wraith(deck,gamestate,inter)

	if deck["spiritguide"]:
		#threads.append(threading.Thread(target=spiritguide,args=(deck,gamestate,inter)))
		spiritguide(deck,gamestate,inter)

	if deck["cabalrit"] and gamestate["b"] and gamestate["mana"] >= 2:
		#threads.append(threading.Thread(target=cabalrit,args=(deck,gamestate,inter)))
		cabalrit(deck,gamestate,inter)

	if deck["esg"]:
		#threads.append(threading.Thread(target=esg,args=(deck,gamestate,inter)))
		esg(deck,gamestate,inter)
		
	if deck["desprit"] and gamestate["r"] and gamestate["mana"] >= 2:
		#threads.append(threading.Thread(target=desprit,args=(deck,gamestate,inter)))
		desprit(deck,gamestate,inter)
		
	if deck["pyrerit"] and gamestate["r"] and gamestate["mana"] >= 2:
		#threads.append(threading.Thread(target=pyrerit,args=(deck,gamestate,inter)))
		pyrerit(deck,gamestate,inter)
		
	if deck["grape"] and gamestate["r"] and gamestate["mana"] >= 2:
		#threads.append(threading.Thread(target=grape,args=(deck,gamestate,inter)))
		grape(deck,gamestate,inter)

	if deck["signblood"] and gamestate["b"] >= 2 and (gamestate["health"] >= 3 or gamestate["life"] <= 2):
		signblood(deck,gamestate,inter)

	for i in threads:
		i.start()
	for i in threads:
		i.join()
	ret = 0
	noplay = 1
	for i in sorted(inter.items(),key=lambda x: x[1], reverse=1):
		count = deck[i[0]]
		tmp = 1
		if gamestate["hand"] + count <= c:
			for x in range(0,gamestate["hand"]):
				tmp *= (c - count - x)
				tmp /= (c - x)
			tmp = 1 - tmp
		tmp *= noplay
		noplay -= tmp
		tmp *= i[1]
		ret += tmp
	return ret
