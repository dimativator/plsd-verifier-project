fun main() {
    var arg10: String = "1"
    var arg11: String = "1"
    var x1: String = stringXor(arg10, arg11)
    var v1: String = "0"
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: String = "0101"
    var arg21: String = "0000"
    var x2: String = stringXor(arg20, arg21)
    var v2: String = "0101"
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }
}

