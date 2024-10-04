// TODO code needs to be better understood using chat gpt
#include <fstream>// to read text file
#include <iostream>
#include <iterator>// to remove elements from vector
#include <vector>  // to use vector container

// the cross word puzzles will be 10x10
const int ROWS = 10;
const int COLUMNS = 10;

// function to get crossword puzzle and words from text file
void readFile(std::string fileName, std::vector<std::vector<char>> &puzzle,
              std::vector<std::string> &wordList);

// function to print crossword puzzle
void printCrosswordPuzzle(std::vector<std::vector<char>> puzzle);

// function to solve cross word puzzle
void solveCrosswordPuzzle(std::vector<std::vector<char>> &puzzle,
                          std::vector<std::string> wordList);

// utilization function to do the actual solving by using recursion
bool utilSolveCrosswordPuzzle(std::vector<std::vector<char>> &puzzle,
                              std::vector<std::string> &wordList,
                              int row, int column);

// function to find where to place word // will return size 2 int array
// that will store row and column where Word can be placed
std::vector<int> findIndicesToPlaceWord(std::vector<std::vector<char>> &puzzle,
                                        int row, int column);

// function to see if word to be placed is left-right
bool isLeftRight(std::vector<std::vector<char>> &puzzle, int row, int column);
// function to see if word to be placed is top-bottom
bool isTopBottom(std::vector<std::vector<char>> &puzzle, int row, int column);

// functions to find left-bound index and right bound index
int leftBoundIndex(std::vector<std::vector<char>> &puzzle, int row,
                   int column);
int rightBoundIndex(std::vector<std::vector<char>> &puzzle, int row,
                    int column);

// functions to find top-bound index and bottom-bound index
int topBoundIndex(std::vector<std::vector<char>> &puzzle, int row,
                  int column);
int bottomBoundIndex(std::vector<std::vector<char>> &puzzle, int row,
                     int column);

// functions to place word in left-right and top-bottom
// and remove word in vector and return word that was removed
// if it returns empty string then a word cannot be placed
std::string placeLeftRight(std::vector<std::vector<char>> &puzzle,
                           std::vector<std::string> &wordList, int row,
                           int leftIndex, int size);
std::string placeTopBottom(std::vector<std::vector<char>> &puzzle,
                           std::vector<std::string> &wordList, int column,
                           int topIndex, int size);

// function to erase given word from vector
bool eraseWordFromList(std::vector<std::string> &wordList, std::string word);

// function to remove left-right word
void removeLeftRightWord(std::vector<std::vector<char>> &puzzle,
                         std::string word, int row, int leftIndex);
// function to remove top-bottom word
void removeTopBottomWord(std::vector<std::vector<char>> &puzzle,
                         std::string word, int column, int topIndex);

int main() {
    // to store file name
    std::string filename;
    // getting input for text file
    std::cout << "Enter filename: ";
    std::getline(std::cin, filename);
    // creating file object and opening file
    std::ifstream textFile;
    textFile.open(filename);
    // checking if file name is not valid
    if (!textFile.is_open()) {
        std::cout << "Error: filename is not valid!" << std::endl;
        return 0;// exit program
    }
    std::cout << std::endl;

    // to store crossword puzzle in text file as a 2d char matrix
    std::vector<std::vector<char>>
            crosswordPuzzle(ROWS, std::vector<char>(COLUMNS, '!'));
    // to store words in crossword puzzle
    std::vector<std::string> words;

    // reading text file to get crossword puzzle and words
    readFile(filename, crosswordPuzzle, words);
    // solving crossword puzzle
    solveCrosswordPuzzle(crosswordPuzzle, words);
    // printing solved crossword puzzle
    printCrosswordPuzzle(crosswordPuzzle);

    return 0;
}

// function to get crossword puzzle and words from text file
void readFile(std::string fileName, std::vector<std::vector<char>> &puzzle,
              std::vector<std::string> &wordList) {
    // crating file object and opening text file
    std::ifstream textFile;
    textFile.open(fileName);

    // reading text file to get matrix
    for (int i = 0; i < puzzle.size(); i++) {
        for (int j = 0; j < puzzle[i].size(); j++) {
            textFile >> puzzle[i][j];
        }
    }

    // reading empty line between crossword puzzle and words in text file
    std::string line;
    std::getline(textFile, line);
    // reading words in text file into word list vector
    while (!textFile.eof()) {
        // getting word
        std::string word;
        textFile >> word;
        // if word is empty exit loop
        if (word.empty()) {
            break;
        }
        wordList.push_back(word);
    }
}

// function to print crossword puzzle
void printCrosswordPuzzle(std::vector<std::vector<char>> puzzle) {
    for (int i = 0; i < puzzle.size(); i++) {
        for (int j = 0; j < puzzle[i].size(); j++) {
            // printing out element
            std::cout << puzzle[i][j];
        }
        // going to next line
        std::cout << std::endl;
    }
}

