extends KinematicBody2D

onready var LOGO = get_node("/root/FlappyBird/FlappyBirdLogo")
onready var START = get_node("/root/FlappyBird/Startknap")
onready var VAEGGE = get_node("/root/FlappyBird/Node2D - Flere Vaegge")
onready var HUD = get_node("/root/FlappyBird/HUD")
onready var TISSEPAUSE = get_node("/root/FlappyBird/Tissepause")

var bevaegelse = Vector2(0,0)
var TYNGDEKRAFT = 3
var HOPSTYRKE = -120

var point = 0
var highscore = 0

var start_spillet = false
var newHighScore = false

var tissepause = false

func _ready():
	TISSEPAUSE.set_visible(false)
	var file = File.new()
	if (file.file_exists("user://highscore.txt")):
		file.open("user://highscore.txt", File.READ)
		highscore = file.get_16()
		file.close()
	update_hud()

func _physics_process(delta):
	if Input.is_action_just_pressed("Start") and !start_spillet:
		start_spil()
	elif start_spillet and !tissepause:
		if Input.is_action_just_pressed("Flyv"):
			bevaegelse.y += HOPSTYRKE
			
		bevaegelse.y += TYNGDEKRAFT
		bevaegelse = move_and_slide(bevaegelse, Vector2.UP)
		
		# Detect collision with screen
		if position.y > get_viewport().size.y:
			game_over()
		if position.y < 0:
			game_over()
			
	if Input.is_action_just_pressed("Pause"):
		if tissepause:
			resume_spil()
		else:
			pause_spil()

func tilfoej_point():
	point += 1
	if (point > highscore):
		newHighScore = true
		highscore = point
	update_hud()

func update_hud():
	HUD.set_antal_point(point)
	HUD.set_highscore(highscore)

func game_over():
	if (newHighScore):
		var file = File.new()
		file.open("user://highscore.txt", File.WRITE)
		file.store_16(highscore)
		file.close()
		print("Stored file with new high score " + str(highscore))
		
	get_tree().change_scene("res://Node2D - Game over.tscn")

func start_spil():
	start_spillet = true
	LOGO.set_visible(false)
	START.set_visible(false)
	VAEGGE.start()
	update_hud()
	
func pause_spil():
	TISSEPAUSE.set_visible(true)
	VAEGGE.set_visible(false)
	VAEGGE.stop()
	tissepause = true
	
func resume_spil():
	TISSEPAUSE.set_visible(false)
	VAEGGE.set_visible(true)
	VAEGGE.start()
	tissepause = false

func _on_Panel_gui_input(event):
	if event is InputEventMouseButton:
		if event.is_pressed():
			start_spil()
