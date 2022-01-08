// Tanay Bennur 12/29/2021
// C implementation of stylizing function

#include <stdbool.h>
#include <stdlib.h>

// This function stylizes jpg and png image files
// This function does not check input validity
void stylize(short *image, short *pallet, int num_rows, int num_columns, 
             int num_colors, bool is_jpg) 
{
    
    int increment = is_jpg ? 3 : 4;
    int i = 0;
    
    for (int i = 0; i < num_rows * num_columns; i++) {
       
        short current_red = *image;
        short current_green = *(image + 1);
        short current_blue = *(image + 2);
        short best_score = 9999;
        short current_score;
       
        for (int j = 0; j < num_colors * 3; j += 3) {
            
            current_score = abs(pallet[j] - current_red) + 
                            abs(pallet[j + 1] - current_green) + 
                            abs(pallet[j + 2] - current_blue);
            
            if (current_score <= best_score) {
                *image = pallet[j];
                *(image + 1) = pallet[j + 1];
                *(image + 2) = pallet[j + 2];
                best_score = current_score;
            }

        }
              
        image = image + increment;
        
    }
}