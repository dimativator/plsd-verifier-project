fun main() {
    var arg10 : List<List<Int>> = mutableListOf(mutableListOf(5, 9, 3), mutableListOf(4, 1, 6), mutableListOf(7, 8, 2))
    var arg11 : Int = 1
    var x1 : List<Int> = minpath(arg10, arg11);
    var v1 : List<Int> = mutableListOf(1);
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20 : List<List<Int>> = mutableListOf(mutableListOf(1, 2, 3, 4), mutableListOf(5, 6, 7, 8), mutableListOf(9, 10, 11, 12), mutableListOf(13, 14, 15, 16))
    var arg21 : Int = 4
    var x2 : List<Int> = minpath(arg20, arg21);
    var v2 : List<Int> = mutableListOf(1, 2, 1, 2);
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30 : List<List<Int>> = mutableListOf(mutableListOf(6, 4, 13, 10), mutableListOf(5, 7, 12, 1), mutableListOf(3, 16, 11, 15), mutableListOf(8, 14, 9, 2))
    var arg31 : Int = 7
    var x3 : List<Int> = minpath(arg30, arg31);
    var v3 : List<Int> = mutableListOf(1, 10, 1, 10, 1, 10, 1);
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40 : List<List<Int>> = mutableListOf(mutableListOf(8, 14, 9, 2), mutableListOf(6, 4, 13, 15), mutableListOf(5, 7, 1, 12), mutableListOf(3, 10, 11, 16))
    var arg41 : Int = 5
    var x4 : List<Int> = minpath(arg40, arg41);
    var v4 : List<Int> = mutableListOf(1, 7, 1, 7, 1);
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50 : List<List<Int>> = mutableListOf(mutableListOf(11, 8, 7, 2), mutableListOf(5, 16, 14, 4), mutableListOf(9, 3, 15, 6), mutableListOf(12, 13, 10, 1))
    var arg51 : Int = 9
    var x5 : List<Int> = minpath(arg50, arg51);
    var v5 : List<Int> = mutableListOf(1, 6, 1, 6, 1, 6, 1, 6, 1);
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60 : List<List<Int>> = mutableListOf(mutableListOf(12, 13, 10, 1), mutableListOf(9, 3, 15, 6), mutableListOf(5, 16, 14, 4), mutableListOf(11, 8, 7, 2))
    var arg61 : Int = 12
    var x6 : List<Int> = minpath(arg60, arg61);
    var v6 : List<Int> = mutableListOf(1, 6, 1, 6, 1, 6, 1, 6, 1, 6, 1, 6);
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70 : List<List<Int>> = mutableListOf(mutableListOf(2, 7, 4), mutableListOf(3, 1, 5), mutableListOf(6, 8, 9))
    var arg71 : Int = 8
    var x7 : List<Int> = minpath(arg70, arg71);
    var v7 : List<Int> = mutableListOf(1, 3, 1, 3, 1, 3, 1, 3);
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }

    var arg80 : List<List<Int>> = mutableListOf(mutableListOf(6, 1, 5), mutableListOf(3, 8, 9), mutableListOf(2, 7, 4))
    var arg81 : Int = 8
    var x8 : List<Int> = minpath(arg80, arg81);
    var v8 : List<Int> = mutableListOf(1, 5, 1, 5, 1, 5, 1, 5);
    if (x8 != v8) {
        throw Exception("Exception -- test case 8 did not pass. x8 = " + x8)
    }

    var arg90 : List<List<Int>> = mutableListOf(mutableListOf(1, 2), mutableListOf(3, 4))
    var arg91 : Int = 10
    var x9 : List<Int> = minpath(arg90, arg91);
    var v9 : List<Int> = mutableListOf(1, 2, 1, 2, 1, 2, 1, 2, 1, 2);
    if (x9 != v9) {
        throw Exception("Exception -- test case 9 did not pass. x9 = " + x9)
    }

    var arg100 : List<List<Int>> = mutableListOf(mutableListOf(1, 3), mutableListOf(3, 2))
    var arg101 : Int = 10
    var x10 : List<Int> = minpath(arg100, arg101);
    var v10 : List<Int> = mutableListOf(1, 3, 1, 3, 1, 3, 1, 3, 1, 3);
    if (x10 != v10) {
        throw Exception("Exception -- test case 10 did not pass. x10 = " + x10)
    }


}

