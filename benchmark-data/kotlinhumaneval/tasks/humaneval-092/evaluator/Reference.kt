fun checkDictCase(dict: Map<Any?, Any?>): Boolean {
    if (dict.isEmpty()) {
        return false
    }
    return (dict.keys.all { it is String && it.lowercase() == it }) ||
            (dict.values.all { it is String && it.uppercase() == it })
}

