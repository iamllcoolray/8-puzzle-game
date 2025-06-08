document.addEventListener('DOMContentLoaded', () => {
    const puzzleGrid = document.getElementById('puzzle-grid');
    const shuffleBtn = document.getElementById('shuffle-btn');
    const solveBtn = document.getElementById('solve-btn');
    const resetBtn = document.getElementById('reset-btn');
    const message = document.getElementById('message');

    // Move tile if adjacent to blank
    puzzleGrid?.addEventListener('click', async (e) => {
        const tile = e.target.closest('.tile');
        if (!tile || tile.classList.contains('blank')) return;

        const pos = parseInt(tile.dataset.pos);
        try {
            const res = await fetch('/move', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({pos})
            });
            if (!res.ok) {
                const err = await res.json();
                message.textContent = err.error || 'Invalid move';
                return;
            }
            const data = await res.json();
            updateGrid(data.puzzle);
            if (data.solved === true){
                message.textContent = 'Puzzle Solved!';
            }
            else{
                message.textContent = '';
            }
        } catch {
            message.textContent = 'Server error on move';
        }
    });

    shuffleBtn?.addEventListener('click', async () => {
        message.textContent = 'Shuffling...';
        try {
            const res = await fetch('/shuffle', {method: 'POST'});
            const data = await res.json();
            updateGrid(data.puzzle);
            message.textContent = 'Puzzle shuffled.';
        } catch {
            message.textContent = 'Server error on shuffle';
        }
    });

    solveBtn?.addEventListener('click', async () => {
        message.textContent = 'Solving...';
        try {
            const res = await fetch('/solve');
            const data = await res.json();
            const solution = data.solution;
            if (!solution || solution.length === 0) {
                message.textContent = 'No solution found.';
                return;
            }
            await animateSolution(solution);
            updateGrid(data.puzzle);
            message.textContent = 'Puzzle solved!';
        } catch {
            message.textContent = 'Server error on solve';
        }
    });

    resetBtn?.addEventListener('click', async () => {
        try {
            const res = await fetch('/solve');
            const data = await res.json();
            updateGrid(data.puzzle);
            message.textContent = 'Puzzle reset!';
        } catch {
            message.textContent = 'Server error on reset';
        }
    });

    function updateGrid(puzzle) {
        for (let i = 0; i < puzzle.length; i++) {
            const tileDiv = puzzleGrid.children[i];
            const val = puzzle[i];
            if (val === 0) {
                tileDiv.classList.add('blank');
                tileDiv.innerHTML = '';
            } else {
                tileDiv.classList.remove('blank');
                tileDiv.innerHTML = `<img src="/static/tiles/${val}.png" alt="Tile ${val}">`;
            }
        }
    }

    async function animateSolution(solution) {
        for (const state of solution) {
            updateGrid(state);
            await new Promise(r => setTimeout(r, 700));
        }
    }
});
