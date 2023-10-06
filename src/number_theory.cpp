#include <string>
#include <iostream>
#include <vector>
#include "../deps/bigint.h"


template<typename T> void printVector(std::vector<T> v) {
    std::cout << "[";
    for (int i = 0; i < v.size(); ++i) {
        std::cout << v[i];
        if (i + 1 != v.size()) {
            std::cout << ", ";
        }
    }
    std::cout << "]";
}


bigint gcd(bigint a, bigint b) {
    /* Find the greatest common divisor of integers a and b */
    bigint temp;
    while (a % b != (bigint)0) {
        temp = a;
        a = b;
        b = temp % a;
    }
    return b;
}

std::vector<bigint> euclideanAlgorithm(bigint a, bigint b) {
    /* Euclid's algorithm to find integers x and y
       that satisfy Bezout's identity: ax + by = gcd(a, b) */
    bigint s0 = 0, s1 = 1, t0 = 1, t1 = 0, r0 = b, r1 = a, q, temp;
    while (r0 != (bigint)0) {
        q = r1 / r0;
        temp = r0;
        r0 = r1 - q * r0;
        r1 = temp;
        temp = s0;
        s0 = s1 - q * s0;
        s1 = temp;
        temp = t0;
        t0 = t1 - q * t0;
        t1 = temp;
    }
    return {s1, t1};
}

bool isCoprime(bigint a, bigint b) {
    return (gcd(a, b) == (bigint)1);
}

int main(const int argc, const char** argv) {
    bigint a("15932973804208740238023357083740"), b("4247802238042803232723073027402");
    printVector(std::vector<bigint>{a, b});
    std::cout << " => ";
    printVector(euclideanAlgorithm(a, b));
    std::cout << std::endl;
    return 0;
}