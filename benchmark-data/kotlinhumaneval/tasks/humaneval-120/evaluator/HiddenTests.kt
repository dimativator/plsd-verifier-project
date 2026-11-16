fun main() {
    var arg10 : Int = 5
    var x1 : List<Int> = getOddCollatz(arg10);
    var v1 : List<Int> = mutableListOf(1, 5);
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20 : Int = 12
    var x2 : List<Int> = getOddCollatz(arg20);
    var v2 : List<Int> = mutableListOf(1, 3, 5);
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30 : Int = 1
    var x3 : List<Int> = getOddCollatz(arg30);
    var v3 : List<Int> = mutableListOf(1);
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }


}

