fun main() {
    var arg10 : List<String> = mutableListOf("name", "enam", "game")
    var x1 : String = findMax(arg10);
    var v1 : String = "enam";
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20 : List<String> = mutableListOf("aaaaaaa", "bb", "cc")
    var x2 : String = findMax(arg20);
    var v2 : String = "aaaaaaa";
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30 : List<String> = mutableListOf("abc", "cba")
    var x3 : String = findMax(arg30);
    var v3 : String = "abc";
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40 : List<String> = mutableListOf("play", "this", "game", "of", "footbott")
    var x4 : String = findMax(arg40);
    var v4 : String = "footbott";
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50 : List<String> = mutableListOf("we", "are", "gonna", "rock")
    var x5 : String = findMax(arg50);
    var v5 : String = "gonna";
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60 : List<String> = mutableListOf("we", "are", "a", "mad", "nation")
    var x6 : String = findMax(arg60);
    var v6 : String = "nation";
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70 : List<String> = mutableListOf("this", "is", "a", "prrk")
    var x7 : String = findMax(arg70);
    var v7 : String = "this";
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }

    var arg80 : List<String> = mutableListOf("b")
    var x8 : String = findMax(arg80);
    var v8 : String = "b";
    if (x8 != v8) {
        throw Exception("Exception -- test case 8 did not pass. x8 = " + x8)
    }

    var arg90 : List<String> = mutableListOf("play", "play", "play")
    var x9 : String = findMax(arg90);
    var v9 : String = "play";
    if (x9 != v9) {
        throw Exception("Exception -- test case 9 did not pass. x9 = " + x9)
    }


}