// function to solve cross word puzzle
void solveCrosswordPuzzle(std::vector<std::vector<char>> &puzzle,
                          std::vector<std::string> wordList) {

    // calling recursive solve function to do the actual solving
    utilSolveCrosswordPuzzle(puzzle, wordList, 0, 0);

    //Note:
    // won't modify list in main because we passed a copy of the word list
}
// utilization function to do the recursion in solveCrosswordPuzzle();
bool utilSolveCrosswordPuzzle(std::vector<std::vector<char>> &puzzle,
                              std::vector<std::string> &wordList,
                              int row, int column) {

    // checking if word list is empty which means all words have been placed
    if (wordList.empty()) {
        return true;
    }


    // finding position to place word:
    int rowPosition = 0;   // to store row index where word can be placed
    int columnPosition = 0;// to store column index where word can be placed
    // finding a location to place the word
    std::vector<int> indices = findIndicesToPlaceWord(puzzle, row, column);
    rowPosition = indices[0];
    columnPosition = indices[1];
    // if there are no places to place word
    if (rowPosition == -1 || columnPosition == -1) {
        std::cout << "Error: Invalid indices!" << std::endl;
        return false;
    }

    // finding out what kind of word can be placed:
    // to determine if word to be placed is left-right
    bool leftRight = isLeftRight(puzzle, rowPosition, columnPosition);
    // to determine if word to be placed is top-bottom
    bool topBottom = isTopBottom(puzzle, rowPosition, columnPosition);

    // to store word to be placed
    std::string word;
    // to store size of word to be placed
    int wordSize = 0;
    // to store bounds
    int leftBound = 0;
    int rightBound = 0;
    int topBound = 0;
    int bottomBound = 0;


    // it is a left-right word to be placed
    if (leftRight) {

        // finding the left and right bound indexes
        leftBound = leftBoundIndex(puzzle, rowPosition, columnPosition);
        rightBound = rightBoundIndex(puzzle, rowPosition, columnPosition);
        // calculating word size
        wordSize = (rightBound - leftBound) + 1;

        // placing word
        word = placeLeftRight(puzzle, wordList, leftBound, rowPosition,
                              wordSize);
        // no valid ways to place a word
        if (word.empty()) {
            return false;
        }

    }

    // it is a top-bottom word to be placed
    else if (topBottom) {

        // finding the left and right bound indexes
        topBound = topBoundIndex(puzzle, rowPosition, columnPosition);
        bottomBound = bottomBoundIndex(puzzle, rowPosition, columnPosition);
        // calculating word size
        wordSize = (bottomBound - topBound) + 1;

        // placing word
        word = placeTopBottom(puzzle, wordList, topBound, columnPosition,
                              wordSize);
        // no valid ways to place a word
        if (word.empty()) {
            return false;
        }
    }


    //     going to the next word
    //     if trying to place the next word returns a false value then try
    //     placing a different word
    std::vector<int> newIndices;
    newIndices = findIndicesToPlaceWord(puzzle, rowPosition, columnPosition);
    int newRowPosition = newIndices[0];
    int newColumnPosition = newIndices[1];
    if (newRowPosition == -1 || newColumnPosition == -1) {
        newRowPosition = 0;
        newColumnPosition = 0;
    }
    // to see if word that was placed was valid
    bool wordWasValid = utilSolveCrosswordPuzzle(puzzle, wordList,
                                                 newRowPosition,
                                                 newColumnPosition);
    if (!wordWasValid) {
        // it is a left right word
        if (leftRight) {
            // removing placed word from matrix
            removeLeftRightWord(puzzle, word, rowPosition, leftBound);


            // placing a different word
            std::string newWord;
            newWord = placeLeftRight(puzzle, wordList, leftBound,
                                     rowPosition, wordSize);
            // adding back old word
            wordList.push_back(word);
            // no valid ways to place a word
            if (newWord.empty()) {
                return false;
            }

        }
        // it is a top bottom word
        else if (topBottom) {
            // removing placed word from matrix
            removeTopBottomWord(puzzle, word, columnPosition, topBound);

            // placing a different word
            std::string newWord;
            newWord = placeTopBottom(puzzle, wordList, topBound,
                                     columnPosition, wordSize);
            // adding back old word
            wordList.push_back(word);
            // no valid ways to place a word
            if (newWord.empty()) {
                return false;
            }
        }
    }

    // checking if list is empty and if it is not continue going to the next
    // word
    if (wordList.empty()) {
        return true;
    } else {
        return utilSolveCrosswordPuzzle(puzzle, wordList,
                                        newRowPosition, newColumnPosition);
    }
}

