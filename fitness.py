import random
vals = ["tendrils", "darkrit", "lotus", "morph", "probe", "wraith", "cabalrit", "nightwhisper", "riteflame", "star"]
def generateDeck():
	ret = {}
	for i in vals:
		ret[i] = 0
	c = 0
	while c < 15:
		t = random.choice(vals)
		if ret[random.choice(vals)] < 4:
			ret[random.choice(vals)] += 1
			c += 1
	return ret

def initGamestate():
	ret = {}
	ret["u"] = 0
	ret["b"] = 0
	ret["r"] = 0
	ret["mana"] = 0
	ret["storm"] = 0
	ret["life"] = 20
	ret["hand"] = 7
	ret["land"] = 1
	ret["grave"] = 0
	ret["riteflame"] = 0
	return ret

def fitness(deck, gamestate):
	inter = {}
	c = sum(deck.values())
	if gamestate["hand"] == 0 or gamestate["hand"] > c:
		return 0

	if deck["lotus"]:
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

	if deck["tendrils"] and gamestate["b"] >= 2 and gamestate["mana"] >= 4:
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
			if tmpGamestate["u"] > tmpGamestate["mana"]:
				tmpGamestate["u"] = tmpGamestate["mana"]
			if tmpGamestate["b"] > tmpGamestate["mana"]:
				tmpGamestate["b"] = tmpGamestate["mana"]
			if tmpGamestate["r"] > tmpGamestate["mana"]:
				tmpGamestate["r"] = tmpGamestate["mana"]
			tmpGamestate["grave"] += 1
			inter["tendrils"] = fitness(tmpDeck,tmpGamestate)

	if deck["darkrit"] and gamestate["b"]:
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
		inter["darkrit"] = fitness(tmpDeck,tmpGamestate)

	if deck["riteflame"] and gamestate["r"]:
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
		inter["riteflame"] = fitness(tmpDeck,tmpGamestate)

	if deck["morph"] and gamestate["r"] and gamestate["mana"] >= 2:
		tmpDeck = dict(deck)
		tmpGamestate = dict(gamestate)
		tmpDeck["morph"] -= 1
		tmpGamestate["storm"] += 1
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

	if deck["star"] and gamestate["mana"] >= 2:
		tmpDeck = dict(deck)
		tmpGamestate = dict(gamestate)
		tmpDeck["star"] -= 1
		tmpGamestate["storm"] += 1
		tmpGamestate["r"] += 1
		tmpGamestate["b"] += 1
		tmpGamestate["u"] += 1
		tmpGamestate["grave"] += 1
		if tmpGamestate["u"] > tmpGamestate["mana"]:
			tmpGamestate["u"] = tmpGamestate["mana"]
		if tmpGamestate["b"] > tmpGamestate["mana"]:
			tmpGamestate["b"] = tmpGamestate["mana"]
		if tmpGamestate["r"] > tmpGamestate["mana"]:
			tmpGamestate["r"] = tmpGamestate["mana"]
		inter["star"] = fitness(tmpDeck,tmpGamestate)

	if deck["probe"]:
		tmpDeck = dict(deck)
		tmpGamestate = dict(gamestate)
		tmpDeck["probe"] -= 1
		tmpGamestate["storm"] += 1
		tmpGamestate["grave"] += 1
		inter["probe"] = fitness(tmpDeck,tmpGamestate)

	if deck["nightwhisper"] and gamestate["b"] and gamestate["mana"] >= 2:
		tmpDeck = dict(deck)
		tmpGamestate = dict(gamestate)
		tmpDeck["nightwhisper"] -= 1
		tmpGamestate["storm"] += 1
		tmpGamestate["grave"] += 1
		tmpGamestate["hand"] += 1
		tmpGamestate["life"] -= 2
		inter["nightwhisper"] = fitness(tmpDeck,tmpGamestate)

	if deck["wraith"]:
		tmpDeck = dict(deck)
		tmpGamestate = dict(gamestate)
		tmpDeck["wraith"] -= 1
		tmpGamestate["grave"] += 1
		inter["wraith"] = fitness(tmpDeck,tmpGamestate)

	if deck["cabalrit"] and gamestate["b"] and gamestate["mana"] >= 2:
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
		if tmpGamestate["grave"] >= 7:
			tmpGamestate["b"] += 5
			tmpGamestate["mana"] += 5
		else:
			tmpGamestate["b"] += 3
			tmpGamestate["mana"] += 3
		tmpGamestate["grave"] += 1
		tmpGamestate["hand"] -= 1
		inter["cabalrit"] = fitness(tmpDeck,tmpGamestate)

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
