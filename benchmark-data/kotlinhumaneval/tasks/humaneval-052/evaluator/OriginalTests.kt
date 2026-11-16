fun main() {
    var arg00: Int = 10
    var x0: Int = fib(arg00)
    var v0: Int = 55
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: Int = 1
    var x1: Int = fib(arg10)
    var v1: Int = 1
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: Int = 8
    var x2: Int = fib(arg20)
    var v2: Int = 21
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: Int = 11
    var x3: Int = fib(arg30)
    var v3: Int = 89
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: Int = 12
    var x4: Int = fib(arg40)
    var v4: Int = 144
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }


}

