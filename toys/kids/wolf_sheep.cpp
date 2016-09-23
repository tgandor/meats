#include <iostream>
#include <vector>
#include <algorithm>
#include <map>

using namespace std;

/* chessboard sizes, should be even */
#ifndef SIZE
const int CB_W = 8;
#else
const int CB_W = SIZE;
#endif
const int CB_H = CB_W;

// position bit field size
const int PSHIFT = 5;

long long position_counter;
int wolf_trapped;
int sheep_blocked;

int VERBOSE_LEVEL = 0;

struct Move
{
	int dr, dc;
};

Move MovesWolf[] = {
	{1, -1},
	{1, 1},
	{-1, -1},
	{-1, 1},
};

Move MovesSheep[] = {
	{-1, -1},
	{-1, 1},
};

struct Pos
{
	int r, c;
	Pos shift(Move d) { return {r + d.dr, c + d.dc}; }
};

enum GameResult
{
	WOLF_WINS,
	SHEEP_WIN
};

enum FieldState
{
	EMPTY,
	SHEEP,
	WOLF
} board[CB_H][CB_W];

Pos pWolf;
Pos pSheep[CB_W/2];

int total_hits, miss_cache;

// .#.#.#
// #.#.#.
// .#.#.#
// etc.
void init(int wolfpos = 0)
{
	for (int i = 0; i < CB_W; i += 2)
	{
		board[CB_H-1][i] = SHEEP;
		pSheep[i/2] = {CB_H-1, i};
	}
	for (int j = 0; j < CB_H - 1; ++j)
	{
		for (int i = 0; i < CB_W; ++i)
		{
			board[j][i] = EMPTY;
		}
	}
	board[0][1 + 2 * wolfpos] = WOLF;
	pWolf = {0, 1 + 2 * wolfpos};
}

void print_board()
{
	for (int j = 0; j < CB_H; ++j)
	{
		for (int i = 0; i < CB_W; ++i)
		{
			switch (board[j][i])
			{
				case WOLF:
					cout << 'W';
					break;
				case SHEEP:
					cout << 'S';
					break;
				default:
					cout << ((i+j) % 2 ? '#' : '.');
			}
		}
		cout << endl;
	}
}

int hash_position()
{
	int res = pWolf.r * (CB_W/2) + pWolf.c/2;
	int positions[CB_W/2];
	transform(begin(pSheep), end(pSheep), positions, [](Pos x) {
		return x.r * (CB_W/2) + x.c/2;
	});
	sort(begin(positions), end(positions));
	for (int x : positions)
	{
		res = (res << PSHIFT) + x;
	}
	return res;
}

map<int, GameResult> cache_wolf, cache_sheep;

inline void board_set(Pos p, FieldState fs)
{
	board[p.r][p.c] = fs;
}

inline bool legal(Pos p)
{
	return p.r >= 0 && p.r < CB_H && p.c >= 0 && p.c < CB_W && board[p.r][p.c] == EMPTY;
}

GameResult sheep(int);

GameResult wolf(int moves = 0)
{
	++total_hits;
	int h = hash_position();
	auto cache_it = cache_wolf.find(h);
	if (cache_it != cache_wolf.end())
	{
		return cache_it->second;
	}
	++miss_cache;
	if (VERBOSE_LEVEL >= 1)
		cout << "  Evaluating wolf position " << h  << " after " << moves << " moves:" << endl;
	if (VERBOSE_LEVEL >= 2)
		print_board();
	
#ifdef VERBOSE

#endif
	Pos origPos = pWolf;
	bool cantMove = true;
	for (auto& d : MovesWolf)
	{
		Pos newPos = origPos.shift(d);
		if (legal(newPos))
		{
			cantMove = false;
			board_set(origPos, EMPTY);
			board_set(newPos, WOLF);
			pWolf = newPos;
			auto res = sheep(moves + 1);
			pWolf = origPos;
			board_set(newPos, EMPTY);
			board_set(origPos, WOLF);
			if (res == WOLF_WINS)
			{
				return cache_wolf[h] = res;
			}
		}
	}
	
	if (cantMove && ++wolf_trapped % 1000000 == 0)
	{
		cout << "Wolf trapped " << wolf_trapped << endl;
		print_board();
	}
	return cache_wolf[h] = SHEEP_WIN;
}

GameResult sheep(int moves = 0)
{
	++total_hits;
	int h = hash_position();
	auto cache_it = cache_sheep.find(h);
	if (cache_it != cache_sheep.end())
	{
		return cache_it->second;
	}
	++miss_cache;
	if (VERBOSE_LEVEL >= 1)
		cout << "  Evaluating sheep position " << h << " after " << moves << " moves:" << endl;
	if (VERBOSE_LEVEL >= 2)
		print_board();

	if (pWolf.r == CB_H - 1
		|| max_element(begin(pSheep), end(pSheep),
					   [](Pos a, Pos b){ return a.r < b.r; })->r <= pWolf.r)
	{
		return cache_sheep[h] = WOLF_WINS;
	}
	
	for (auto& pOneSheep : pSheep)
	{
		// cout << "Moving sheep at " << pOneSheep.r << ", " << pOneSheep.c << endl;
		Pos origPos = pOneSheep;
		for (auto& d : MovesSheep)
		{
			Pos newPos = origPos.shift(d);
			if (legal(newPos))
			{
				board_set(origPos, EMPTY);
				board_set(newPos, SHEEP);
				pOneSheep = newPos;
				auto res = wolf(moves + 1);
				pOneSheep = origPos;
				board_set(newPos, EMPTY);
				board_set(origPos, SHEEP);
				if (res == SHEEP_WIN)
				{
					return cache_sheep[h] = res;
				}
			}
			// else { cout << "Pos " << newPos.r << ", " << newPos.c << " illegal for sheep." << endl; }
		}
	}
	
	return cache_sheep[h] = WOLF_WINS;
}

int main()
{
	init();
	if (wolf() == WOLF_WINS)
		cout << "Wolf wins if he starts" << endl;
	else
		cout << "Wolf loses even if he starts" << endl;

	if (sheep() == SHEEP_WIN)
		cout << "Sheep wins if she starts" << endl;
	else
		cout << "Sheep loses even if she starts" << endl;

	cout << "Total calls: " << total_hits << ", cache misses: " << miss_cache << endl;
	return 0;
}
