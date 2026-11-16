fun main() {
    var arg10 : List<Int> = mutableListOf(2, 4, 1, 3, 5, 7, 0)
    var x1 : List<Int?> = largestSmallestIntegers(arg10);
    var v1 : List<Int?> = mutableListOf(null, 1);
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20 : List<Int> = mutableListOf(1, 3, 2, 4, 5, 6, -2)
    var x2 : List<Int?> = largestSmallestIntegers(arg20);
    var v2 : List<Int?> = mutableListOf(-2, 1);
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30 : List<Int> = mutableListOf(4, 5, 3, 6, 2, 7, -7)
    var x3 : List<Int?> = largestSmallestIntegers(arg30);
    var v3 : List<Int?> = mutableListOf(-7, 2);
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40 : List<Int> = mutableListOf(7, 3, 8, 4, 9, 2, 5, -9)
    var x4 : List<Int?> = largestSmallestIntegers(arg40);
    var v4 : List<Int?> = mutableListOf(-9, 2);
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50 : List<Int> = mutableListOf()
    var x5 : List<Int?> = largestSmallestIntegers(arg50);
    var v5 : List<Int?> = mutableListOf(null, null);
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60 : List<Int> = mutableListOf(0)
    var x6 : List<Int?> = largestSmallestIntegers(arg60);
    var v6 : List<Int?> = mutableListOf(null, null);
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70 : List<Int> = mutableListOf(-1, -3, -5, -6)
    var x7 : List<Int?> = largestSmallestIntegers(arg70);
    var v7 : List<Int?> = mutableListOf(-1, null);
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }

    var arg80 : List<Int> = mutableListOf(-1, -3, -5, -6, 0)
    var x8 : List<Int?> = largestSmallestIntegers(arg80);
    var v8 : List<Int?> = mutableListOf(-1, null);
    if (x8 != v8) {
        throw Exception("Exception -- test case 8 did not pass. x8 = " + x8)
    }

    var arg90 : List<Int> = mutableListOf(-6, -4, -4, -3, 1)
    var x9 : List<Int?> = largestSmallestIntegers(arg90);
    var v9 : List<Int?> = mutableListOf(-3, 1);
    if (x9 != v9) {
        throw Exception("Exception -- test case 9 did not pass. x9 = " + x9)
    }

    var arg100 : List<Int> = mutableListOf(-6, -4, -4, -3, -100, 1)
    var x10 : List<Int?> = largestSmallestIntegers(arg100);
    var v10 : List<Int?> = mutableListOf(-3, 1);
    if (x10 != v10) {
        throw Exception("Exception -- test case 10 did not pass. x10 = " + x10)
    }


}

