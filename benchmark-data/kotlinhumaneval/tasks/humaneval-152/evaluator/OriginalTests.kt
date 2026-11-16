fun main() {
    var arg00 : Int = 7
    var x0 : List<Int> = evenOddCount(arg00);
    var v0 : List<Int> = mutableListOf(0, 1);
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10 : Int = -78
    var x1 : List<Int> = evenOddCount(arg10);
    var v1 : List<Int> = mutableListOf(1, 1);
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20 : Int = 3452
    var x2 : List<Int> = evenOddCount(arg20);
    var v2 : List<Int> = mutableListOf(2, 2);
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30 : Int = 346211
    var x3 : List<Int> = evenOddCount(arg30);
    var v3 : List<Int> = mutableListOf(3, 3);
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40 : Int = -345821
    var x4 : List<Int> = evenOddCount(arg40);
    var v4 : List<Int> = mutableListOf(3, 3);
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50 : Int = -2
    var x5 : List<Int> = evenOddCount(arg50);
    var v5 : List<Int> = mutableListOf(1, 0);
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60 : Int = -45347
    var x6 : List<Int> = evenOddCount(arg60);
    var v6 : List<Int> = mutableListOf(2, 3);
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70 : Int = 0
    var x7 : List<Int> = evenOddCount(arg70);
    var v7 : List<Int> = mutableListOf(1, 0);
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }


}

