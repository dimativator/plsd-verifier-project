fun main() {
    var arg10 : String = "Hello,world!"
    var x1 : Any = splitWords(arg10);
    var v1 : Any = mutableListOf("Hello", "world!");
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20 : String = "Hello world,!"
    var x2 : Any = splitWords(arg20);
    var v2 : Any = mutableListOf("Hello", "world,!");
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30 : String = "Hello,Hello,world !"
    var x3 : Any = splitWords(arg30);
    var v3 : Any = mutableListOf("Hello,Hello,world", "!");
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40 : String = "abcdef"
    var x4 : Any = splitWords(arg40);
    var v4 : Any = 3;
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50 : String = "aaabb"
    var x5 : Any = splitWords(arg50);
    var v5 : Any = 2;
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60 : String = "aaaBb"
    var x6 : Any = splitWords(arg60);
    var v6 : Any = 1;
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70 : String = ""
    var x7 : Any = splitWords(arg70);
    var v7 : Any = 0;
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }


}

