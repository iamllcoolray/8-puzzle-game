from PIL import Image

def slice_image(image_path, output_folder):
    """
    Slice the image into 3x3 tiles, save tiles 1.png to 8.png,
    and 0.png for the blank tile.
    Returns list of filenames in order [1,...,8,0].
    """
    im = Image.open(image_path)
    width, height = im.size
    tile_width = width // 3
    tile_height = height // 3

    filenames = []
    tile_num = 1
    for row in range(3):
        for col in range(3):
            box = (col * tile_width, row * tile_height,
                   (col + 1) * tile_width, (row + 1) * tile_height)
            tile = im.crop(box)
            # The last tile is blank
            if row == 2 and col == 2:
                # Save a blank white tile for the empty space
                blank_tile = Image.new('RGB', (tile_width, tile_height), color='white')
                blank_tile.save(f"{output_folder}/0.png")
                filenames.append('0.png')
            else:
                filename = f"{tile_num}.png"
                tile.save(f"{output_folder}/{filename}")
                filenames.append(filename)
                tile_num += 1
    return filenames

def is_solvable(puzzle):
    """
    Check if a puzzle is solvable
    puzzle: tuple/list of length 9 with numbers 0-8 (0 is blank)
    """
    inv_count = 0
    puzzle_list = [x for x in puzzle if x != 0]
    for i in range(len(puzzle_list)):
        for j in range(i + 1, len(puzzle_list)):
            if puzzle_list[i] > puzzle_list[j]:
                inv_count += 1
    # For 3x3 puzzle, if inversions count is even, puzzle solvable
    return inv_count % 2 == 0
