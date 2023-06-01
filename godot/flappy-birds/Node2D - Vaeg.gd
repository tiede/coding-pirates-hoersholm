extends Node2D

var cheatMode = false

func _physics_process(delta):
	position.x += -100 * delta
	if global_position.x <= -50:
		queue_free()
		print("vaeg fjernet")

func _on_Area2D__Top_body_entered(body):
	print("top ramt")
	if !cheatMode:
		game_over(body)
	
func _on_Area2D__Bund_body_entered(body):
	print("bund ramt")
	if !cheatMode:
		game_over(body)

func _on_Area2D_body_entered(body):
	print("wuhu - point")
	body.tilfoej_point()
	$"PointsStreamPlayer".play()

func game_over(body):
	body.game_over()
