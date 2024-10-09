
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
/// @param wordCount Number of words in word array
int cleanup(string word[], int wordCount) {
    ofstream outFile("output.txt");  // Assuming this is defined earlier

    for (int idx = 0; idx < wordCount; ++idx) {
        string original = word[idx];
        string cleaned;
        bool hasDigit = false;

        // Loop through each character in the word
        for (char ch : original) {
            if (isalpha(ch)) {
                // Convert to lowercase if it's an alphabetic character
                cleaned += tolower(ch);
            } else if (isdigit(ch)) {
                hasDigit = true;
                break;  // Exit the loop if a digit is found
            }
        }

        // If a digit was found, replace the word with "NONALPHA"
        if (hasDigit) {
            cleaned = "NONALPHA";
        }

        // Output if any changes were made
        if (cleaned != original) {
            outFile << original << setw(20) << "--> " << cleaned << endl;
            word[idx] = cleaned;
        }
    }

    outFile.close();
    return 0;  // Assuming a return value is needed
}