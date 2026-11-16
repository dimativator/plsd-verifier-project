fun main() {
    var arg00: Int = 5
    var x0: Int = fib4(arg00)
    var v0: Int = 4
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: Int = 8
    var x1: Int = fib4(arg10)
    var v1: Int = 28
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: Int = 10
    var x2: Int = fib4(arg20)
    var v2: Int = 104
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: Int = 12
    var x3: Int = fib4(arg30)
    var v3: Int = 386
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }


}

