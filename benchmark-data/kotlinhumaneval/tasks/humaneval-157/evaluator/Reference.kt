fun doAlgebra(operator: List<String>, operand: List<Int>): Int {
    if (operator.isEmpty()) {
        return operand[0]
    }
    operator.withIndex().reversed().forEach { (index, op) ->
        when (op) {
            "+" -> return doAlgebra(operator.subList(0, index), operand.subList(0, index + 1)) +
                    doAlgebra(operator.subList(index + 1, operator.size), operand.subList(index + 1, operand.size))

            "-" -> return doAlgebra(operator.subList(0, index), operand.subList(0, index + 1)) -
                    doAlgebra(operator.subList(index + 1, operator.size), operand.subList(index + 1, operand.size))
        }
    }
    operator.withIndex().reversed().forEach { (index, op) ->
        when (op) {
            "*" -> return doAlgebra(operator.subList(0, index), operand.subList(0, index + 1)) *
                    doAlgebra(operator.subList(index + 1, operator.size), operand.subList(index + 1, operand.size))

            "//" -> return doAlgebra(operator.subList(0, index), operand.subList(0, index + 1)) /
                    doAlgebra(operator.subList(index + 1, operator.size), operand.subList(index + 1, operand.size))
        }
    }
    operator.withIndex().reversed().forEach { (index, op) ->
        when (op) {
            "**" -> return Math.pow(
                doAlgebra(operator.subList(0, index), operand.subList(0, index + 1)).toDouble(),
                doAlgebra(operator.subList(index + 1, operator.size), operand.subList(index + 1, operand.size)).toDouble()
            ).toInt()
        }
    }

    throw Exception("Invalid operator")
}

