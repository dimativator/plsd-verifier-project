fun main() {
    var arg00 : List<String> = mutableListOf("aa", "a", "aaa")
    var x0 : List<Any> = sortedListSum(arg00);
    var v0 : List<Any> = mutableListOf("aa");
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
