// TODO: Add your header

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
