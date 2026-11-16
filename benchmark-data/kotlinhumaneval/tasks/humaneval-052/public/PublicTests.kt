fun main() {
    var arg00: Int = 10
    var x0: Int = fib(arg00)
    var v0: Int = 55
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
