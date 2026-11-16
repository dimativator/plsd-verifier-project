fun main() {
    var arg10 : List<Int> = mutableListOf(30, 13, 24, 321)
    var x1 : Int = solution(arg10);
    var v1 : Int = 0;
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20 : List<Int> = mutableListOf(5, 9)
    var x2 : Int = solution(arg20);
    var v2 : Int = 5;
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30 : List<Int> = mutableListOf(2, 4, 8)
    var x3 : Int = solution(arg30);
    var v3 : Int = 0;
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40 : List<Int> = mutableListOf(30, 13, 23, 32)
    var x4 : Int = solution(arg40);
    var v4 : Int = 23;
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50 : List<Int> = mutableListOf(3, 13, 2, 9)
    var x5 : Int = solution(arg50);
    var v5 : Int = 3;
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }


}

