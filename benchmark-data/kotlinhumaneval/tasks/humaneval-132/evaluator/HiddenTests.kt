fun main() {
    var arg10 : List<Int> = mutableListOf(1, 2, 4, 5)
    var x1 : Int = canArrange(arg10);
    var v1 : Int = -1;
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20 : List<Int> = mutableListOf(1, 4, 2, 5, 6, 7, 8, 9, 10)
    var x2 : Int = canArrange(arg20);
    var v2 : Int = 2;
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30 : List<Int> = mutableListOf(4, 8, 5, 7, 3)
    var x3 : Int = canArrange(arg30);
    var v3 : Int = 4;
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40 : List<Int> = mutableListOf()
    var x4 : Int = canArrange(arg40);
    var v4 : Int = -1;
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }


}

