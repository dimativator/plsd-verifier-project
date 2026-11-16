fun main() {
    var arg00: List<Int> = mutableListOf()
    var x0: Int = countNums(arg00);
    var v0: Int = 0;
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: List<Int> = mutableListOf(-1, -2, 0)
    var x1: Int = countNums(arg10);
    var v1: Int = 0;
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: List<Int> = mutableListOf(1, 1, 2, -2, 3, 4, 5)
    var x2: Int = countNums(arg20);
    var v2: Int = 6;
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: List<Int> = mutableListOf(1, 6, 9, -6, 0, 1, 5)
    var x3: Int = countNums(arg30);
    var v3: Int = 5;
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: List<Int> = mutableListOf(1, 100, 98, -7, 1, -1)
    var x4: Int = countNums(arg40);
    var v4: Int = 4;
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50: List<Int> = mutableListOf(12, 23, 34, -45, -56, 0)
    var x5: Int = countNums(arg50);
    var v5: Int = 5;
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60: List<Int> = mutableListOf(0, 1)
    var x6: Int = countNums(arg60);
    var v6: Int = 1;
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70: List<Int> = mutableListOf(1)
    var x7: Int = countNums(arg70);
    var v7: Int = 1;
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }


}

