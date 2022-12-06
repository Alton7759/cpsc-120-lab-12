/// Wilfredo Rodas
// CPSC 120-01
// 2022-12-05
// rodaswilfredo24@csu.fullerton.edu
// @rodasw24
//
// Lab 12-01
// Partners: @AHan003, @alton7759
//
// Program that makes an animation.
//

#include "animated_gradient_functions.h"

#include <cmath>
#include <iostream>

bool HasMatchingFileExtension(const std::string& file_name,
                              const std::string& extension) {
  return file_name.size() >= extension.size() &&
         (file_name.compare(file_name.size() - extension.size(),
                            extension.size(), extension) == 0);
}

std::vector<double> BuildSineLookupTable(int image_width) {
  std::vector<double> lookup_table;
  double radian_step = M_PI / double(image_width);
  for (int column = 0; column < image_width; column++) {
    double sin_of = sin(radian_step * column);
    lookup_table.push_back(sin_of);
  }

  return lookup_table;
}
