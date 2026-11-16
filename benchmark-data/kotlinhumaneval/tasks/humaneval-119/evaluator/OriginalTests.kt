fun main() {
    var arg00 : List<Int> = mutableListOf(1, -2, -3, 41, 57, 76, 87, 88, 99)
    var arg01 : Int = 3
    var x0 : Int = addElements(arg00, arg01);
    var v0 : Int = -4;
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10 : List<Int> = mutableListOf(111, 121, 3, 4000, 5, 6)
    var arg11 : Int = 2
    var x1 : Int = addElements(arg10, arg11);
    var v1 : Int = 0;
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20 : List<Int> = mutableListOf(11, 21, 3, 90, 5, 6, 7, 8, 9)
    var arg21 : Int = 4
    var x2 : Int = addElements(arg20, arg21);
    var v2 : Int = 125;
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30 : List<Int> = mutableListOf(111, 21, 3, 4000, 5, 6, 7, 8, 9)
    var arg31 : Int = 4
    var x3 : Int = addElements(arg30, arg31);
    var v3 : Int = 24;
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40 : List<Int> = mutableListOf(1)
    var arg41 : Int = 1
    var x4 : Int = addElements(arg40, arg41);
    var v4 : Int = 1;
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }


}

