extends CharacterBody2D

@export var hastighed : float = 150
@export var despawn_x : float = -100

func _ready() -> void:
	if $AnimatedSprite2D:
		$AnimatedSprite2D.play("flyv")

func _physics_process(delta: float) -> void:
	velocity.x = hastighed * -1 
	velocity.y = 0
	move_and_slide()

	if global_position.x <= despawn_x:
		print("Removing bird")
		queue_free()
		
	for i in range(get_slide_collision_count()):
		var collision = get_slide_collision(i)
		if collision.get_collider().is_in_group("Player"):
			print("Collision with dino")
