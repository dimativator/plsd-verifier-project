fun main() {
    var arg00 : Int = 5
    var x0 : List<Int> = f(arg00);
    var v0 : List<Int> = mutableListOf(1, 2, 6, 24, 15);
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10 : Int = 7
    var x1 : List<Int> = f(arg10);
    var v1 : List<Int> = mutableListOf(1, 2, 6, 24, 15, 720, 28);
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20 : Int = 1
    var x2 : List<Int> = f(arg20);
    var v2 : List<Int> = mutableListOf(1);
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30 : Int = 3
    var x3 : List<Int> = f(arg30);
    var v3 : List<Int> = mutableListOf(1, 2, 6);
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }


}

