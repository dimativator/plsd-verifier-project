fun sortedListSum(lst : List<String>) : List<String> {
    return lst.filter { it.length % 2 == 0 }
        .sortedWith(compareBy({ it.length }, { it }))
}

