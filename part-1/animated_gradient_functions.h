// Wilfredo Rodas
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

/* Do not edit below this line. */
/* Do not edit below this line. */
/* Do not edit below this line. */

#ifndef ANIMAGED_GRADIENT_FUNCTIONS_H
#define ANIMAGED_GRADIENT_FUNCTIONS_H

#include <string>
#include <vector>

bool HasMatchingFileExtension(const std::string& file_name,
                              const std::string& extension);

std::vector<double> BuildSineLookupTable(int image_width);

#endif
