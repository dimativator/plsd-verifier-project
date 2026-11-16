fun main() {
    var arg00 : Int = 5
    var arg01 : Int = 6
    var arg02 : Int = 10
    var x0 : List<Int> = eat(arg00, arg01, arg02);
    var v0 : List<Int> = mutableListOf(11, 4);
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10 : Int = 4
    var arg11 : Int = 8
    var arg12 : Int = 9
    var x1 : List<Int> = eat(arg10, arg11, arg12);
    var v1 : List<Int> = mutableListOf(12, 1);
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20 : Int = 1
    var arg21 : Int = 10
    var arg22 : Int = 10
    var x2 : List<Int> = eat(arg20, arg21, arg22);
    var v2 : List<Int> = mutableListOf(11, 0);
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30 : Int = 2
    var arg31 : Int = 11
    var arg32 : Int = 5
    var x3 : List<Int> = eat(arg30, arg31, arg32);
    var v3 : List<Int> = mutableListOf(7, 0);
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40 : Int = 4
    var arg41 : Int = 5
    var arg42 : Int = 7
    var x4 : List<Int> = eat(arg40, arg41, arg42);
    var v4 : List<Int> = mutableListOf(9, 2);
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50 : Int = 4
    var arg51 : Int = 5
    var arg52 : Int = 1
    var x5 : List<Int> = eat(arg50, arg51, arg52);
    var v5 : List<Int> = mutableListOf(5, 0);
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }


}

