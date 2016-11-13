#include <iostream>
#include <sstream>
#include <cstdio>
#include <cstring>
#include <string>
#include <cstdlib>
#include <cmath>
#include <cctype>
#include <ctime>
#include <algorithm>
#include <climits>
#include <cassert>
#include <vector>
#include <set>
#include <map>

const int MAX_H = 20;
const int MAX_B = 16;
const int MAX_M = 1 << MAX_B;

int counter[MAX_H][MAX_M];
unsigned h_a[MAX_H], h_b[MAX_H], h_v[MAX_H];

int B, M;

double alpha_norm(int n) {
	if (n == 16) {
		return 0.673;
	}
	if (n == 32) {
		return 0.697;
	}
	if (n == 64) {
		return 0.709;
	}
	return 0.7213 / (1 + 1.079 / n);
}

double exp2(int e) {
	return exp(log(2.0) * e);
}

double harmonic_mean(int v[], int n) {
	double ret = 0.0;
	for (int i = 0; i < n; ++ i) {
		ret += 1.0 / exp2(v[i]);
	}
	return n / ret;
}

const int MAX_L = (int)1e6;

char buffer[MAX_L];

unsigned hash_map(unsigned a, unsigned b, unsigned x) {
	return a * x + b;
}

unsigned code(unsigned v, std::string s) {
	unsigned ret = 0;
	for (int i = 0; i < s.length(); ++ i) {
		ret = ret * v + s[i] - 'a' + 1;
	}
	return ret;
}

void update(int &cc, unsigned p) {
	int tmp = (p == 0 ? 32 : __builtin_clz(p)) - B + 1;
	cc = std::max(cc, tmp);
}

unsigned u_rand() {
	return (rand() << 1) | (rand() & 1);
}

int to_int(char *buf) {
	std::istringstream sin(buf);
	int ret;
	sin >> ret;
	return ret;
}

int period, allwords;
int constant;
double linear, square;

bool is_vowel(char ch) {
	static const char vowel[5] = {'a', 'e', 'i', 'o', 'u'};
	return std::find(std::begin(vowel), std::end(vowel), ch) != std::end(vowel);
}

int main(int argc, char *argv[]) {
	srand(100003);

	if (argc > 1) {
		B = to_int(argv[1]);
		assert(B >= 4);
	}
	else {
		B = 4;
	}
	M = 1 << B;

	for (int i = 0; i < MAX_H; ++ i) {
		h_a[i] = u_rand();
		h_b[i] = u_rand();
		while (h_v[i] <= 26) {
			h_v[i] = u_rand();
		}
	}

	for (int i = 0; i < MAX_H; ++ i) {
		for (int j = 0; j < M; ++ j) {
			counter[i][j] = 0;
		}
	}

	//std::set<std::string> dict;

	char *tokenizer = NULL;
	while (gets(buffer)) {
		tokenizer = buffer;
		while (*tokenizer != '\0') {
			char word[200];
			word[0] = '\0';
			sscanf(tokenizer, "%[a-zA-Z]", word);
			std::string tmp(word);
			std::transform(tmp.begin(), tmp.end(), tmp.begin(), tolower);
			tokenizer += tmp.length();
			if (*tokenizer == '.') {
				++ period;
			}
			if (*tokenizer != '\0') {
				++ tokenizer;
			}
			if (tmp == "") {
				continue;
			}

			++ allwords;

			++ constant;
			int score = 0;
			char last = '#';
			for (auto ch : tmp) {
				if (is_vowel(ch) && last != ch) {
					++ score;
				}
				last = ch;
			}
			int pos = tmp.length() - 2;

			if (tmp.length() > 1 && !is_vowel(tmp[0]) && !is_vowel(tmp[1])) {
				++ score;
			}
			if (pos >= 0 && last == 'l' && !is_vowel(tmp[pos])) {
				++ score;
			}

			if (pos >= 0 && last == 'y' && !is_vowel(tmp[pos])) {
				++ score;
			}

			if (!is_vowel(last) && last != 'g' && last != 'q' && last != 'r' && last != 'w' && last != 'l' && last != 'y') {
				++ score;
			}
			//score /= tmp.length();
			linear += score;
			square += score * score;
			//printf("%d\n", score);

			//dict.insert(tmp);

			for (int j = 0; j < MAX_H; ++ j) {
				unsigned p = hash_map(h_a[j], h_b[j], code(h_v[j], tmp));
				update(counter[j][p >> (32 - B)], p << B >> B);
			}
			//std::cerr << tmp << std::endl;
		}

	}

	double ret = 0;
	for (int i = 0; i < MAX_H; ++ i) {
		double e = harmonic_mean(counter[i], M) * alpha_norm(M) * M;
		if (e < 2.5 * M) {
			int tmp = 0;
			for (int j = 0; j < M; ++ j) {
				if (counter[i][j] == 0) {
					++ tmp;
				}
			}
			if (tmp > 0) {
				ret += M * log((double)M / tmp);
			}
			else {
				ret += e;
			}
		}
		else if (e < exp2(32) / 30.0) {
			ret += e;
		}
		else {
			ret += -exp2(32) * log(1.0 - e / exp2(32));
		}
	}

	double expect = (double)linear / constant;
	double pop = (double)square / constant - expect * expect;
	double length = (double)allwords / period;
	double result = ret / MAX_H / 50.0 + pop * 5.0 + length * 1.0;
	printf("amount = %f, popularity = %f, length = %f\n", ret / MAX_H / 50.0, pop * 5.0, length);
	printf("%f\n", result);

	return 0;
}

