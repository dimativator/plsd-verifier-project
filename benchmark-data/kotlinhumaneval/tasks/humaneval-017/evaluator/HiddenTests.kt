fun main() {
    var arg10: String = "o o o o"
    var x1: List<Any> = parseMusic(arg10)
    var v1: List<Any> = mutableListOf(4, 4, 4, 4)
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: String = ".| .| .| .|"
    var x2: List<Any> = parseMusic(arg20)
    var v2: List<Any> = mutableListOf(1, 1, 1, 1)
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: String = "o| o| .| .| o o o o"
    var x3: List<Any> = parseMusic(arg30)
    var v3: List<Any> = mutableListOf(2, 2, 1, 1, 4, 4, 4, 4)
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: String = "o| .| o| .| o o| o o|"
    var x4: List<Any> = parseMusic(arg40)
    var v4: List<Any> = mutableListOf(2, 1, 2, 1, 4, 2, 4, 2)
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }


}

