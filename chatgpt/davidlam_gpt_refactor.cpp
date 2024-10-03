
/// @function will populate and format the unigram to standard
///
/// @param unigram Struct of the unigram to be sorted
///
/// @param unigramCount The new number of words in unigram
///
/// @param word The word array with the words
///
/// @param wordCount The number of words in original array
///
/// @note The second and third outer for loops here will count
/// frequency of words and removed duplicate words while keeping
/// the words and frequencies matching each other.
void generate_unigrams(struct unigram unigram[], int& unigramCount,
                       string word[], int wordCount) {
    unigramCount = wordCount;    // Used for finding new number in unigram

    // Copy the word array into the unigram
    for (int idx = 0; idx < wordCount; idx++) {
        unigram[idx].word = "NA";    // Initialization of word
        unigram[idx].word = word[idx];
    }

    for (int idx = 0; idx < wordCount; idx++) {
        // Initializes unigram to 1
        unigram[idx].frequency = 1;

        // Checks second word to compare in unigram
        for (int j = idx + 1; j < wordCount; j++) {
            // && is needed as to ensure NULL is not
            // compared with NULL
            if ((unigram[idx].word.compare(unigram[j].word) == 0)
                && !unigram[idx].word.empty()) {
                unigram[idx].frequency++;
                unigramCount--;

                // erases the additional of the same word.
                // Prepares it for the next loop
                unigram[j].word.erase(0, unigram[j].word.length());
                //unigram[j].frequency = 0;
            }      // if, END
        }    // Inner for, END
    }      // Outer for, END

    // These loops will move the frequency as well as words
    // up. It also erases the word it copied
    for (int idx = 0; idx < wordCount; idx++) {
        for (int j = idx + 1; j < wordCount; j++) {
            if (unigram[idx].word.empty()) {        // Look, empty word array
                // replace word with the once after it
                unigram[idx].word = unigram[j].word;

                // replace frequency with the one after it
                unigram[idx].frequency = unigram[j].frequency;

                // The copied word is erased
                unigram[j].word.erase(0, unigram[j].word.length());
            }    // If, END
        }    // Inner for, END
    }    // Outer for, END

    // Moves words of larger freq up
    // unigramCount or wordCount can be used here
    sortgms(unigram, unigramCount);
}

/// @function will sort a string array and organize it from the
/// longest frequency to shortest
///
/// @param uni the struct array which contains the words
///
/// @param wordCount number of words in the array
///
/// @note Using a selection sort method, unigram has to already have frequency
/// in the array already. Also duplicate words must be removed already.
/// Function takes into account 0 frequencies and ignores them
void sortgms(struct unigram uni[], int wordCount) {
    string temp = "NA";
    int tempFQ;

    for (int idx = 0; idx < wordCount; idx++) {
        // Checks second freq to compare in unigram

        for (int j = idx + 1; j < wordCount; j++) {
            // && is needed as to ensure NULL is not considered
            if ((uni[j].frequency > uni[idx].frequency)
                && uni[idx].frequency != 0) {

                // Will move idx word into largest index word
                // and largest index word will move down to idx word
                temp = uni[j].word;
                uni[j].word = uni[idx].word;
                uni[idx].word = temp;

                // Moves idx freq into largest index freq
                // and largest index freq into idx freq
                tempFQ = uni[j].frequency;
                uni[j].frequency = uni[idx].frequency;
                uni[idx].frequency = tempFQ;
            }      // if, END
        }    // Inner for, END
    }      // Outer for, END
}

/// @brief Function will remove anything that is not a letter
/// or numeric value
///
/// @param word Array to be checked
///
/// @param wordCount Number of words in word array
int cleanup(string word[], int wordCount) {

    // Loop through entire array to see if cleanup is neccessary
    for (int idx = 0; idx < wordCount; idx++) {
        // If edit is made, original string is saved
        str = word[idx];
        /// https://www.programiz.com/cpp-programming/
        /// library-function/cctype/tolower
        /// Where I found out about tolower
        // For loop will change all letters into lowercase and erase
        // unwanted characters
        for (int i = 0; i < str.length(); i++) {
            // 63 through 90 are all capital letters. If it is
            // a capital letter, change to lower case
            if ((64 < str[i]) && (str[i] < 91)) {
                str[i] = tolower(str[i]);
                editMade = true;
            }    // if capital letters, END
            // If char is not a number or letter, erase it
            if ((!isalpha(str[i])) && (!isdigit(str[i]))) {
                str.erase(str.begin() + i);
                editMade = true;
                // As to ensure when undesirable is erase, immediate
                // char is not ignored. EX.  u.ELL
                // without i--   output is uEll
                i--;
            }    // If non-alpha, END
            if ((!isalpha(str[i])) && (isdigit(str[i]))) {
                // if value is a digit, change to NONALPHA
                // and close the loop
                str = "NONALPHA";
                i = 1000;      // Terminates loop
                editMade = true;
            }
        }               // Inner for, END
        if (editMade) {
            // output unedited string first
            outFile << word[idx] << setw(20) << "-->";
            // output edited string
            outFile << str << endl;
            editMade = false;        // toggle
            word[idx] = str;
        }        // if editMade, END
    }           // Outer for, END
}
