fun main() {
    var arg00: List<Int> = mutableListOf(1, 5, 2, 3, 4)
    var x0: List<Int> = sortArrayByBinary(arg00);
    var v0: List<Int> = mutableListOf(1, 2, 4, 3, 5);
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: List<Int> = mutableListOf(-2, -3, -4, -5, -6)
    var x1: List<Int> = sortArrayByBinary(arg10);
    var v1: List<Int> = mutableListOf(-4, -2, -6, -5, -3);
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: List<Int> = mutableListOf(1, 0, 2, 3, 4)
    var x2: List<Int> = sortArrayByBinary(arg20);
    var v2: List<Int> = mutableListOf(0, 1, 2, 4, 3);
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: List<Int> = mutableListOf()
    var x3: List<Int> = sortArrayByBinary(arg30);
    var v3: List<Int> = mutableListOf();
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: List<Int> = mutableListOf(2, 5, 77, 4, 5, 3, 5, 7, 2, 3, 4)
    var x4: List<Int> = sortArrayByBinary(arg40);
    var v4: List<Int> = mutableListOf(2, 2, 4, 4, 3, 3, 5, 5, 5, 7, 77);
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50: List<Int> = mutableListOf(3, 6, 44, 12, 32, 5)
    var x5: List<Int> = sortArrayByBinary(arg50);
    var v5: List<Int> = mutableListOf(32, 3, 5, 6, 12, 44);
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60: List<Int> = mutableListOf(2, 4, 8, 16, 32)
    var x6: List<Int> = sortArrayByBinary(arg60);
    var v6: List<Int> = mutableListOf(2, 4, 8, 16, 32);
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70: List<Int> = mutableListOf(2, 4, 8, 16, 32)
    var x7: List<Int> = sortArrayByBinary(arg70);
    var v7: List<Int> = mutableListOf(2, 4, 8, 16, 32);
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }


}

