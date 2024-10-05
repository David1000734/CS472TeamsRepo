# Crossword Puzzle Solver Explanation

This document provides an overview of the functions in the crossword puzzle solver implemented in C++. The solver uses recursion to place words into a predefined crossword grid.

## Functions Overview

### 1. `readFile`
- **Purpose:** Reads a crossword puzzle and a list of words from a specified text file.
- **Parameters:**
  - `fileName`: The name of the file containing the puzzle and words.
  - `puzzle`: A 2D vector where the crossword puzzle will be stored.
  - `wordList`: A vector where the words will be stored.

### 2. `printCrosswordPuzzle`
- **Purpose:** Displays the crossword puzzle on the console.
- **Parameters:**
  - `puzzle`: The 2D vector representing the crossword puzzle.

### 3. `solveCrosswordPuzzle`
- **Purpose:** Initiates the crossword puzzle-solving process.
- **Parameters:**
  - `puzzle`: The current state of the crossword puzzle.
  - `wordList`: A list of words to be placed in the puzzle.

### 4. `utilSolveCrosswordPuzzle`
- **Purpose:** Performs the actual recursive solving of the puzzle.
- **Parameters:**
  - `puzzle`: The current state of the crossword puzzle.
  - `wordList`: The list of remaining words to place.
  - `row`: The current row index to consider for placement.
  - `column`: The current column index to consider for placement.

### 5. `findIndicesToPlaceWord`
- **Purpose:** Finds the first available position in the puzzle where a word can be placed.
- **Parameters:**
  - `puzzle`: The current state of the crossword puzzle.
  - `row`: The starting row index.
  - `column`: The starting column index.

### 6. `isLeftRight`
- **Purpose:** Determines if a word can be placed horizontally.
- **Parameters:**
  - `puzzle`: The current state of the crossword puzzle.
  - `row`: The row index to check.
  - `column`: The column index to check.

### 7. `isTopBottom`
- **Purpose:** Determines if a word can be placed vertically.
- **Parameters:**
  - `puzzle`: The current state of the crossword puzzle.
  - `row`: The row index to check.
  - `column`: The column index to check.

### 8. `leftBoundIndex` and `rightBoundIndex`
- **Purpose:** Find the leftmost and rightmost bounds where a word can be placed in a row.
- **Parameters:**
  - `puzzle`: The current state of the crossword puzzle.
  - `row`: The row index.
  - `column`: The starting column index.

### 9. `topBoundIndex` and `bottomBoundIndex`
- **Purpose:** Find the uppermost and bottommost bounds where a word can be placed in a column.
- **Parameters:**
  - `puzzle`: The current state of the crossword puzzle.
  - `row`: The starting row index.
  - `column`: The column index.

### 10. `placeLeftRight` and `placeTopBottom`
- **Purpose:** Place a word horizontally or vertically in the puzzle.
- **Parameters:**
  - `puzzle`: The current state of the crossword puzzle.
  - `wordList`: The list of remaining words.
  - `leftIndex` or `topIndex`: The starting index for placement.
  - `row` or `column`: The row or column index for placement.
  - `size`: The size of the word to be placed.

### 11. `eraseWordFromList`
- **Purpose:** Removes a specified word from the list of words.
- **Parameters:**
  - `wordList`: The list of words.
  - `word`: The word to remove.

### 12. `removeLeftRightWord` and `removeTopBottomWord`
- **Purpose:** Removes a word placed horizontally or vertically from the puzzle.
- **Parameters:**
  - `puzzle`: The current state of the crossword puzzle.
  - `word`: The word to remove.
  - `row`, `leftIndex` or `column`, `topIndex`: Indices for removal.
