fun main() {
    var arg00: String = "TEST"
    var x0: String = encode(arg00)
    var v0: String = "tgst"
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: String = "Mudasir"
    var x1: String = encode(arg10)
    var v1: String = "mWDCSKR"
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: String = "YES"
    var x2: String = encode(arg20)
    var v2: String = "ygs"
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: String = "This is a message"
    var x3: String = encode(arg30)
    var v3: String = "tHKS KS C MGSSCGG"
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: String = "I DoNt KnOw WhAt tO WrItE"
    var x4: String = encode(arg40)
    var v4: String = "k dQnT kNqW wHcT Tq wRkTg"
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }


}

