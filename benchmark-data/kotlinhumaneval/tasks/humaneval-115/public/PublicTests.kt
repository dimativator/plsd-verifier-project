fun main() {
    var arg00: String = "yogurt"
    var x0: String = getClosestVowel(arg00);
    var v0: String = "u";
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
