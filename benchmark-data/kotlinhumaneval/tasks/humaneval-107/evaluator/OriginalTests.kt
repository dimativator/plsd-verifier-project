fun main() {
    var arg00 : List<Int> = mutableListOf(1, 2, 3, 4)
    var arg01 : List<Int> = mutableListOf(1, 2, 3, 4)
    var x0 : String = exchange(arg00, arg01);
    var v0 : String = "YES";
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10 : List<Int> = mutableListOf(1, 2, 3, 4)
    var arg11 : List<Int> = mutableListOf(1, 5, 3, 4)
    var x1 : String = exchange(arg10, arg11);
    var v1 : String = "NO";
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20 : List<Int> = mutableListOf(1, 2, 3, 4)
    var arg21 : List<Int> = mutableListOf(2, 1, 4, 3)
    var x2 : String = exchange(arg20, arg21);
    var v2 : String = "YES";
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30 : List<Int> = mutableListOf(5, 7, 3)
    var arg31 : List<Int> = mutableListOf(2, 6, 4)
    var x3 : String = exchange(arg30, arg31);
    var v3 : String = "YES";
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40 : List<Int> = mutableListOf(5, 7, 3)
    var arg41 : List<Int> = mutableListOf(2, 6, 3)
    var x4 : String = exchange(arg40, arg41);
    var v4 : String = "NO";
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50 : List<Int> = mutableListOf(3, 2, 6, 1, 8, 9)
    var arg51 : List<Int> = mutableListOf(3, 5, 5, 1, 1, 1)
    var x5 : String = exchange(arg50, arg51);
    var v5 : String = "NO";
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60 : List<Int> = mutableListOf(100, 200)
    var arg61 : List<Int> = mutableListOf(200, 200)
    var x6 : String = exchange(arg60, arg61);
    var v6 : String = "YES";
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }


}

