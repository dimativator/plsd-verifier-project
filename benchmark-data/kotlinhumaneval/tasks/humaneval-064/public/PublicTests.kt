fun main() {
    var arg00: String = "5 apples and 6 oranges"
    var arg01: Int = 19
    var x0: Int = fruitDistribution(arg00, arg01)
    var v0: Int = 8
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
