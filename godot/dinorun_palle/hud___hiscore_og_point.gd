extends Control

func opdater_point(point, highscore):
	var point_node = get_node("Point")
	point_node.text = str(point)
	
	var highscore_node = get_node("Highscore")
	highscore_node.text = str(highscore)
