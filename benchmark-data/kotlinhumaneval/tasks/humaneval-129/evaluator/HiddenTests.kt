fun main() {
    var arg10 : String = "[]]]]]]][[[[[]"
    var x1 : Boolean = isNested(arg10);
    var v1 : Boolean = false;
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20 : String = "[][]"
    var x2 : Boolean = isNested(arg20);
    var v2 : Boolean = false;
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30 : String = "[]"
    var x3 : Boolean = isNested(arg30);
    var v3 : Boolean = false;
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40 : String = "[[[[]]]]"
    var x4 : Boolean = isNested(arg40);
    var v4 : Boolean = true;
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50 : String = "[]]]]]]]]]]"
    var x5 : Boolean = isNested(arg50);
    var v5 : Boolean = false;
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60 : String = "[][][[]]"
    var x6 : Boolean = isNested(arg60);
    var v6 : Boolean = true;
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70 : String = "[[]"
    var x7 : Boolean = isNested(arg70);
    var v7 : Boolean = false;
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }

    var arg80 : String = "[]]"
    var x8 : Boolean = isNested(arg80);
    var v8 : Boolean = false;
    if (x8 != v8) {
        throw Exception("Exception -- test case 8 did not pass. x8 = " + x8)
    }

    var arg90 : String = "[[]][["
    var x9 : Boolean = isNested(arg90);
    var v9 : Boolean = true;
    if (x9 != v9) {
        throw Exception("Exception -- test case 9 did not pass. x9 = " + x9)
    }

    var arg100 : String = "[[][]]"
    var x10 : Boolean = isNested(arg100);
    var v10 : Boolean = true;
    if (x10 != v10) {
        throw Exception("Exception -- test case 10 did not pass. x10 = " + x10)
    }

    var arg110 : String = ""
    var x11 : Boolean = isNested(arg110);
    var v11 : Boolean = false;
    if (x11 != v11) {
        throw Exception("Exception -- test case 11 did not pass. x11 = " + x11)
    }

    var arg120 : String = "[[[[[[[["
    var x12 : Boolean = isNested(arg120);
    var v12 : Boolean = false;
    if (x12 != v12) {
        throw Exception("Exception -- test case 12 did not pass. x12 = " + x12)
    }

    var arg130 : String = "]]]]]]]]"
    var x13 : Boolean = isNested(arg130);
    var v13 : Boolean = false;
    if (x13 != v13) {
        throw Exception("Exception -- test case 13 did not pass. x13 = " + x13)
    }


}

