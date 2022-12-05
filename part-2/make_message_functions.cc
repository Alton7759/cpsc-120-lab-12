// TODO: Add your header

#include "make_message_functions.h"

#include <iomanip>

bool HasMatchingFileExtension(const std::string& file_name,
                              const std::string& extension) {
  // TODO: Copy and paste the body of the function from Lab 10.
  return false;
}

// Secret global variable to make the randome number generator
// predictable
std::seed_seq rng_seed{1, 2, 3, 4, 5};

// Secret global variable that is used by RandomDouble_01()
RandomNumberGenerator rng_01{0, 1, rng_seed};

// Secret global variable that is used by RandomDouble_11()
RandomNumberGenerator rng_11{-1, 1, rng_seed};

// Secret global variable that is used by CoinFlip()
RandomNumberGenerator rng_coin_flip{-1, 1, rng_seed};

// Returns a random double between o and 1
double RandomDouble01() {
  // TODO: Using rng_01, call next() and return the next random number.
  return 0;
}

// Returns a random double between -1 and 1
double RandomDouble11() {
  // TODO: Using rng_11, call next() and return the next random number.
  return 0;
}

/// Return a True or False depending on a random value.
/// Generates a random number and then decides to return True or False
bool CoinFlip() {
  // TODO: Using rng_coin_flip, call next() and return true if the randome
  // number is greater than 0.0 and false otherwise.
  return false;
}
