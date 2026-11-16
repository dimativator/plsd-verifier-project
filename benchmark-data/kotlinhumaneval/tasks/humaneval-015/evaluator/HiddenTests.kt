fun main() {
    var arg10: Int = 3
    var x1: String = stringSequence(arg10)
    var v1: String = "0 1 2 3"
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: Int = 10
    var x2: String = stringSequence(arg20)
    var v2: String = "0 1 2 3 4 5 6 7 8 9 10"
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }


}

