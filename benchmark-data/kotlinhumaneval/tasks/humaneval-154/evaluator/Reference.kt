fun rightAngleTriangle(a : Int, b : Int, c : Int) : Boolean {
    fun sq(num: Int) = num * num
	return sq(listOf(a, b, c).max()) * 2 == sq(a) + sq(b) + sq(c)
}

