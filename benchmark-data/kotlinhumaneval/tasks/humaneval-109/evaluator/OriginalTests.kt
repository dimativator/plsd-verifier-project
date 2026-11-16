fun main() {
    var arg00 : String = "abcde"
    var arg01 : String = "ae"
    var x0 : Pair<String, Boolean> = reverseDelete(arg00, arg01);
    var v0 : Pair<String, Boolean> = Pair("bcd", false)
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10 : String = "abcdef"
    var arg11 : String = "b"
    var x1 : Pair<String, Boolean> = reverseDelete(arg10, arg11);
    var v1 : Pair<String, Boolean> = Pair("acdef", false);
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20 : String = "abcdedcba"
    var arg21 : String = "ab"
    var x2 : Pair<String, Boolean> = reverseDelete(arg20, arg21);
    var v2 : Pair<String, Boolean> = Pair("cdedc", true);
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30 : String = "dwik"
    var arg31 : String = "w"
    var x3 : Pair<String, Boolean> = reverseDelete(arg30, arg31);
    var v3 : Pair<String, Boolean> = Pair("dik", false);
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40 : String = "a"
    var arg41 : String = "a"
    var x4 : Pair<String, Boolean> = reverseDelete(arg40, arg41);
    var v4 : Pair<String, Boolean> = Pair("", true);
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50 : String = "abcdedcba"
    var arg51 : String = ""
    var x5 : Pair<String, Boolean> = reverseDelete(arg50, arg51);
    var v5 : Pair<String, Boolean> = Pair("abcdedcba", true);
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60 : String = "abcdedcba"
    var arg61 : String = "v"
    var x6 : Pair<String, Boolean> = reverseDelete(arg60, arg61);
    var v6 : Pair<String, Boolean> = Pair("abcdedcba", true);
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70 : String = "vabba"
    var arg71 : String = "v"
    var x7 : Pair<String, Boolean> = reverseDelete(arg70, arg71);
    var v7 : Pair<String, Boolean> = Pair("abba", true);
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }

    var arg80 : String = "mamma"
    var arg81 : String = "mia"
    var x8 : Pair<String, Boolean> = reverseDelete(arg80, arg81);
    var v8 : Pair<String, Boolean> = Pair("", true);
    if (x8 != v8) {
        throw Exception("Exception -- test case 8 did not pass. x8 = " + x8)
    }


}

