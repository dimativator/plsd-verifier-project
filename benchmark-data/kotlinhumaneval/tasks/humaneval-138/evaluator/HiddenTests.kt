fun main() {
    var arg10 : String = "1example.dll"
    var x1 : String = fileNameCheck(arg10);
    var v1 : String = "No";
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20 : String = "s1sdf3.asd"
    var x2 : String = fileNameCheck(arg20);
    var v2 : String = "No";
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30 : String = "K.dll"
    var x3 : String = fileNameCheck(arg30);
    var v3 : String = "Yes";
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40 : String = "MY16FILE3.exe"
    var x4 : String = fileNameCheck(arg40);
    var v4 : String = "Yes";
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50 : String = "His12FILE94.exe"
    var x5 : String = fileNameCheck(arg50);
    var v5 : String = "No";
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60 : String = "_Y.txt"
    var x6 : String = fileNameCheck(arg60);
    var v6 : String = "No";
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70 : String = "?aREYA.exe"
    var x7 : String = fileNameCheck(arg70);
    var v7 : String = "No";
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }

    var arg80 : String = "/this_is_valid.dll"
    var x8 : String = fileNameCheck(arg80);
    var v8 : String = "No";
    if (x8 != v8) {
        throw Exception("Exception -- test case 8 did not pass. x8 = " + x8)
    }

    var arg90 : String = "this_is_valid.wow"
    var x9 : String = fileNameCheck(arg90);
    var v9 : String = "No";
    if (x9 != v9) {
        throw Exception("Exception -- test case 9 did not pass. x9 = " + x9)
    }

    var arg100 : String = "this_is_valid.txt"
    var x10 : String = fileNameCheck(arg100);
    var v10 : String = "Yes";
    if (x10 != v10) {
        throw Exception("Exception -- test case 10 did not pass. x10 = " + x10)
    }

    var arg110 : String = "this_is_valid.txtexe"
    var x11 : String = fileNameCheck(arg110);
    var v11 : String = "No";
    if (x11 != v11) {
        throw Exception("Exception -- test case 11 did not pass. x11 = " + x11)
    }

    var arg120 : String = "#this2_i4s_5valid.ten"
    var x12 : String = fileNameCheck(arg120);
    var v12 : String = "No";
    if (x12 != v12) {
        throw Exception("Exception -- test case 12 did not pass. x12 = " + x12)
    }

    var arg130 : String = "@this1_is6_valid.exe"
    var x13 : String = fileNameCheck(arg130);
    var v13 : String = "No";
    if (x13 != v13) {
        throw Exception("Exception -- test case 13 did not pass. x13 = " + x13)
    }

    var arg140 : String = "this_is_12valid.6exe4.txt"
    var x14 : String = fileNameCheck(arg140);
    var v14 : String = "No";
    if (x14 != v14) {
        throw Exception("Exception -- test case 14 did not pass. x14 = " + x14)
    }

    var arg150 : String = "all.exe.txt"
    var x15 : String = fileNameCheck(arg150);
    var v15 : String = "No";
    if (x15 != v15) {
        throw Exception("Exception -- test case 15 did not pass. x15 = " + x15)
    }

    var arg160 : String = "I563_No.exe"
    var x16 : String = fileNameCheck(arg160);
    var v16 : String = "Yes";
    if (x16 != v16) {
        throw Exception("Exception -- test case 16 did not pass. x16 = " + x16)
    }

    var arg170 : String = "Is3youfault.txt"
    var x17 : String = fileNameCheck(arg170);
    var v17 : String = "Yes";
    if (x17 != v17) {
        throw Exception("Exception -- test case 17 did not pass. x17 = " + x17)
    }

    var arg180 : String = "no_one#knows.dll"
    var x18 : String = fileNameCheck(arg180);
    var v18 : String = "Yes";
    if (x18 != v18) {
        throw Exception("Exception -- test case 18 did not pass. x18 = " + x18)
    }

    var arg190 : String = "1I563_Yes3.exe"
    var x19 : String = fileNameCheck(arg190);
    var v19 : String = "No";
    if (x19 != v19) {
        throw Exception("Exception -- test case 19 did not pass. x19 = " + x19)
    }

    var arg200 : String = "I563_Yes3.txtt"
    var x20 : String = fileNameCheck(arg200);
    var v20 : String = "No";
    if (x20 != v20) {
        throw Exception("Exception -- test case 20 did not pass. x20 = " + x20)
    }

    var arg210 : String = "final..txt"
    var x21 : String = fileNameCheck(arg210);
    var v21 : String = "No";
    if (x21 != v21) {
        throw Exception("Exception -- test case 21 did not pass. x21 = " + x21)
    }

    var arg220 : String = "final132"
    var x22 : String = fileNameCheck(arg220);
    var v22 : String = "No";
    if (x22 != v22) {
        throw Exception("Exception -- test case 22 did not pass. x22 = " + x22)
    }

    var arg230 : String = "_f4indsartal132."
    var x23 : String = fileNameCheck(arg230);
    var v23 : String = "No";
    if (x23 != v23) {
        throw Exception("Exception -- test case 23 did not pass. x23 = " + x23)
    }

    var arg240 : String = ".txt"
    var x24 : String = fileNameCheck(arg240);
    var v24 : String = "No";
    if (x24 != v24) {
        throw Exception("Exception -- test case 24 did not pass. x24 = " + x24)
    }

    var arg250 : String = "s."
    var x25 : String = fileNameCheck(arg250);
    var v25 : String = "No";
    if (x25 != v25) {
        throw Exception("Exception -- test case 25 did not pass. x25 = " + x25)
    }


}

