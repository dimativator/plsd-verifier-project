fun main() {
    var arg10 : String = "a b c a b"
    var x1 : Map<String, Int> = histogram(arg10);
    var v1 : Map<String, Int> = mutableMapOf("a" to 2, "b" to 2);
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20 : String = "a b c d g"
    var x2 : Map<String, Int> = histogram(arg20);
    var v2 : Map<String, Int> = mutableMapOf("a" to 1, "b" to 1, "c" to 1, "d" to 1, "g" to 1);
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30 : String = "r t g"
    var x3 : Map<String, Int> = histogram(arg30);
    var v3 : Map<String, Int> = mutableMapOf("r" to 1, "t" to 1, "g" to 1);
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40 : String = "b b b b a"
    var x4 : Map<String, Int> = histogram(arg40);
    var v4 : Map<String, Int> = mutableMapOf("b" to 4);
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50 : String = "r t g"
    var x5 : Map<String, Int> = histogram(arg50);
    var v5 : Map<String, Int> = mutableMapOf("r" to 1, "t" to 1, "g" to 1);
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60 : String = ""
    var x6 : Map<String, Int> = histogram(arg60);
    var v6 : Map<String, Int> = mutableMapOf();
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70 : String = "a"
    var x7 : Map<String, Int> = histogram(arg70);
    var v7 : Map<String, Int> = mutableMapOf("a" to 1);
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }


}

