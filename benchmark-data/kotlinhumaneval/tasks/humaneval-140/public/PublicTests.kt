fun main() {
    var arg00 : String = "This is a test"
    var x0 : String = wordsInSentence(arg00);
    var v0 : String = "is";
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
