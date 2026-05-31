from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import time
import sys

app = Flask(__name__)          # Buat instance aplikasi Flask
CORS(app)                      # Izinkan request lintas-origin dari browser

# Increase recursion limit for large mazes
sys.setrecursionlimit(10000)

# RANDOM MAZE GENERATOR

def generate_random_maze(rows, cols, density=0.3):
    maze = []
    for r in range(rows):
        row = []
        for c in range(cols):
            # Jika angka acak < density, tembok (1), selain itu, jalan (0)
            if random.random() < density:
                row.append(1)
            else:
                row.append(0)
        maze.append(row)
    maze[0][0] = 0                    # Paksa titik START selalu jalan
    maze[rows - 1][cols - 1] = 0     # Paksa titik END selalu jalan
    return maze


# ALGORITHM 1 — RECURSIVE BACKTRACKING
#Eksplorasi 4 arah secara acak
#Iterative (explicit stack): hindari stack overflow
#Backtrack dengan pop dari stack

class RecursiveBacktracking:

    PATH_COLOR = "#1E90FF" 

    def __init__(self, maze):
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])

    def solve(self):
        start_time = time.time()

        visited = set()
        visited.add((0, 0))

        # Stack menyimpan: (r, c, list arah yang belum dicoba)
        # 4 arah diacak tiap node baru untuk path diversity
        explicit_stack = [(0, 0, self._shuffled_dirs())]

        path_found = []
        found = False
        max_stack_depth = 0

        while explicit_stack:
            if len(explicit_stack) > max_stack_depth:
                max_stack_depth = len(explicit_stack)

            r, c, remaining_dirs = explicit_stack[-1]

            # Cek apakah sudah sampai tujuan
            if r == self.rows - 1 and c == self.cols - 1:
                found = True
                # Path direkonstruksi langsung dari explicit stack
                path_found = [[node[0], node[1]] for node in explicit_stack]
                break

            if not remaining_dirs:
                # Semua arah sudah dicoba maka akan dihapus/kembali ke node sebelumnya
                explicit_stack.pop()
                continue

            dr, dc = remaining_dirs.pop(0)
            nr, nc = r + dr, c + dc

            if (0 <= nr < self.rows and 0 <= nc < self.cols
                    and self.maze[nr][nc] == 0
                    and (nr, nc) not in visited):
                visited.add((nr, nc))
                # Masuk ke node baru dengan arah baru yang diacak
                explicit_stack.append((nr, nc, self._shuffled_dirs()))

        end_time = time.time()
        exec_time = (end_time - start_time) * 1000

        return {
            "found": found,
            "path": path_found,
            "path_length": len(path_found),
            "path_color": self.PATH_COLOR,     
            "time_ms": round(exec_time, 4),
            "max_recursion_depth": max_stack_depth,
            "algorithm": "Recursive Backtracking"
        }

    def _shuffled_dirs(self):
        """4 arah diacak menghasilkan path yang beragam tiap run."""
        dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(dirs)
        return dirs

# ALGORITHM 2 — BINARY TREE
#Ekspansi level-by-level menggunakan queue
#Tiap node di queue membawa salinan path lengkap
#Dead-end ditandai, grandparent direexplore

class BinaryTree:

    PATH_COLOR = "#FF4444"

    def __init__(self, maze):
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])

        # Arah ekspansi: kanan & bawah sebagai prioritas utama,
        # kiri & atas sebagai fallback saat dead-end
        self.PRIMARY_DIRS   = [(0, 1), (1, 0)]           # kanan, bawah
        self.SECONDARY_DIRS = [(0, -1), (-1, 0)]         # kiri, atas

    def solve(self):
        from collections import deque

        start_time = time.time()

        visited = set()
        visited.add((0, 0))
        dead_end_nodes = set()

        # Queue menyimpan: (r, c, path_lengkap)
        # Setiap elemen queue membawa salinan path sendiri
        queue = deque()
        queue.append((0, 0, [(0, 0)]))

        found = False
        final_path = []
        max_depth = 0

        while queue:
            r, c, current_path = queue.popleft()

            if len(current_path) > max_depth:
                max_depth = len(current_path)

            # Cek apakah sudah sampai tujuan
            if r == self.rows - 1 and c == self.cols - 1:
                found = True
                # Path sudah tersimpan utuh di current_path
                final_path = [[node[0], node[1]] for node in current_path]
                break

            # Ekspansi ke arah prioritas (kanan & bawah) terlebih dulu,
            # lalu fallback ke kiri & atas jika diperlukan
            all_dirs = self.PRIMARY_DIRS + self.SECONDARY_DIRS
            expanded = False

            for dr, dc in all_dirs:
                nr, nc = r + dr, c + dc
                if (0 <= nr < self.rows and 0 <= nc < self.cols
                        and self.maze[nr][nc] == 0
                        and (nr, nc) not in visited
                        and (nr, nc) not in dead_end_nodes):
                    visited.add((nr, nc))
                    # Buat salinan path baru dengan node berikutnya
                    new_path = current_path + [(nr, nc)]
                    queue.append((nr, nc, new_path))
                    expanded = True

            # Dead-end: tandai node ini, coba ulang dari grandparent
            if not expanded:
                dead_end_nodes.add((r, c))

                if len(current_path) >= 2:
                    grandparent = current_path[-2]
                    gr, gc = grandparent
                    # Re-explore grandparent ke arah yang belum dicoba
                    for dr, dc in all_dirs:
                        nr, nc = gr + dr, gc + dc
                        if (0 <= nr < self.rows and 0 <= nc < self.cols
                                and self.maze[nr][nc] == 0
                                and (nr, nc) not in visited
                                and (nr, nc) not in dead_end_nodes):
                            visited.add((nr, nc))
                            # Ganti node terakhir di path dengan alternatif
                            new_path = current_path[:-1] + [(nr, nc)]
                            queue.append((nr, nc, new_path))
                            break

        end_time = time.time()
        exec_time = (end_time - start_time) * 1000

        return {
            "found": found,
            "path": final_path,
            "path_length": len(final_path),
            "path_color": self.PATH_COLOR,          # << MERAH
            "time_ms": round(exec_time, 4),
            "max_recursion_depth": max_depth,
            "algorithm": "Binary Tree"
        }

