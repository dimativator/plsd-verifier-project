fun compareOne(a : Any, b : Any) : Any? {
	fun toNumber(x: Any): Double {
        if (x is String) {
            return x.replace(',', '.').toDouble()
        }
        if (x is Double) {
            return x
        }
        if (x is Int) {
            return x.toDouble()
        }
        throw Exception("Invalid number")
    }

    val aval = toNumber(a)
    val bval = toNumber(b)
    return if (aval > bval) {
        return a
    } else if (aval < bval) {
        return b
    } else {
        return null
    }
}

