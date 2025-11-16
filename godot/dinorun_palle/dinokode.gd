extends CharacterBody2D
@export var hoppehoejde: float = 200
@export var tyngdekraft: float = 5

@export var point: int = 0
@export var high_score: int = 0

const POINT_HASTIGHED: float = 0.1
const SAVE_FILE_NAME: String = "user://dinorun.save"

var _timer: Timer

func _ready() -> void:
	_timer = Timer.new()
	add_child(_timer)
	_timer.timeout.connect(tilfoej_point)  
	_timer.start(POINT_HASTIGHED)
	
	nulstil_point()
	
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
			_game_over()
		if collision.get_collider().is_in_group("Kaktus"):
			print("Collision with cactus")
			_game_over()

func nulstil_point() -> void:
	point = 0
	high_score = hent_highscore()
	_opdater_hud()

func tilfoej_point() -> void:
	point += 1
	if (point > high_score):
		high_score = point
	_opdater_hud()	

func gem_highscore() -> void:
	var save_file = FileAccess.open(SAVE_FILE_NAME, FileAccess.WRITE)
	save_file.store_32(high_score)
		
func hent_highscore() -> int:
	if not FileAccess.file_exists(SAVE_FILE_NAME):
		return 0
	else:
		var save_file = FileAccess.open(SAVE_FILE_NAME, FileAccess.READ)
		return save_file.get_32()

func _opdater_hud() -> void:
	get_parent().get_node("HUD - Hiscore og point").opdater_point(point, high_score)

func _game_over() -> void:
	gem_highscore()
	get_tree().change_scene_to_file("res://gameover.tscn")
