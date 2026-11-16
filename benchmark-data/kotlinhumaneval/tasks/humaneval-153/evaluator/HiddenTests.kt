fun main() {
    var arg10 : Int = 152
    var x1 : String = intToMiniRoman(arg10);
    var v1 : String = "clii";
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20 : Int = 251
    var x2 : String = intToMiniRoman(arg20);
    var v2 : String = "ccli";
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30 : Int = 426
    var x3 : String = intToMiniRoman(arg30);
    var v3 : String = "cdxxvi";
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40 : Int = 500
    var x4 : String = intToMiniRoman(arg40);
    var v4 : String = "d";
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50 : Int = 1
    var x5 : String = intToMiniRoman(arg50);
    var v5 : String = "i";
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60 : Int = 4
    var x6 : String = intToMiniRoman(arg60);
    var v6 : String = "iv";
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70 : Int = 43
    var x7 : String = intToMiniRoman(arg70);
    var v7 : String = "xliii";
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }

    var arg80 : Int = 90
    var x8 : String = intToMiniRoman(arg80);
    var v8 : String = "xc";
    if (x8 != v8) {
        throw Exception("Exception -- test case 8 did not pass. x8 = " + x8)
    }

    var arg90 : Int = 94
    var x9 : String = intToMiniRoman(arg90);
    var v9 : String = "xciv";
    if (x9 != v9) {
        throw Exception("Exception -- test case 9 did not pass. x9 = " + x9)
    }

    var arg100 : Int = 532
    var x10 : String = intToMiniRoman(arg100);
    var v10 : String = "dxxxii";
    if (x10 != v10) {
        throw Exception("Exception -- test case 10 did not pass. x10 = " + x10)
    }

    var arg110 : Int = 900
    var x11 : String = intToMiniRoman(arg110);
    var v11 : String = "cm";
    if (x11 != v11) {
        throw Exception("Exception -- test case 11 did not pass. x11 = " + x11)
    }

    var arg120 : Int = 994
    var x12 : String = intToMiniRoman(arg120);
    var v12 : String = "cmxciv";
    if (x12 != v12) {
        throw Exception("Exception -- test case 12 did not pass. x12 = " + x12)
    }

    var arg130 : Int = 1000
    var x13 : String = intToMiniRoman(arg130);
    var v13 : String = "m";
    if (x13 != v13) {
        throw Exception("Exception -- test case 13 did not pass. x13 = " + x13)
    }


}

