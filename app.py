import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from puzzle.utils import slice_image, is_solvable
from puzzle.solver import solve_puzzle
from PIL import Image

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['UPLOAD_FOLDER'] = 'static/tiles'

# Make sure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)

def tiles_to_matrix(tiles):
    # Convert flat list to 3x3 matrix
    return [list(tiles[i*3:(i+1)*3]) for i in range(3)]

@app.route('/', methods=['GET'])
def index():
    # If no puzzle in session, display upload page
    puzzle = session.get('puzzle')
    tiles = session.get('tiles')
    return render_template('index.html', puzzle=tiles, solvable=session.get('solvable', True))

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return redirect(url_for('index'))
    file = request.files['image']
    if file.filename == '':
        return redirect(url_for('index'))

    # Clear previous tiles
    for f in os.listdir(app.config['UPLOAD_FOLDER']):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], f))

    # Save original image temporarily
    filename = str(uuid.uuid4()) + ".png"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Slice image into 3x3 tiles
    tiles_filenames = slice_image(filepath, app.config['UPLOAD_FOLDER'])

    # Create puzzle initial state as tuple
    puzzle = tuple(range(1, 9)) + (0,)  # goal state initially

    # Save puzzle and tiles in session
    session['puzzle'] = puzzle
    session['tiles'] = tiles_filenames
    session['image_path'] = filename
    session['solved'] = False

    # Check solvability
    session['solvable'] = is_solvable(puzzle)

    # Remove original full image after slicing
    os.remove(filepath)

    return redirect(url_for('index'))

@app.route('/shuffle', methods=['POST'])
def shuffle():
    import random
    puzzle = list(session.get('puzzle', GOAL_STATE))
    # Shuffle until solvable and not equal to goal
    while True:
        random.shuffle(puzzle)
        if is_solvable(puzzle) and tuple(puzzle) != GOAL_STATE:
            break
    session['puzzle'] = tuple(puzzle)
    session['solvable'] = True
    return jsonify({'puzzle': puzzle})

@app.route('/move', methods=['POST'])
def move():
    data = request.json
    pos = data.get('pos')  # index 0-8 of tile to move
    puzzle = list(session.get('puzzle', GOAL_STATE))

    # Find blank index
    blank_index = puzzle.index(0)

    # Check if pos is adjacent to blank
    adjacents = {
        0: [1, 3],
        1: [0, 2, 4],
        2: [1, 5],
        3: [0, 4, 6],
        4: [1, 3, 5, 7],
        5: [2, 4, 8],
        6: [3, 7],
        7: [4, 6, 8],
        8: [5, 7]
    }

    if pos in adjacents[blank_index]:
        puzzle[blank_index], puzzle[pos] = puzzle[pos], puzzle[blank_index]
        session['puzzle'] = tuple(puzzle)
        session['solvable'] = is_solvable(puzzle)
        if session['puzzle'] == GOAL_STATE:
            session['solved'] = True
        else:
            session['solved'] = False
        return jsonify({'puzzle': puzzle, 'solvable': True, 'solved' : session['solved']})
    else:
        return jsonify({'error': 'Invalid move'}), 400

@app.route('/solve', methods=['GET'])
def solve():
    puzzle = session.get('puzzle', GOAL_STATE)
    path = solve_puzzle(puzzle)
    # Return list of states for front-end animation
    return jsonify({'solution': path})

if __name__ == '__main__':
    app.run(debug=True)
