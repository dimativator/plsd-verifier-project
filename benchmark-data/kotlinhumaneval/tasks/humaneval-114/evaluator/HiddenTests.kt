fun main() {
    var arg10 : String = "Mary had a little lamb"
    var arg11 : Int = 3
    var x1 : List<Any> = selectWords(arg10, arg11);
    var v1 : List<Any> = mutableListOf("Mary", "lamb");
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20 : String = "simple white space"
    var arg21 : Int = 2
    var x2 : List<Any> = selectWords(arg20, arg21);
    var v2 : List<Any> = mutableListOf();
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30 : String = "Hello world"
    var arg31 : Int = 4
    var x3 : List<Any> = selectWords(arg30, arg31);
    var v3 : List<Any> = mutableListOf("world");
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40 : String = "Uncle sam"
    var arg41 : Int = 3
    var x4 : List<Any> = selectWords(arg40, arg41);
    var v4 : List<Any> = mutableListOf("Uncle");
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50 : String = ""
    var arg51 : Int = 4
    var x5 : List<Any> = selectWords(arg50, arg51);
    var v5 : List<Any> = mutableListOf();
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60 : String = "a b c d e f"
    var arg61 : Int = 1
    var x6 : List<Any> = selectWords(arg60, arg61);
    var v6 : List<Any> = mutableListOf("b", "c", "d", "f");
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }


}