// function to find where to place word // will return size 2 int array
// that will store row and column where Word can be placed
std::vector<int> findIndicesToPlaceWord(std::vector<std::vector<char>> &puzzle,
                                        int row, int column) {
    // to store if word position was found
    bool wordSpotFound = false;

    // to store a vector of indices to be returned
    std::vector<int> indices(2);

    // to store row and column indices
    int rPos = 0;
    int cPos = 0;
    // searching for indices where a word can be placed
    for (int i = row; i < puzzle.size(); i++) {
        for (int j = column; j < puzzle[i].size(); j++) {
            // finding where a '-' sign shows up which means word can be placed
            if (puzzle[i][j] == '-') {
                // saving position of word to be placed
                rPos = i;
                cPos = j;

                wordSpotFound = true;

                break;// exit inner for loop
            }
        }

        // exit outer loop because word spot was found
        if (wordSpotFound) {
            break;
        }
    }

    // checking if word spot was not found
    if (!wordSpotFound) {
        indices[0] = -1;
        indices[1] = -1;
        return indices;
    }

    // setting indices to return
    indices[0] = rPos;
    indices[1] = cPos;


    // returning indices vector that has the space where a word can be placed
    return indices;
}

// function to see if word to be placed is left-right
bool isLeftRight(std::vector<std::vector<char>> &puzzle, int row, int column) {
    // checking to see if it is left-right word
    // looking at right character
    if (column + 1 <= (puzzle[column].size() - 1)) {
        if (puzzle[row][column + 1] == '-' || puzzle[row][column + 1] != '+') {
            return true;
        }
    }
    // looking at left character
    if (column - 1 >= 0) {
        if (puzzle[row][column - 1] == '-' || puzzle[row][column - 1] != '+') {
            return true;
        }
    }

    // not left-right
    return false;
}
// function to see if word to be placed is top-bottom
bool isTopBottom(std::vector<std::vector<char>> &puzzle, int row, int column) {
    // checking to see if it is top-bottom word
    // looking at bottom character
    if (row + 1 <= (puzzle[row].size() - 1)) {
        if (puzzle[row + 1][column] == '-' || puzzle[row + 1][column] != '+') {
            return true;
        }
    }
    // looking at top character
    if (row - 1 >= 0) {
        if (puzzle[row - 1][column] == '-' || puzzle[row - 1][column] != '+') {
            return true;
        }
    }

    // not top-bottom
    return false;
}

// functions to find left-bound index and right bound index
int leftBoundIndex(std::vector<std::vector<char>> &puzzle, int row,
                   int column) {
    int leftBoundIndex = column;
    for (int i = column; i >= 0; i--) {
        if (puzzle[row][i] == '+') {
            break;
        }
        // finding right bound index
        if (puzzle[row][i] == '-' || puzzle[row][i] != '+') {
            leftBoundIndex = i;
        }
    }
    return leftBoundIndex;
}
int rightBoundIndex(std::vector<std::vector<char>> &puzzle, int row,
                    int column) {
    int rightBoundIndex = column;
    for (int i = column; i < puzzle.size(); i++) {
        if (puzzle[row][i] == '+') {
            break;
        }
        // finding right bound index
        if (puzzle[row][i] == '-' || puzzle[row][i] != '+') {
            rightBoundIndex = i;
        }
    }
    return rightBoundIndex;
}

// functions to find top-bound index and bottom-bound index
int topBoundIndex(std::vector<std::vector<char>> &puzzle, int row,
                  int column) {
    int topBoundIndex = row;
    for (int i = row; i >= 0; i--) {
        // checking if we have reached a plus sign
        if (puzzle[i][column] == '+') {
            break;
        }
        // finding right bound index
        if (puzzle[i][column] == '-' || puzzle[i][column] != '+') {
            topBoundIndex = i;
        }
    }
    return topBoundIndex;
}
int bottomBoundIndex(std::vector<std::vector<char>> &puzzle, int row,
                     int column) {
    int bottomBoundIndex = row;
    for (int i = row; i < puzzle.size(); i++) {
        // checking if we have reached a plus sign
        if (puzzle[i][column] == '+') {
            break;
        }
        // finding right bound index
        if (puzzle[i][column] == '-' || puzzle[i][column] != '+') {
            bottomBoundIndex = i;
        }
    }
    return bottomBoundIndex;
}

