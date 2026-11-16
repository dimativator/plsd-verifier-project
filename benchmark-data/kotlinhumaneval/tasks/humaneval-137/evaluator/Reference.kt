fun fixSpaces(text : String) : String {
	return text.replace(Regex(" {3,}"), "-").replace(' ', '_')
}

