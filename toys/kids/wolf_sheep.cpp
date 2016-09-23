#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

/* chessboard sizes */
const int CB_W = 8;
const int CB_H = 8;

long long position_counter;
int wolf_trapped;
int sheep_blocked;

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

inline void board_set(Pos p, FieldState fs)
{
	board[p.r][p.c] = fs;
}

inline bool legal(Pos p)
{
	return p.r >= 0 && p.r < CB_H && p.c >= 0 && p.c < CB_W && board[p.r][p.c] == EMPTY;
}

GameResult sheep();

GameResult wolf()
{
    if (++ position_counter % 100000000 == 0)
	{
		cout << "Position " << position_counter << endl;
		print_board();
	}
#ifdef VERBOSE
	cout << "Wolf to move:" << endl;
	print_board();
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
			auto res = sheep();
			pWolf = origPos;
			board_set(newPos, EMPTY);
			board_set(origPos, WOLF);
			if (res == WOLF_WINS)
			{
				return res;
			}
		}
	}
	
	if (cantMove && ++wolf_trapped % 1000000 == 0)
	{
		cout << "Wolf trapped " << wolf_trapped << endl;
		print_board();
	}
	return SHEEP_WIN;
}

GameResult sheep()
{
#ifdef VERBOSE
	cout << "Sheep to move:" << endl;
	print_board();
#endif
	if (pWolf.r == CB_H - 1
		|| max_element(begin(pSheep), end(pSheep),
					   [](Pos a, Pos b){ return a.r < b.r; })->r <= pWolf.r)
	{
#ifdef VERBOSE
		cout << "Wolf (" << pWolf.r << ", " << pWolf.c << ") passed or is at finish line" << endl;
#endif
		return WOLF_WINS;
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
				auto res = wolf();
				pOneSheep = origPos;
				board_set(newPos, EMPTY);
				board_set(origPos, SHEEP);
				if (res == SHEEP_WIN)
				{
					return res;
				}
			}
			// else { cout << "Pos " << newPos.r << ", " << newPos.c << " illegal for sheep." << endl; }
		}
	}
	
	return WOLF_WINS;
}

int main()
{
	init();
	if (wolf() == WOLF_WINS)
		cout << "Wolf wins if he starts" << endl;
	else
		cout << "Wolf loses even if he starts" << endl;
/*
	if (sheep() == SHEEP_WIN)
		cout << "Sheep wins if she starts" << endl;
	else
		cout << "Sheep loses even if she starts" << endl;
*/
	return 0;
}
