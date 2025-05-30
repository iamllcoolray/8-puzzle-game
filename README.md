# Assignment 1: 8-Puzzle

## Description

In this assignment, you are required to develop a software application or website (a localhost implementation is
acceptable) that allows users to upload an image. Your program should process the uploaded image and convert
it into a playable 8-puzzle game format. Additionally, you must provide an option to shuffle the puzzle as well as
an option to directly display the optimal solution step-by-step. You are expected to test your program from a
user’s perspective, addressing and resolving any issues to ensure smooth and logical interaction. The image
below shows a common 8-puzzle game. You need to transform the given scrambled configuration into the correct
placement.

For ease of implementation on a computer, we have simplified the above puzzles into numbers and saved them
as the matrix below. Specifically, you may choose to represent the blank space as either 0 or 9.

## Requirements

1. Core algorithm: A\* algorithm is required (60 points). You may choose any rational heuristic (need to explain
   in a report) by yourself. You can deploy multiple algorithms, such as BFS & DFS, to help user understand their
   differences.

2. A user-friendly interface. (40 points)

3. Extra points (20 at most). You may freely add additional, reasonable features to your software or website.
   The grader will evaluate your implementation and assign extra points based on its performance.
   Deliverable

4. A short report/README to explain your assignment. (PDF format)

5. An executable source code.

6. Put all files into one folder and compress this folder to submit.
   Annotations

## Setup

**Python Version 3.13+ (3.13.3 - used)**

Fork the Project and the download the repository.

### Create a Virtual Environment

```
python3 -m venv .venv
source .venv/bin/activate
```

### Install Dependencies

```
python3 -m pip install -r requirements.txt
```

### Run the Project

```
python3 app.py
```
