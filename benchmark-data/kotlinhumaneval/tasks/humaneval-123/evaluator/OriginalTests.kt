fun main() {
    var arg00 : List<Int> = mutableListOf(5)
    var x0 : Boolean = isSorted(arg00);
    var v0 : Boolean = true;
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10 : List<Int> = mutableListOf(1, 2, 3, 4, 5)
    var x1 : Boolean = isSorted(arg10);
    var v1 : Boolean = true;
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20 : List<Int> = mutableListOf(1, 3, 2, 4, 5)
    var x2 : Boolean = isSorted(arg20);
    var v2 : Boolean = false;
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30 : List<Int> = mutableListOf(1, 2, 3, 4, 5, 6)
    var x3 : Boolean = isSorted(arg30);
    var v3 : Boolean = true;
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40 : List<Int> = mutableListOf(1, 2, 3, 4, 5, 6, 7)
    var x4 : Boolean = isSorted(arg40);
    var v4 : Boolean = true;
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50 : List<Int> = mutableListOf(1, 3, 2, 4, 5, 6, 7)
    var x5 : Boolean = isSorted(arg50);
    var v5 : Boolean = false;
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60 : List<Int> = mutableListOf()
    var x6 : Boolean = isSorted(arg60);
    var v6 : Boolean = true;
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70 : List<Int> = mutableListOf(1)
    var x7 : Boolean = isSorted(arg70);
    var v7 : Boolean = true;
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }

    var arg80 : List<Int> = mutableListOf(3, 2, 1)
    var x8 : Boolean = isSorted(arg80);
    var v8 : Boolean = false;
    if (x8 != v8) {
        throw Exception("Exception -- test case 8 did not pass. x8 = " + x8)
    }

    var arg90 : List<Int> = mutableListOf(1, 2, 2, 2, 3, 4)
    var x9 : Boolean = isSorted(arg90);
    var v9 : Boolean = false;
    if (x9 != v9) {
        throw Exception("Exception -- test case 9 did not pass. x9 = " + x9)
    }

    var arg100 : List<Int> = mutableListOf(1, 2, 3, 3, 3, 4)
    var x10 : Boolean = isSorted(arg100);
    var v10 : Boolean = false;
    if (x10 != v10) {
        throw Exception("Exception -- test case 10 did not pass. x10 = " + x10)
    }

    var arg110 : List<Int> = mutableListOf(1, 2, 2, 3, 3, 4)
    var x11 : Boolean = isSorted(arg110);
    var v11 : Boolean = true;
    if (x11 != v11) {
        throw Exception("Exception -- test case 11 did not pass. x11 = " + x11)
    }

    var arg120 : List<Int> = mutableListOf(1, 2, 3, 4)
    var x12 : Boolean = isSorted(arg120);
    var v12 : Boolean = true;
    if (x12 != v12) {
        throw Exception("Exception -- test case 12 did not pass. x12 = " + x12)
    }


}

