#include<iostream>
int cards = 2;
int stateSize = 6;
int *makeGamestate();
double fitness(int *);
double fitnessSub(int *, int *, int);
int main() {
	int *decklist = (int *)malloc(sizeof(int) * cards);
	decklist[0] = 1;
	decklist[1] = 7;
	std::cout << "Fitness: "<< fitness(decklist) << "\n";
	system("pause");
}

double fitness(int *decklist) {
	int *gamestate = makeGamestate();
	for (int x = 0; x < cards; x++) {
		gamestate[2] += decklist[x];
	}
	return fitnessSub(decklist, gamestate, 1);
}

double fitnessSub(int *decklist, int *gamestate, int d) {
	std::cout << "this deep" << d << "\n";
	if (!gamestate[1]) return 0;
	double *playvalue = (double *)malloc(sizeof(double) * cards);
	if (decklist[0] && gamestate[3] >= 4 && gamestate[4] >= 2) { //block for Tendrils of Agony
		int *tmpDecklist = (int *)malloc(sizeof(int) * cards);
		memcpy(tmpDecklist, decklist, sizeof(int) * cards);
		int *tmpGamestate = (int *)malloc(sizeof(int)*stateSize);
		memcpy(tmpGamestate, gamestate, sizeof(int)*stateSize);
		tmpGamestate[5]++;
		tmpGamestate[0] -= tmpGamestate[5] * 2;
		if (tmpGamestate[0] <= 0) {
			playvalue[0] = 1;
		}
		else {
			tmpDecklist[0]--;
			tmpGamestate[1]--;
			tmpGamestate[2]--;
			tmpGamestate[3] -= 4;
			tmpGamestate[4] -= 2;
			if (tmpGamestate[4] > tmpGamestate[3]) {
				tmpGamestate[4] = tmpGamestate[3];
			}
			playvalue[0] = fitnessSub(tmpDecklist, tmpGamestate, d+1);
		}
		free(tmpDecklist);
		free(tmpGamestate);
	}
	if(decklist[1]) { //block for Lotus Petal
		int *tmpDecklist = (int *)malloc(sizeof(int) * cards);
		memcpy(tmpDecklist, decklist, sizeof(int) * cards);
		int *tmpGamestate = (int *)malloc(sizeof(int) * stateSize);
		memcpy(tmpGamestate, gamestate, sizeof(int) * stateSize);
		tmpGamestate[5]++;
		tmpGamestate[3]++;
		tmpGamestate[4]++;
		tmpGamestate[1]--;
		tmpGamestate[2]--;
		tmpDecklist[1]--;
		playvalue[1] = fitnessSub(tmpDecklist, tmpGamestate, d+1);
	}
	int flag = 1;
	double ret = 0;
	double prob = 1;
	while (flag) {
		int max = 0;
		double maxW = 0;
		for (int x = 0; x < cards; x++) {
			if (playvalue[x] > maxW) {
				max = x;
				maxW = playvalue[x];
			}
		}
		if (maxW > 0) {
			playvalue[max] = 0;
			int n = gamestate[2] - decklist[max];
			int d = gamestate[2];
			double handChance = 1;
			for (int x = 0; x < gamestate[1] && handChance > 0; x++) {
				handChance *= (double)n / d;
				std::cout << "test value " << n << " and " << d << " gives " << handChance << "\n";
				n--;
				d--;
			}
			handChance = 1 - handChance;
			handChance *= prob;
			prob -= handChance;
			ret += handChance*maxW;
		}
		else {
			flag = 0;
		}
	}
	return ret;
}

int * makeGamestate() {
	int *ret = (int *)malloc(sizeof(int) * stateSize);
	ret[0] = 10; //opponent's life total
	ret[1] = 7; //cards in hand
	ret[2] = 0; //total cards in deck
	ret[3] = 0; //total mana
	ret[4] = 0; //mana of any color
	ret[5] = 0; //storm count
	return ret;
}
