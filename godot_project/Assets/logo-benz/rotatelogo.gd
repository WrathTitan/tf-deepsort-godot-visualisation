extends Spatial


# Declare member variables here. Examples:
# var a = 2
# var b = "text"

var dashboard_object_map = preload("res://SceneOne.tscn").instance()


# Called when the node enters the scene tree for the first time.
func _ready():
	var anim = get_node("AnimationPlayer").get_animation("LogoRotation")
	anim.set_loop(true)
	get_node("AnimationPlayer").play("LogoRotation")
	#self.rotate(Vector3(0,1,0),0)
	#self.rotatey(deg2rad(90.0))
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass


func _on_StartGUI_pressed():
	get_child(0).get_child(2).play("fade_to_black")
	get_child(0).get_child(2).play("fade_to_normal")
	for n in self.get_children():
		self.remove_child(n)
		n.queue_free()
	
	self.add_child(dashboard_object_map)
	
	#get_tree().get_root().add_child(dashboard_object_map)
	pass # Replace with function body.
