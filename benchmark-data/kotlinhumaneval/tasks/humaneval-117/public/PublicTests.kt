fun main() {
    var arg00 : List<Int> = mutableListOf(-3, -4, 5)
    var arg01 : Int = 3
    var x0 : List<Any> = maximum(arg00, arg01);
    var v0 : List<Any> = mutableListOf(-4, -3, 5);
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
