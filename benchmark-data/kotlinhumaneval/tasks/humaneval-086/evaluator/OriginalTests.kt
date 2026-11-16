fun main() {
    var arg00: String = "hi"
    var x0: String = encrypt(arg00)
    var v0: String = "lm"
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: String = "asdfghjkl"
    var x1: String = encrypt(arg10)
    var v1: String = "ewhjklnop"
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: String = "gf"
    var x2: String = encrypt(arg20)
    var v2: String = "kj"
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: String = "et"
    var x3: String = encrypt(arg30)
    var v3: String = "ix"
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: String = "faewfawefaewg"
    var x4: String = encrypt(arg40)
    var v4: String = "jeiajeaijeiak"
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50: String = "hellomyfriend"
    var x5: String = encrypt(arg50)
    var v5: String = "lippsqcjvmirh"
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60: String = "dxzdlmnilfuhmilufhlihufnmlimnufhlimnufhfucufh"
    var x6: String = encrypt(arg60)
    var v6: String = "hbdhpqrmpjylqmpyjlpmlyjrqpmqryjlpmqryjljygyjl"
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70: String = "a"
    var x7: String = encrypt(arg70)
    var v7: String = "e"
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }


}

