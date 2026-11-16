fun main() {
    var arg00: String = "yogurt"
    var x0: String = getClosestVowel(arg00);
    var v0: String = "u";
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: String = "full"
    var x1: String = getClosestVowel(arg10);
    var v1: String = "u";
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: String = "easy"
    var x2: String = getClosestVowel(arg20);
    var v2: String = "";
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: String = "eAsy"
    var x3: String = getClosestVowel(arg30);
    var v3: String = "";
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: String = "ali"
    var x4: String = getClosestVowel(arg40);
    var v4: String = "";
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50: String = "bad"
    var x5: String = getClosestVowel(arg50);
    var v5: String = "a";
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60: String = "most"
    var x6: String = getClosestVowel(arg60);
    var v6: String = "o";
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70: String = "ab"
    var x7: String = getClosestVowel(arg70);
    var v7: String = "";
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }

    var arg80: String = "ba"
    var x8: String = getClosestVowel(arg80);
    var v8: String = "";
    if (x8 != v8) {
        throw Exception("Exception -- test case 8 did not pass. x8 = " + x8)
    }

    var arg90: String = "quick"
    var x9: String = getClosestVowel(arg90);
    var v9: String = "";
    if (x9 != v9) {
        throw Exception("Exception -- test case 9 did not pass. x9 = " + x9)
    }

    var arg100: String = "anime"
    var x10: String = getClosestVowel(arg100);
    var v10: String = "i";
    if (x10 != v10) {
        throw Exception("Exception -- test case 10 did not pass. x10 = " + x10)
    }

    var arg110: String = "Asia"
    var x11: String = getClosestVowel(arg110);
    var v11: String = "";
    if (x11 != v11) {
        throw Exception("Exception -- test case 11 did not pass. x11 = " + x11)
    }

    var arg120: String = "Above"
    var x12: String = getClosestVowel(arg120);
    var v12: String = "o";
    if (x12 != v12) {
        throw Exception("Exception -- test case 12 did not pass. x12 = " + x12)
    }


}