# HELPER — tentukan shortest path dari 2 hasil solve

def pick_shortest(result_rb, result_bt):
    """
    Bandingkan path_length kedua algoritma.
    Return dict berisi info algoritma mana yang menghasilkan path lebih pendek,
    beserta warnanya untuk ditampilkan di frontend.
    """
    # Jika algoritma gagal menemukan path, panjangnya dianggap tak terhingga
    len_rb = result_rb.get("path_length", float("inf")) if result_rb.get("found") else float("inf")
    len_bt = result_bt.get("path_length", float("inf")) if result_bt.get("found") else float("inf")

    # Pemenang = path lebih pendek; jika sama, Recursive Backtracking dipilih
    if len_rb <= len_bt:
        winner = "Recursive Backtracking"
        color  = RecursiveBacktracking.PATH_COLOR 
    else:
        winner = "Binary Tree"
        color  = BinaryTree.PATH_COLOR             

    return {
        "shortest_algorithm": winner,
        "shortest_color": color,
        "recursive_backtracking_length": len_rb if len_rb != float("inf") else None,
        "binary_tree_length": len_bt if len_bt != float("inf") else None,
    }

# ROUTES

@app.route("/status")
def status():
    return jsonify({
        "status": "online",
        "message": "Maze Solver Backend - 2 Algorithms",
        "algorithms": [
            "recursive_backtracking",
            "binary_tree"
        ],
        "path_colors": {
            "recursive_backtracking": RecursiveBacktracking.PATH_COLOR,
            "binary_tree": BinaryTree.PATH_COLOR                         
        }
    })


@app.route("/solve", methods=["POST"])
def solve_maze():
    """
    Solve maze dengan 1 algoritma pilihan.
    Response menyertakan 'path_color' untuk pewarnaan di frontend.
    """
    try:
        data = request.get_json()
        maze = data["maze"]
        algorithm = data.get("algorithm", "recursive_backtracking")  # Default: Recursive Backtracking

        # Peta nama algoritma ke kelasnya masing-masing
        solvers = {
            "recursive_backtracking": RecursiveBacktracking,
            "binary_tree": BinaryTree,
        }

        if algorithm not in solvers:  # Validasi nama algoritma
            return jsonify({
                "error": f"Algorithm '{algorithm}' tidak ditemukan. Pilih dari: {list(solvers.keys())}"
            }), 400

        solver = solvers[algorithm](maze)  # Buat instance solver sesuai pilihan
        result = solver.solve()

        return jsonify({
            **result,
            "maze": maze
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/solve/all", methods=["POST"])
def solve_all():
    """
    Jalankan kedua algoritma sekaligus dan bandingkan hasilnya.
    Response menyertakan:
      - hasil masing-masing algoritma (dengan path_color)
      - info shortest path (algoritma mana yang menang + warnanya)
    """
    try:
        data = request.get_json()
        maze = data["maze"]

        # Jalankan Recursive Backtracking
        result_rb = RecursiveBacktracking(maze).solve()

        # Jalankan Binary Tree
        result_bt = BinaryTree(maze).solve()

        # Tentukan shortest path
        shortest_info = pick_shortest(result_rb, result_bt)

        return jsonify({
            "maze": maze,
            "comparison": {
                "recursive_backtracking": result_rb,
                "binary_tree": result_bt
            },
            "shortest": shortest_info
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/random", methods=["POST"])
def random_maze():
    """Generate random maze dengan ukuran dan density yang ditentukan."""
    try:
        data = request.get_json()
        rows    = int(data["rows"])       # Jumlah baris
        cols    = int(data["cols"])       # Jumlah kolom
        density = float(data["density"]) # Proporsi tembok (0.0 – 1.0)
        maze = generate_random_maze(rows, cols, density)
        return jsonify({"maze": maze})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# MAIN

if __name__ == "__main__":
    print("=" * 50)
    print(" Maze Solver Backend — 2 Algorithms")
    print(" http://127.0.0.1:5000")
    print("=" * 50)
    print(" Path Colors:")
    print(f"  Recursive Backtracking : {RecursiveBacktracking.PATH_COLOR}  (Biru)")
    print(f"  Binary Tree            : {BinaryTree.PATH_COLOR}  (Merah)")
    print("=" * 50)
    print(" Endpoints:")
    print("  GET  /status")
    print("  POST /random     → generate maze")
    print("  POST /solve      → solve (1 algoritma)")
    print("  POST /solve/all  → bandingkan kedua algoritma")
    print("=" * 50)
    app.run(debug=True)
