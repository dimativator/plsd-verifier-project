fun main() {
    var arg00: List<Int> = mutableListOf(3, 4, 5, 1, 2)
    var x0: Boolean = moveOneBall(arg00);
    var v0: Boolean = true;
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: List<Int> = mutableListOf(3, 5, 10, 1, 2)
    var x1: Boolean = moveOneBall(arg10);
    var v1: Boolean = true;
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: List<Int> = mutableListOf(4, 3, 1, 2)
    var x2: Boolean = moveOneBall(arg20);
    var v2: Boolean = false;
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: List<Int> = mutableListOf(3, 5, 4, 1, 2)
    var x3: Boolean = moveOneBall(arg30);
    var v3: Boolean = false;
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: List<Int> = mutableListOf()
    var x4: Boolean = moveOneBall(arg40);
    var v4: Boolean = true;
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }


}

