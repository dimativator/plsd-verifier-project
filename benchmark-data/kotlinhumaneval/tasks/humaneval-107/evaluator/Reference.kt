fun exchange(lst1 : List<Int>, lst2 : List<Int>) : String {
	val countEven = lst1.count { it % 2 == 0 } + lst2.count { it % 2 == 0 }
    return if (countEven >= lst1.size) {
        "YES"
    } else {
        "NO"
    }
}

