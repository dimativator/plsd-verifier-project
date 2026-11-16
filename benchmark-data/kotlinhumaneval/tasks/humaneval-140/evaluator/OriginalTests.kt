fun main() {
    var arg00 : String = "This is a test"
    var x0 : String = wordsInSentence(arg00);
    var v0 : String = "is";
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10 : String = "lets go for swimming"
    var x1 : String = wordsInSentence(arg10);
    var v1 : String = "go for";
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20 : String = "there is no place available here"
    var x2 : String = wordsInSentence(arg20);
    var v2 : String = "there is no place";
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30 : String = "Hi I am Hussein"
    var x3 : String = wordsInSentence(arg30);
    var v3 : String = "Hi am Hussein";
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40 : String = "go for it"
    var x4 : String = wordsInSentence(arg40);
    var v4 : String = "go for it";
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50 : String = "here"
    var x5 : String = wordsInSentence(arg50);
    var v5 : String = "";
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60 : String = "here is"
    var x6 : String = wordsInSentence(arg60);
    var v6 : String = "is";
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }


}

