fun main() {
    var arg00 : List<Int> = mutableListOf(1, 11, -1, -11, -12)
    var x0 : List<Int> = orderByPoints(arg00);
    var v0 : List<Int> = mutableListOf(-1, -11, 1, -12, 11);
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10 : List<Int> = mutableListOf(1234, 423, 463, 145, 2, 423, 423, 53, 6, 37, 3457, 3, 56, 0, 46)
    var x1 : List<Int> = orderByPoints(arg10);
    var v1 : List<Int> = mutableListOf(0, 2, 3, 6, 53, 423, 423, 423, 1234, 145, 37, 46, 56, 463, 3457);
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20 : List<Int> = mutableListOf()
    var x2 : List<Int> = orderByPoints(arg20);
    var v2 : List<Int> = mutableListOf();
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30 : List<Int> = mutableListOf(1, -11, -32, 43, 54, -98, 2, -3)
    var x3 : List<Int> = orderByPoints(arg30);
    var v3 : List<Int> = mutableListOf(-3, -32, -98, -11, 1, 2, 43, 54);
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40 : List<Int> = mutableListOf(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)
    var x4 : List<Int> = orderByPoints(arg40);
    var v4 : List<Int> = mutableListOf(1, 10, 2, 11, 3, 4, 5, 6, 7, 8, 9);
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50 : List<Int> = mutableListOf(0, 6, 6, -76, -21, 23, 4)
    var x5 : List<Int> = orderByPoints(arg50);
    var v5 : List<Int> = mutableListOf(-76, -21, 0, 4, 23, 6, 6);
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }


}

