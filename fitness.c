#include<stdlib.h>
#include<string.h>
#include<stdio.h>
int cards = 2;
int stateSize = 6;
int *makeGamestate();
double fitness(int *);
double fitnessSub(int *, int *);
int main() {
	int *decklist = malloc(sizeof(int) * cards);
	decklist[0] = 3;
	decklist[1] = 4;
	printf("TEST");
	printf("Fitness: %lf\n", fitness(decklist));
}

double fitness(int *decklist) {
	int *gamestate = makeGamestate();
	for(int x = 0; x < cards; x++) {
		gamestate[2] += decklist[x];
	}
	return fitnessSub(decklist, gamestate);
}

double fitnessSub(int *decklist, int *gamestate) {
	double *playvalue = malloc(sizeof(double) * cards);
	if(gamestate[3] >= 4 && gamestate[4] >= 2) { //block for Tendrils of Agony
		int *tmpDecklist = malloc(sizeof(int) * cards);
		memcpy(tmpDecklist, decklist, sizeof(int) * cards);
		int *tmpGamestate = malloc(sizeof(int)*stateSize);
		memcpy(tmpGamestate,gamestate,sizeof(int)*stateSize);
		tmpGamestate[5]++;
		tmpGamestate[0] -= tmpGamestate[5]*2;
		if(tmpGamestate[0] <= 0) {
			playvalue[0] = 1;
		}
		else {
			tmpDecklist[0]--;
			tmpGamestate[1]--;
			tmpGamestate[2]--;
			tmpGamestate[3] -= 4;
			tmpGamestate[4] -= 2;
			if(tmpGamestate[4] > tmpGamestate[3]) {
				tmpGamestate[4] = tmpGamestate[3];
			}
			playvalue[0] = fitnessSub(tmpDecklist, tmpGamestate);
		}
		free(tmpDecklist);
		free(tmpGamestate);
	}
	{ //block for Lotus Petal
		int *tmpDecklist = malloc(sizeof(int) * cards);
		memcpy(tmpDecklist, decklist, sizeof(int) * cards);
		int *tmpGamestate = malloc(sizeof(int) * stateSize);
		memcpy(tmpGamestate, gamestate, sizeof(int) * stateSize);
		tmpGamestate[5]++;
		tmpGamestate[3]++;
		tmpGamestate[4]++;
		tmpGamestate[1]--;
		tmpGamestate[2]--;
		tmpDecklist[1]--;
		playvalue[1] = fitnessSub(tmpDecklist, tmpGamestate);
	}
}

int * makeGamestate() {
	int *ret = malloc(sizeof(int) * stateSize);
	ret[0] = 20; //opponent's life total
	ret[1] = 7; //cards in hand
	ret[2] = 0; //total cards in deck
	ret[3] = 0; //total mana
	ret[4] = 0; //mana of any color
	ret[5] = 0; //storm count
	return ret;
}
