fun main() {
    var arg00 : List<String> = mutableListOf("aa", "a", "aaa")
    var x0 : List<Any> = sortedListSum(arg00);
    var v0 : List<Any> = mutableListOf("aa");
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10 : List<String> = mutableListOf("school", "AI", "asdf", "b")
    var x1 : List<Any> = sortedListSum(arg10);
    var v1 : List<Any> = mutableListOf("AI", "asdf", "school");
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20 : List<String> = mutableListOf("d", "b", "c", "a")
    var x2 : List<Any> = sortedListSum(arg20);
    var v2 : List<Any> = mutableListOf();
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30 : List<String> = mutableListOf("d", "dcba", "abcd", "a")
    var x3 : List<Any> = sortedListSum(arg30);
    var v3 : List<Any> = mutableListOf("abcd", "dcba");
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40 : List<String> = mutableListOf("AI", "ai", "au")
    var x4 : List<Any> = sortedListSum(arg40);
    var v4 : List<Any> = mutableListOf("AI", "ai", "au");
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50 : List<String> = mutableListOf("a", "b", "b", "c", "c", "a")
    var x5 : List<Any> = sortedListSum(arg50);
    var v5 : List<Any> = mutableListOf();
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60 : List<String> = mutableListOf("aaaa", "bbbb", "dd", "cc")
    var x6 : List<Any> = sortedListSum(arg60);
    var v6 : List<Any> = mutableListOf("cc", "dd", "aaaa", "bbbb");
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }


}

