fun main() {
    var arg10: List<Int> = mutableListOf(152, 323, 1422, 10)
    var x1: List<Int> = uniqueDigits(arg10);
    var v1: List<Int> = mutableListOf();
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: List<Int> = mutableListOf(12345, 2033, 111, 151)
    var x2: List<Int> = uniqueDigits(arg20);
    var v2: List<Int> = mutableListOf(111, 151);
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: List<Int> = mutableListOf(135, 103, 31)
    var x3: List<Int> = uniqueDigits(arg30);
    var v3: List<Int> = mutableListOf(31, 135);
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }


}

