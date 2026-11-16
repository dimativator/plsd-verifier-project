fun minpath(grid : List<List<Int>>, k : Int) : List<Int> {
    val n = grid.size
    var bestPath = List(k) { Int.MAX_VALUE }

    fun dfs(x: Int, y: Int, step: Int, path: MutableList<Int>) {
        if (step == k) {
            for (i in 0 until k) {
                if (path[i] < bestPath[i]) {
                    bestPath = path.toList()
                    break
                } else if (path[i] > bestPath[i]) break
            }
            return
        }

        val directions = listOf(-1 to 0, 1 to 0, 0 to -1, 0 to 1) // Up, down, left, right
        for ((dx, dy) in directions) {
            val newX = x + dx
            val newY = y + dy
            if (newX in 0 until n && newY in 0 until n) {
                path.add(grid[newX][newY])
                dfs(newX, newY, step + 1, path)
                path.removeAt(path.lastIndex) // Backtrack
            }
        }
    }

    for (i in 0 until n) {
        for (j in 0 until n) {
            dfs(i, j, 1, mutableListOf(grid[i][j]))
        }
    }

    return bestPath
}

