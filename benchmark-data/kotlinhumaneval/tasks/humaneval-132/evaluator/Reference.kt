fun canArrange(arr : List<Int>) : Int {
    for (i in (1 until arr.size).reversed()) {
        if (arr[i] < arr[i - 1]) {
            return i
        }
    }
    return -1
}

