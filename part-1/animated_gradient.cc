
// TODO: Add your header

#include <Magick++.h>

#include <cmath>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

#include "animated_gradient_functions.h"

// The width of the image is the number of columns.
const int kImageWidth{512};
// The height of the image is the number of rows.
const int kImageHeight{512};
// The number of images in our flipbook animation.
const int kNumberOfImages = 10;

int main(int argc, char* argv[]) {
  // Initialize the GraphicsMagick library. It must be the first thing
  // that happens in the main function.
  // Do not change or remove the line below.
  Magick::InitializeMagick(*argv);
  // TODO: convert the command line arguments to a
  // std::vector of std::strings.
  // TODO: Check to make sure you have enough arguments. If you have
  // too few, print an error message and exit.
  // TODO: Declare a std::string variable named output_file_name.
  // TODO: Assign the first argument to output_file_name

  // TODO: Declare a std::string variable named image_format and
  // initialize it to ".gif"
  // TODO: Using HasMatchingFileExtension(), check to see if
  // output_file_name has the extension defined as image_format. If
  // output_file_name does not, then print an error message and return 1.

  // Lookup Table
  // TODO: Declare a std::vector of doubles, name the variable
  // sine_lookup_table.
  // TODO: call BuildSineLookupTable() with kImageWidth, assign the return value
  // to sine_lookup_table

  // TODO: Declare a Magick::ColorRGB variable named white and set it's
  // color to white which means setting each color channel to 1.
  // For example:
  // Magick::ColorRGB white(1, 1, 1);

  // TODO: Declare a std::vector of Magick::Image, name the variable images.

  // TODO: Declare a double variable named blue_step. Intialize it to M_PI
  // divided by kNumberOfImages. Remember to convert kNumberOfImages to a double
  // to avoid integer division.
  // TODO: Declare an int variable named row_col_step and initialize it to
  // kImageWidth / kNumberOfImages.

  for (int current_image = 0; current_image < kNumberOfImages;
       current_image++) {
    // TODO: Declare a Magick::Image variable named image. Initialize it to be
    // kImageWidth by kImageHeight and fill it with white. See Lab 10 for an
    // example.
    std::cerr << "Image " << current_image + 1 << "...";
    // TODO: Declare a double named blue and assign it the blue value needed for
    // the current image. This value is the sine of blue_step * current_image
    // TODO: Create an inner and outer loop to visit each pixel.
    // For example:
    //for (int column = 0; column < image.columns(); column++) {
      //for (int row = 0; row < image.rows(); row++) {
        // TODO: Declare an int variable named current_step and initliaze it to 
        // current_image * row_col_step
        // TODO: Declare a double variable named red. Initialize it to the
        // correct value from the sine_lookup_table.
        // TODO: Declare a double variable named green. Initialize it to the
        // correct value from the sine_lookup_table.
        // TODO: Declare a Magick::ColorRGB variable named color and initialize
        // it with the values from the red, green, blue variables.
        // TODO: Set the current pixel color in the image to the new color.
        // For example:
        // image.pixelColor(column, row, color);
    //   }
    // }
    // TODO: Use push_back to add the current image to the vector images.
    std::cerr << "completed.\n";
  }
  // TODO: Write the images to an output file using Magick::writeImages()
  // For example:
  // Magick::writeImages(images.begin(), images.end(), output_file_name);

  return 0;
}
