#include <array>
#include <iostream>
#include <vector>

// this is for t=2, d=1

typedef std::pair<std::array<int, 2>, std::array<int, 2>> interaction;

const int k = 8;
const int v = 3;
const int N = 12;
const int pop_size = 200;

auto generate_interactions(int k, int v) {
    std::vector<interaction> interactions;
    for (int k1=0; k1<k; k1++) {
        for (int k2=k1+1; k2<k; k2++) {
            for (int v1=0; v1<v; v1++) {
                for (int v2=0; v2<v; v2++) {
                    std::array<int, 2> cols{{k1,k2}};
                    std::array<int, 2> vals{{v1,v2}};
                    auto pair = std::make_pair(cols,vals);
                    interactions.push_back(pair);
                }
            }
        }
    }
    return interactions;
}

auto is_in_row(const std::array<int,k>& row, const interaction& inter) {
    auto cols = inter.first;
    auto vals = inter.second;
    for (int col_idx=0; col_idx<cols.size(); col_idx++) {
        if (vals[col_idx] != row[col_idx]) {
            return false;
        }
    }
    return true;
}

auto fitness(const std::vector<std::array<int, k>>& array) {
    int count = 0;
    auto interactions = generate_interactions(k,v);
    for (int idx1=0; idx1<interactions.size(); idx1++) {
        for (int idx2=idx1+1; idx2<interactions.size(); idx2++) {
            bool different = false;
            for (int row_idx=0; row_idx<array.size(); row_idx++) {
                auto row = array[row_idx];
                auto inter1 = interactions[idx1];
                auto inter2 = interactions[idx2];
                if (is_in_row(row,inter1) != is_in_row(row,inter2)) {
                    different = true;
                    break;
                }
            }
            if (different) {
                count += 1;
            }
        }
    }
    return count;
}

int main() {

}
