fun main() {
    var arg00: Int = 2
    var x0: List<Int> = factorize(arg00)
    var v0: List<Int> = mutableListOf(2)
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
