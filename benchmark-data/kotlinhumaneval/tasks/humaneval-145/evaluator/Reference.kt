fun bf(planet1 : String, planet2 : String) : List<String> {
    val planets = listOf("Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune")
	val ind1 = planets.indexOf(planet1)
    val ind2 = planets.indexOf(planet2)
    if (ind1 == -1 || ind2 == -1 || ind1 == ind2) {
        return emptyList()
    }
    return planets.subList(Math.min(ind1, ind2) + 1, Math.max(ind1, ind2))
}