// functions to place word in left-right and top-bottom
// and remove word in vector and return word that was removed
// if it returns empty string then a word cannot be placed
std::string placeLeftRight(std::vector<std::vector<char>> &puzzle,
                           std::vector<std::string> &wordList, int leftIndex,
                           int row, int size) {
    // creating vector of possible valid words, which means they match the size
    std::vector<std::string> possibleWords;
    // finding words that can be placed
    for (int i = 0; i < wordList.size(); i++) {
        // checking to see if word has the right size
        if (wordList[i].size() == size) {
            possibleWords.push_back(wordList[i]);
        }
    }
    // if list of possible words is empty return empty word
    if (possibleWords.empty()) {
        std::string emptyString;
        return emptyString;
    }

    // try placing the possible words
    bool validWord = true;// to see if word is valid
    std::string word;     // to store word that will be returned
    for (int j = 0; j < possibleWords.size(); j++) {
        // resetting valid word value
        validWord = true;
        // setting current word
        word = possibleWords[j];

        // checking to see if word is valid
        int countIndex = leftIndex;
        for (int i = 0; i < size; i++) {
            if (puzzle[row][countIndex] != '-' &&
                word[i] != puzzle[row][countIndex]) {
                validWord = false;
                break;
            }
            countIndex++;
        }
        // word is not valid
        if (!validWord) {
            word.clear();
            continue;// moving to next word
        }

        // word is valid
        // actually placing word
        countIndex = leftIndex;
        for (int i = 0; i < size; i++) {
            puzzle[row][countIndex] = word[i];
            countIndex++;
        }
        // removing word from word list
        eraseWordFromList(wordList, word);

        return word;
    }

    // if out of for loop word will be empty adn return it
    return word;
}

std::string placeTopBottom(std::vector<std::vector<char>> &puzzle,
                           std::vector<std::string> &wordList, int topIndex,
                           int column, int size) {

    // creating vector of possible valid words, which means they match the size
    std::vector<std::string> possibleWords;
    // finding words that can be placed
    for (int i = 0; i < wordList.size(); i++) {
        // checking to see if word has the right size
        if (wordList[i].size() == size) {
            possibleWords.push_back(wordList[i]);
        }
    }
    // if list of possible words is empty return empty word
    if (possibleWords.empty()) {
        std::string emptyString;
        return emptyString;
    }

    // try placing the possible words
    bool validWord = true;// to see if word is valid
    std::string word;     // to store word that will be returned
    for (int j = 0; j < possibleWords.size(); j++) {
        // resetting valid word value
        validWord = true;
        // setting current word
        word = possibleWords[j];

        // checking to see if word is valid
        int countIndex = topIndex;
        for (int i = 0; i < size; i++) {
            if (puzzle[countIndex][column] != '-' &&
                word[i] != puzzle[countIndex][column]) {
                validWord = false;
                break;
            }
            countIndex++;
        }
        // word is not valid
        if (!validWord) {
            word.clear();
            continue;// moving to next word
        }

        // word is valid
        // actually placing word
        countIndex = topIndex;
        for (int i = 0; i < size; i++) {
            puzzle[countIndex][column] = word[i];
            countIndex++;
        }
        // removing word from word list
        eraseWordFromList(wordList, word);

        return word;
    }

    // if out of for loop word will be empty adn return it
    return word;
}

// function to erase given word from vector
bool eraseWordFromList(std::vector<std::string> &wordList, std::string word) {
    for (auto it = wordList.begin(); it != wordList.end(); it++) {
        // deleting word that needed to be found
        if (*it == word) {
            it = wordList.erase(it);
            return true;
        }
    }
    // word was not found
    return false;
}

// function to remove left-right word
void removeLeftRightWord(std::vector<std::vector<char>> &puzzle,
                         std::string word, int row, int leftIndex) {
    int countIndex = leftIndex;
    for (int i = 0; i < word.size(); i++) {

        // checking character above
        if (row - 1 >= 0) {
            if (puzzle[row - 1][countIndex] == '+' ||
                puzzle[row - 1][countIndex] == '-') {

                puzzle[row][countIndex] = '-';
            }
        }
        // checking character below
        if (row + 1 <= (puzzle.size() - 1)) {
            if (puzzle[row + 1][countIndex] == '+' ||
                puzzle[row + 1][countIndex] == '-') {

                puzzle[row][countIndex] = '-';
            }
        }

        // next character
        countIndex++;
    }
}
// function to remove top-bottom word
void removeTopBottomWord(std::vector<std::vector<char>> &puzzle,
                         std::string word, int column, int topIndex) {

    int countIndex = topIndex;
    for (int i = 0; i < word.size(); i++) {

        // checking character on left
        if (column - 1 >= 0) {
            if (puzzle[countIndex][column - 1] == '+' ||
                puzzle[countIndex][column - 1] == '-') {

                puzzle[countIndex][column] = '-';
            }
        }
        // checking character on right
        if (column + 1 <= (puzzle.size() - 1)) {
            if (puzzle[countIndex][column + 1] == '+' ||
                puzzle[countIndex][column + 1] == '-') {

                puzzle[countIndex][column] = '-';
            }
        }

        // next character
        countIndex++;
    }
}