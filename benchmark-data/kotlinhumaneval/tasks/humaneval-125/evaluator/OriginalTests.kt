fun main() {
    var arg00 : List<Int> = mutableListOf(1, 2, 2, -4)
    var x0 : Int? = prodSigns(arg00);
    var v0 : Int? = -9;
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10 : List<Int> = mutableListOf(0, 1)
    var x1 : Int? = prodSigns(arg10);
    var v1 : Int? = 0;
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20 : List<Int> = mutableListOf(1, 1, 1, 2, 3, -1, 1)
    var x2 : Int? = prodSigns(arg20);
    var v2 : Int? = -10;
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30 : List<Int> = mutableListOf()
    var x3 : Int? = prodSigns(arg30);
    var v3 : Int? = null;
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40 : List<Int> = mutableListOf(2, 4, 1, 2, -1, -1, 9)
    var x4 : Int? = prodSigns(arg40);
    var v4 : Int? = 20;
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50 : List<Int> = mutableListOf(-1, 1, -1, 1)
    var x5 : Int? = prodSigns(arg50);
    var v5 : Int? = 4;
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60 : List<Int> = mutableListOf(-1, 1, 1, 1)
    var x6 : Int? = prodSigns(arg60);
    var v6 : Int? = -4;
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70 : List<Int> = mutableListOf(-1, 1, 1, 0)
    var x7 : Int? = prodSigns(arg70);
    var v7 : Int? = 0;
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }


}

