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
  std::vector<std::string> args{argv, argv + argc};
  // convert the command line arguments to a
  // std::vector of std::strings.
  if (args.size() < 2) {
    std::cout << "Please provide a path to a file.\n";
    return 1;
  }
  std::string output_file_name{args.at(1)};
  std::string image_format{".gif"};
  if (!HasMatchingFileExtension(output_file_name, image_format)) {
    std::cout << output_file_name
              << " is missing the required file extension .gif.\n";
    return 1;
  }
  std::vector<double> sine_lookup_table = BuildSineLookupTable(kImageWidth);
  Magick::ColorRGB white(1, 1, 1);
  std::vector<Magick::Image> images;
  double bule_step = M_PI / double(kNumberOfImages);
  int row_col_step = kImageWidth / kNumberOfImages;
  for (int current_image = 0; current_image < kNumberOfImages;
       current_image++) {
    Magick::Image image =
        Magick::Image(Magick::Geometry(kImageWidth, kImageHeight), white);
    std::cerr << "Image " << current_image + 1 << "...";
    double blue = sin(bule_step * current_image);

    for (int column = 0; column < image.columns(); column++) {
      for (int row = 0; row < image.rows(); row++) {
        int current_step = current_image * row_col_step;
        double red =
            sine_lookup_table.at((column + current_step) % kImageWidth);
        double green =
            sine_lookup_table.at((row + current_step) % kImageHeight);
        Magick::ColorRGB color(red, green, blue);
        image.pixelColor(column, row, color);
      }
    }
    images.push_back(image);
    std::cerr << "completed.\n";
  }
  Magick::writeImages(images.begin(), images.end(), output_file_name);
  // Check to make sure you have enough arguments. If you have
  // too few, print an error message and exit.
  // Declare a std::string variable named output_file_name.
  // Assign the first argument to output_file_name

  // Declare a std::string variable named image_format and
  // initialize it to ".gif"
  // Using HasMatchingFileExtension(), check to see if
  // output_file_name has the extension defined as image_format. If
  // output_file_name does not, then print an error message and return 1.

  // Lookup Table
  // Declare a std::vector of doubles, name the variable
  // sine_lookup_table.
  // call BuildSineLookupTable() with kImageWidth, assign the return value
  // to sine_lookup_table

  // Declare a Magick::ColorRGB variable named white and set it's
  // color to white which means setting each color channel to 1.
  // For example:
  // Magick::ColorRGB white(1, 1, 1);

  // Declare a std::vector of Magick::Image, name the variable images.

  // Declare a double variable named blue_step. Intialize it to M_PI
  // divided by kNumberOfImages. Remember to convert kNumberOfImages to a double
  // to avoid integer division.
  // Declare an int variable named row_col_step and initialize it to
  // kImageWidth / kNumberOfImages.

  // Write the images to an output file using Magick::writeImages()
  // For example:
  // Magick::writeImages(images.begin(), images.end(), output_file_name);

  return 0;
}
