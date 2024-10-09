# Crossword Puzzle Solver Documentation

This document provides an overview of the functions in the crossword puzzle solver implemented in C++. The solver uses recursion to place words into a predefined crossword grid.

## Functions Overview

### 1. `readFile`
- **Purpose:** Reads a crossword puzzle and a list of words from a specified text file.
- **Parameters:**
  - `fileName`: The name of the file containing the puzzle and words.
  - `puzzle`: A 2D vector where the crossword puzzle will be stored.
  - `wordList`: A vector where the words will be stored.
- **Return:** This function does not return anything. It modifies the `puzzle` and `wordList` vectors in place.

### 2. `printCrosswordPuzzle`
- **Purpose:** Displays the crossword puzzle on the console.
- **Parameters:**
  - `puzzle`: The 2D vector representing the crossword puzzle.
- **Return:** This function does not return anything. It simply prints the puzzle to the console.

### 3. `solveCrosswordPuzzle`
- **Purpose:** Initiates the crossword puzzle-solving process.
- **Parameters:**
  - `puzzle`: The current state of the crossword puzzle.
  - `wordList`: A list of words to be placed in the puzzle.
- **Return:** This function does not return anything. It serves as an entry point to start the solving process.

### 4. `utilSolveCrosswordPuzzle`
- **Purpose:** Performs the actual recursive solving of the puzzle.
- **Parameters:**
  - `puzzle`: The current state of the crossword puzzle.
  - `wordList`: The list of remaining words to place.
  - `row`: The current row index to consider for placement.
  - `column`: The current column index to consider for placement.
- **Return:** This function returns `true` if the puzzle can be solved by placing all the words. If no valid solution is found, it returns `false`. The `puzzle` and `wordList` are modified during the process.

### 5. `findIndicesToPlaceWord`
- **Purpose:** Finds the first available position in the puzzle where a word can be placed.
- **Parameters:**
  - `puzzle`: The current state of the crossword puzzle.
  - `row`: The starting row index.
  - `column`: The starting column index.
- **Return:** Returns a pair of integers representing the row and column index of the first available position. If no available position is found, it returns a special value like `(-1, -1)`.

### 6. `isLeftRight`
- **Purpose:** Determines if a word can be placed horizontally.
- **Parameters:**
  - `puzzle`: The current state of the crossword puzzle.
  - `row`: The row index to check.
  - `column`: The column index to check.
- **Return:** Returns `true` if a word can be placed from left to right at the given position, otherwise returns `false`.

### 7. `isTopBottom`
- **Purpose:** Determines if a word can be placed vertically.
- **Parameters:**
  - `puzzle`: The current state of the crossword puzzle.
  - `row`: The row index to check.
  - `column`: The column index to check.
- **Return:** Returns `true` if a word can be placed from top to bottom at the given position, otherwise returns `false`.

### 8. `leftBoundIndex` and `rightBoundIndex`
- **Purpose:** Find the leftmost and rightmost bounds where a word can be placed in a row.
- **Parameters:**
  - `puzzle`: The current state of the crossword puzzle.
  - `row`: The row index.
  - `column`: The starting column index.
- **Return:** Returns the index of the leftmost or rightmost boundary where a word can be placed in the row. The boundary is identified by encountering a '+' character or the edge of the puzzle.

### 9. `topBoundIndex` and `bottomBoundIndex`
- **Purpose:** Find the uppermost and bottommost bounds where a word can be placed in a column.
- **Parameters:**
  - `puzzle`: The current state of the crossword puzzle.
  - `row`: The starting row index.
  - `column`: The column index.
- **Return:** Returns the index of the topmost or bottommost boundary where a word can be placed in the column. The boundary is identified by encountering a '+' character or the edge of the puzzle.

### 10. `placeLeftRight` and `placeTopBottom`
- **Purpose:** Place a word horizontally or vertically in the puzzle.
- **Parameters:**
  - `puzzle`: The current state of the crossword puzzle.
  - `wordList`: The list of remaining words.
  - `leftIndex` or `topIndex`: The starting index for placement.
  - `row` or `column`: The row or column index for placement.
  - `size`: The size of the word to be placed.
- **Return:** Returns `true` if the word is successfully placed in the puzzle. If placement fails, it returns `false`.

### 11. `eraseWordFromList`
- **Purpose:** Removes a specified word from the list of words.
- **Parameters:**
  - `wordList`: The list of words.
  - `word`: The word to remove.
- **Return:** This function does not return anything. It modifies the `wordList` by removing the specified word.

### 12. `removeLeftRightWord` and `removeTopBottomWord`
- **Purpose:** Removes a word placed horizontally or vertically from the puzzle.
- **Parameters:**
  - `puzzle`: The current state of the crossword puzzle.
  - `word`: The word to remove.
  - `row`, `leftIndex` or `column`, `topIndex