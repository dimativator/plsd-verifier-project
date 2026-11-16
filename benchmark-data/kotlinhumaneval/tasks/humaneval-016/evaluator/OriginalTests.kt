fun main() {
    var arg00: String = ""
    var x0: Int = countDistinctCharacters(arg00)
    var v0: Int = 0
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: String = "abcde"
    var x1: Int = countDistinctCharacters(arg10)
    var v1: Int = 5
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: String = "abcdecadeCADE"
    var x2: Int = countDistinctCharacters(arg20)
    var v2: Int = 5
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: String = "aaaaAAAAaaaa"
    var x3: Int = countDistinctCharacters(arg30)
    var v3: Int = 1
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: String = "Jerry jERRY JeRRRY"
    var x4: Int = countDistinctCharacters(arg40)
    var v4: Int = 5
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }


}

