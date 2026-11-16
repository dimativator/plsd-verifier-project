fun main() {
    var arg10 : List<Int> = mutableListOf(1, 4, 9)
    var x1 : Int = sumSquares(arg10);
    var v1 : Int = 14;
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20 : List<Int> = mutableListOf()
    var x2 : Int = sumSquares(arg20);
    var v2 : Int = 0;
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30 : List<Int> = mutableListOf(1, 1, 1, 1, 1, 1, 1, 1, 1)
    var x3 : Int = sumSquares(arg30);
    var v3 : Int = 9;
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40 : List<Int> = mutableListOf(-1, -1, -1, -1, -1, -1, -1, -1, -1)
    var x4 : Int = sumSquares(arg40);
    var v4 : Int = -3;
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50 : List<Int> = mutableListOf(0)
    var x5 : Int = sumSquares(arg50);
    var v5 : Int = 0;
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60 : List<Int> = mutableListOf(-1, -5, 2, -1, -5)
    var x6 : Int = sumSquares(arg60);
    var v6 : Int = -126;
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70 : List<Int> = mutableListOf(-56, -99, 1, 0, -2)
    var x7 : Int = sumSquares(arg70);
    var v7 : Int = 3030;
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }

    var arg80 : List<Int> = mutableListOf(-1, 0, 0, 0, 0, 0, 0, 0, -1)
    var x8 : Int = sumSquares(arg80);
    var v8 : Int = 0;
    if (x8 != v8) {
        throw Exception("Exception -- test case 8 did not pass. x8 = " + x8)
    }

    var arg90 : List<Int> = mutableListOf(-16, -9, -2, 36, 36, 26, -20, 25, -40, 20, -4, 12, -26, 35, 37)
    var x9 : Int = sumSquares(arg90);
    var v9 : Int = -14196;
    if (x9 != v9) {
        throw Exception("Exception -- test case 9 did not pass. x9 = " + x9)
    }

    var arg100 : List<Int> = mutableListOf(-1, -3, 17, -1, -15, 13, -1, 14, -14, -12, -5, 14, -14, 6, 13, 11, 16, 16, 4, 10)
    var x10 : Int = sumSquares(arg100);
    var v10 : Int = -1448;
    if (x10 != v10) {
        throw Exception("Exception -- test case 10 did not pass. x10 = " + x10)
    }


}

