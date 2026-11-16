fun main() {
    var arg00: String = "Hi, my name is John"
    var x0: List<String> = wordsString(arg00)
    var v0: List<String> = mutableListOf("Hi", "my", "name", "is", "John")
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
