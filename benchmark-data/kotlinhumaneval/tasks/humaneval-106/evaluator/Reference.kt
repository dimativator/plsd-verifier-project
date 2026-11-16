fun moveOneBall(arr: List<Int>): Boolean {
    if (arr.isEmpty()) {
        return true
    }

    var pivotCount = 0
    var pivotIndex = -1
    for (i in 1 until arr.size) {
        if (arr[i] < arr[i - 1]) {
            pivotCount++
            pivotIndex = i
        }
    }

    if (pivotCount > 1) {
        return false
    }
    if (pivotCount == 0) {
        return true
    }

    return arr.slice(0 until pivotIndex).sorted() ==
            arr.slice(0 until pivotIndex) &&
            arr.slice(pivotIndex until arr.size).sorted() ==
            arr.slice(pivotIndex until arr.size) &&
            arr.last() <= arr.first()
}

