fun main() {
    var arg10 : List<List<Int>> = mutableListOf(mutableListOf(0, 0, 1, 1), mutableListOf(0, 0, 0, 0), mutableListOf(1, 1, 1, 1), mutableListOf(0, 1, 1, 1))
    var arg11 : Int = 2
    var x1 : Int = maxFill(arg10, arg11);
    var v1 : Int = 5;
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20 : List<List<Int>> = mutableListOf(mutableListOf(0, 0, 0), mutableListOf(0, 0, 0))
    var arg21 : Int = 5
    var x2 : Int = maxFill(arg20, arg21);
    var v2 : Int = 0;
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30 : List<List<Int>> = mutableListOf(mutableListOf(1, 1, 1, 1), mutableListOf(1, 1, 1, 1))
    var arg31 : Int = 2
    var x3 : Int = maxFill(arg30, arg31);
    var v3 : Int = 4;
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40 : List<List<Int>> = mutableListOf(mutableListOf(1, 1, 1, 1), mutableListOf(1, 1, 1, 1))
    var arg41 : Int = 9
    var x4 : Int = maxFill(arg40, arg41);
    var v4 : Int = 2;
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }


}

