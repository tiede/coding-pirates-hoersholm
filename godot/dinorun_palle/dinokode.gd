extends CharacterBody2D
@export var hoppehoejde: float = 200
@export var tyngdekraft: float = 5

@export var point: int = 0

func _physics_process(delta: float) -> void:
	if not is_on_floor():
		velocity.y += tyngdekraft + delta
	else:
		velocity.y = 0
	
	if Input.is_action_just_pressed("hop"):
		velocity.y -= hoppehoejde
		
	move_and_slide() # Dette er kommandoen der gør at dino flytter sig.	
	
	for i in range(get_slide_collision_count()):
		var collision = get_slide_collision(i)
		if collision.get_collider().is_in_group("Fugl"):
			print("Collision with bird")
			get_tree().change_scene_to_file("res://gameover.tscn")
		if collision.get_collider().is_in_group("Kaktus"):
			print("Collision with cactus")
			get_tree().change_scene_to_file("res://gameover.tscn")

func tilfoej_point() -> void:
	point += 1
	
func gem_highscore() -> void:
	pass
	
func hent_highscore() -> void:
	pass
