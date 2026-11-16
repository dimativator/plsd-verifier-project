fun maxFill(grid : List<List<Int>>, capacity : Int) : Int {
    val compressedWells = grid.map { row -> row.count { it == 1 } }
    return compressedWells.sumOf { wellSize -> (wellSize + capacity - 1) / capacity }
}

