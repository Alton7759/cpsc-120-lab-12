// Wilfredo Rodas
// CPSC 120-01
// 2022-12-05
// rodaswilfredo24@csu.fullerton.edu
// @rodasw24
//
// Lab 12-02
// Partners: @AHan003, @alton7759
//
// Uses random number generator function
//

#include "make_message_functions.h"

#include <iomanip>

bool HasMatchingFileExtension(const std::string& file_name,
                              const std::string& extension) {
  return file_name.size() >= extension.size() &&
         (file_name.compare(file_name.size() - extension.size(),
                            extension.size(), extension) == 0);
  return false;
}

std::seed_seq rng_seed{1, 2, 3, 4, 5};

RandomNumberGenerator rng_01{0, 1, rng_seed};

RandomNumberGenerator rng_11{-1, 1, rng_seed};

RandomNumberGenerator rng_coin_flip{-1, 1, rng_seed};

double RandomDouble01() {
  return rng_01.next();
  ;
}

double RandomDouble11() { return rng_11.next(); }

bool CoinFlip() { return rng_coin_flip.next() > 0.0; }
