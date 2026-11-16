fun main() {
    var arg00: String = "Hi, my name is John"
    var x0: List<String> = wordsString(arg00)
    var v0: List<String> = mutableListOf("Hi", "my", "name", "is", "John")
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: String = "One, two, three, four, five, six"
    var x1: List<String> = wordsString(arg10)
    var v1: List<String> = mutableListOf("One", "two", "three", "four", "five", "six")
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: String = "Hi, my name"
    var x2: List<String> = wordsString(arg20)
    var v2: List<String> = mutableListOf("Hi", "my", "name")
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: String = "One,, two, three, four, five, six,"
    var x3: List<String> = wordsString(arg30)
    var v3: List<String> = mutableListOf("One", "two", "three", "four", "five", "six")
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: String = ""
    var x4: List<String> = wordsString(arg40)
    var v4: List<String> = mutableListOf()
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50: String = "ahmed     , gamal"
    var x5: List<String> = wordsString(arg50)
    var v5: List<String> = mutableListOf("ahmed", "gamal")
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }


}

