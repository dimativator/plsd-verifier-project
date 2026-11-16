fun main() {
    var arg00: List<Int> = mutableListOf(1, 2, 3, 5, 4, 7, 9, 6)
    var x0: Int = smallestChange(arg00)
    var v0: Int = 4
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
