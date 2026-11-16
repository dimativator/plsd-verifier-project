fun main() {
    var arg00: List<Int> = mutableListOf(2, 1, 1, 4, 5, 8, 2, 3)
    var x0: List<String> = byLength(arg00)
    var v0: List<String> = mutableListOf("Eight", "Five", "Four", "Three", "Two", "Two", "One", "One")
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
