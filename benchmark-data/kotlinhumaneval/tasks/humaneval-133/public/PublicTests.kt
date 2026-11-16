fun main() {
    var arg00 : List<Int> = mutableListOf(2, 4, 1, 3, 5, 7)
    var x0 : List<Int?> = largestSmallestIntegers(arg00);
    var v0 : List<Int?> = mutableListOf(null, 1);
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
