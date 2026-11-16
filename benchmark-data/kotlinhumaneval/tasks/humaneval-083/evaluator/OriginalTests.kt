fun main() {
    var arg00: String = "Hi"
    var x0: String = antiShuffle(arg00)
    var v0: String = "Hi"
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: String = "hello"
    var x1: String = antiShuffle(arg10)
    var v1: String = "ehllo"
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: String = "number"
    var x2: String = antiShuffle(arg20)
    var v2: String = "bemnru"
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: String = "abcd"
    var x3: String = antiShuffle(arg30)
    var v3: String = "abcd"
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: String = "Hello World!!!"
    var x4: String = antiShuffle(arg40)
    var v4: String = "Hello !!!Wdlor"
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50: String = ""
    var x5: String = antiShuffle(arg50)
    var v5: String = ""
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60: String = "Hi. My name is Mister Robot. How are you?"
    var x6: String = antiShuffle(arg60)
    var v6: String = ".Hi My aemn is Meirst .Rboot How aer ?ouy"
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }


}

