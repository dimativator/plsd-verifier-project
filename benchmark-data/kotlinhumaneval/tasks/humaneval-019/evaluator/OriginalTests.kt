fun main() {
    var arg00: String = ""
    var x0: String = sortNumbers(arg00)
    var v0: String = ""
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: String = "three"
    var x1: String = sortNumbers(arg10)
    var v1: String = "three"
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: String = "three five nine"
    var x2: String = sortNumbers(arg20)
    var v2: String = "three five nine"
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: String = "five zero four seven nine eight"
    var x3: String = sortNumbers(arg30)
    var v3: String = "zero four five seven eight nine"
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: String = "six five four three two one zero"
    var x4: String = sortNumbers(arg40)
    var v4: String = "zero one two three four five six"
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }


}

