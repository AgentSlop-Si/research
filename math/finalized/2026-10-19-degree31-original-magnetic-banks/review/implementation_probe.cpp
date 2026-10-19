// Independently written driver for the candidate's exact active field implementation.
#define main candidate_discovery_main_not_run
#include "search_degree31.cpp"
#undef main
#include <limits>
#include <string>
static_assert(std::numeric_limits<int>::max() >= 2147483647, "32-bit signed reduction capacity required");
int main() {
    std::string op;
    while (std::cin >> op) {
        F a, b;
        for (int &v : a.a) std::cin >> v;
        if (op == "mul") {
            for (int &v : b.a) std::cin >> v;
            std::cout << a*b << '\n';
        } else if (op == "pow") {
            std::string exponent; std::cin >> exponent;
            std::cout << a.power(Big(exponent)) << '\n';
        } else if (op == "inv") {
            std::cout << a.inverse() << '\n';
        } else return 2;
    }
}
