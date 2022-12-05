// TODO: Add your header

/* Do not edit below this line. */
/* Do not edit below this line. */
/* Do not edit below this line. */

#ifndef MAKE_MESSAGE_FUNCTIONS_H
#define MAKE_MESSAGE_FUNCTIONS_H

#include <iostream>
#include <random>
#include <string>

// Check to see if file_name ends with the string extension, returns true if
// file_name ends with extension, false otherwise.
bool HasMatchingFileExtension(const std::string& file_name,
                              const std::string& extension);

// Flips a coin and returns true some of the time and false the rest of the
// time.
bool CoinFlip();

/// Generate a random number between min and max.
/// Uses the class RandomNumberGenerator to generate and return
/// a random number between \p min and \p max.
/// \param min The smallest value the random number generator should return
/// \param max The largest value the random number generator should return
/// \returns A random number
double RandomDouble(double min, double max);

/// Generate a randome number between 0 and 1
/// \returns A random number between 0 and 1
double RandomDouble01();

/// Generate a randome number between -1 and 1
/// \returns A random number between -1 and 1
double RandomDouble11();

/// The RandomNumberGenerator class is a wrapper around the Standard C++
/// Library's Mersenne Twister pseudo random number generator.
/// This class is complete and correct; please do not make any changes to it.
///
/// In lieu of directly working with the [Mersenne Twister
/// class]
/// (https://en.cppreference.com/w/cpp/numeric/random/mersenne_twister_engine),
/// this class serves as a lightweight wrapper around the necessary elements of
/// the library. The usage of this class is very simple and requires a
/// minimum and maximum value for initialization.
class RandomNumberGenerator {
 private:
  /// A hardware entropy source (a device on your computer to give random bits)
  /// A sequence of random bits to seed the Mersenne Twister engine
  // std::seed_seq seed;
  /// A Mersenne Twister engine
  std::mt19937 mt_engine_;
  /// A uniform distribution; select numbers randomly in a uniform manner
  std::uniform_real_distribution<double> uniform_dist_;

 public:
  /// Constructor to the RandomNumberGenerator class
  ///
  /// The RandomNumberGenerator generates random integer numbers between
  /// minimum and maximum. The constructor initializes and prepares
  /// the engine. To generate a number use the <RandomNumberGenerator::next>()
  /// method.
  ///
  /// minimum The lowest double value the random number generator will return
  /// maximum The largest double value the random number generator will return
  RandomNumberGenerator(double minimum, double maximum) {
    // A hardware entropy source (a device on your computer to give random bits)
    std::random_device rd;
    // A sequence of random bits to seed the Mersenne Twister engine
    std::seed_seq seed{rd()};
    // A Mersenne Twister engine
    mt_engine_ = std::mt19937{seed};
    // A uniform distribution; select numbers randomly in a uniform manner
    uniform_dist_ = std::uniform_real_distribution<double>{minimum, maximum};
  }

  // An alternate constructor which will always create randome numbers in a
  // predictable fashion so long as the seed sequence is the same.
  // We're using this constructor for testing our programs.
  RandomNumberGenerator(double minimum, double maximum, std::seed_seq& seed) {
    // A Mersenne Twister engine
    mt_engine_ = std::mt19937{seed};
    // A uniform distribution; select numbers randomly in a uniform manner
    uniform_dist_ = std::uniform_real_distribution<double>{minimum, maximum};
  }

  /// Return a random number
  ///
  /// Returns a random integer number between the minimum and maximum set
  /// when the constructor was called.
  ///
  /// returns An integer between the minimum and maximum set when
  /// the constructor was called
  double next() {
    double random_number = uniform_dist_(mt_engine_);
    // std::cout << "Debugging: The random number is " << random_number << "\n";
    return random_number;
  }
};

#endif