fun main() {
    var arg00: List<Int> = mutableListOf(5, 5, 5, 5, 1)
    var x0: Int = search(arg00)
    var v0: Int = 1
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: List<Int> = mutableListOf(4, 1, 4, 1, 4, 4)
    var x1: Int = search(arg10)
    var v1: Int = 4
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: List<Int> = mutableListOf(3, 3)
    var x2: Int = search(arg20)
    var v2: Int = -1
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: List<Int> = mutableListOf(8, 8, 8, 8, 8, 8, 8, 8)
    var x3: Int = search(arg30)
    var v3: Int = 8
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: List<Int> = mutableListOf(2, 3, 3, 2, 2)
    var x4: Int = search(arg40)
    var v4: Int = 2
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50: List<Int> = mutableListOf(2, 7, 8, 8, 4, 8, 7, 3, 9, 6, 5, 10, 4, 3, 6, 7, 1, 7, 4, 10, 8, 1)
    var x5: Int = search(arg50)
    var v5: Int = 1
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60: List<Int> = mutableListOf(3, 2, 8, 2)
    var x6: Int = search(arg60)
    var v6: Int = 2
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70: List<Int> = mutableListOf(6, 7, 1, 8, 8, 10, 5, 8, 5, 3, 10)
    var x7: Int = search(arg70)
    var v7: Int = 1
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }

    var arg80: List<Int> = mutableListOf(8, 8, 3, 6, 5, 6, 4)
    var x8: Int = search(arg80)
    var v8: Int = -1
    if (x8 != v8) {
        throw Exception("Exception -- test case 8 did not pass. x8 = " + x8)
    }

    var arg90: List<Int> = mutableListOf(6, 9, 6, 7, 1, 4, 7, 1, 8, 8, 9, 8, 10, 10, 8, 4, 10, 4, 10, 1, 2, 9, 5, 7, 9)
    var x9: Int = search(arg90)
    var v9: Int = 1
    if (x9 != v9) {
        throw Exception("Exception -- test case 9 did not pass. x9 = " + x9)
    }

    var arg100: List<Int> = mutableListOf(1, 9, 10, 1, 3)
    var x10: Int = search(arg100)
    var v10: Int = 1
    if (x10 != v10) {
        throw Exception("Exception -- test case 10 did not pass. x10 = " + x10)
    }

    var arg110: List<Int> = mutableListOf(6, 9, 7, 5, 8, 7, 5, 3, 7, 5, 10, 10, 3, 6, 10, 2, 8, 6, 5, 4, 9, 5, 3, 10)
    var x11: Int = search(arg110)
    var v11: Int = 5
    if (x11 != v11) {
        throw Exception("Exception -- test case 11 did not pass. x11 = " + x11)
    }

    var arg120: List<Int> = mutableListOf(1)
    var x12: Int = search(arg120)
    var v12: Int = 1
    if (x12 != v12) {
        throw Exception("Exception -- test case 12 did not pass. x12 = " + x12)
    }

    var arg130: List<Int> = mutableListOf(8, 8, 10, 6, 4, 3, 5, 8, 2, 4, 2, 8, 4, 6, 10, 4, 2, 1, 10, 2, 1, 1, 5)
    var x13: Int = search(arg130)
    var v13: Int = 4
    if (x13 != v13) {
        throw Exception("Exception -- test case 13 did not pass. x13 = " + x13)
    }

    var arg140: List<Int> = mutableListOf(2, 10, 4, 8, 2, 10, 5, 1, 2, 9, 5, 5, 6, 3, 8, 6, 4, 10)
    var x14: Int = search(arg140)
    var v14: Int = 2
    if (x14 != v14) {
        throw Exception("Exception -- test case 14 did not pass. x14 = " + x14)
    }

    var arg150: List<Int> = mutableListOf(1, 6, 10, 1, 6, 9, 10, 8, 6, 8, 7, 3)
    var x15: Int = search(arg150)
    var v15: Int = 1
    if (x15 != v15) {
        throw Exception("Exception -- test case 15 did not pass. x15 = " + x15)
    }

    var arg160: List<Int> =
        mutableListOf(9, 2, 4, 1, 5, 1, 5, 2, 5, 7, 7, 7, 3, 10, 1, 5, 4, 2, 8, 4, 1, 9, 10, 7, 10, 2, 8, 10, 9, 4)
    var x16: Int = search(arg160)
    var v16: Int = 4
    if (x16 != v16) {
        throw Exception("Exception -- test case 16 did not pass. x16 = " + x16)
    }

    var arg170: List<Int> = mutableListOf(2, 6, 4, 2, 8, 7, 5, 6, 4, 10, 4, 6, 3, 7, 8, 8, 3, 1, 4, 2, 2, 10, 7)
    var x17: Int = search(arg170)
    var v17: Int = 4
    if (x17 != v17) {
        throw Exception("Exception -- test case 17 did not pass. x17 = " + x17)
    }

    var arg180: List<Int> = mutableListOf(9, 8, 6, 10, 2, 6, 10, 2, 7, 8, 10, 3, 8, 2, 6, 2, 3, 1)
    var x18: Int = search(arg180)
    var v18: Int = 2
    if (x18 != v18) {
        throw Exception("Exception -- test case 18 did not pass. x18 = " + x18)
    }

    var arg190: List<Int> = mutableListOf(5, 5, 3, 9, 5, 6, 3, 2, 8, 5, 6, 10, 10, 6, 8, 4, 10, 7, 7, 10, 8)
    var x19: Int = search(arg190)
    var v19: Int = -1
    if (x19 != v19) {
        throw Exception("Exception -- test case 19 did not pass. x19 = " + x19)
    }

    var arg200: List<Int> = mutableListOf(10)
    var x20: Int = search(arg200)
    var v20: Int = -1
    if (x20 != v20) {
        throw Exception("Exception -- test case 20 did not pass. x20 = " + x20)
    }

    var arg210: List<Int> = mutableListOf(9, 7, 7, 2, 4, 7, 2, 10, 9, 7, 5, 7, 2)
    var x21: Int = search(arg210)
    var v21: Int = 2
    if (x21 != v21) {
        throw Exception("Exception -- test case 21 did not pass. x21 = " + x21)
    }

    var arg220: List<Int> = mutableListOf(5, 4, 10, 2, 1, 1, 10, 3, 6, 1, 8)
    var x22: Int = search(arg220)
    var v22: Int = 1
    if (x22 != v22) {
        throw Exception("Exception -- test case 22 did not pass. x22 = " + x22)
    }

    var arg230: List<Int> = mutableListOf(7, 9, 9, 9, 3, 4, 1, 5, 9, 1, 2, 1, 1, 10, 7, 5, 6, 7, 6, 7, 7, 6)
    var x23: Int = search(arg230)
    var v23: Int = 1
    if (x23 != v23) {
        throw Exception("Exception -- test case 23 did not pass. x23 = " + x23)
    }

    var arg240: List<Int> = mutableListOf(3, 10, 10, 9, 2)
    var x24: Int = search(arg240)
    var v24: Int = -1
    if (x24 != v24) {
        throw Exception("Exception -- test case 24 did not pass. x24 = " + x24)
    }


}

