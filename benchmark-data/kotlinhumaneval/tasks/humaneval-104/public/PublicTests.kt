fun main() {
    var arg00 : Int = 123
    var x0 : List<Int> = evenOddPalindrome(arg00);
    var v0 : List<Int> = mutableListOf(8, 13);
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
