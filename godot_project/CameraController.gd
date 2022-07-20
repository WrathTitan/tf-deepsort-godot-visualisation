extends Node


# Declare member variables here. Examples:
# var a = 2
# var b = "text"


# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass


func _on_BackButton_pressed():
	if ($BackCamera.current==true):
		pass
	else:
		$FrontCamera.current=false
		$RightCamera.current=false
		$LeftCamera.current=false
		$BackCamera.current=true

func _on_FrontButton_pressed():
	if ($FrontCamera.current==true):
		pass
	else:
		$BackCamera.current=false
		$RightCamera.current=false
		$LeftCamera.current=false
		$FrontCamera.current=true


func _on_LeftButton_pressed():
	if ($LeftCamera.current==true):
		pass
	else:
		$BackCamera.current=false
		$FrontCamera.current=false
		$RightCamera.current=false
		$LeftCamera.current=true

func _on_RightButton_pressed():
	if ($RightCamera.current==true):
		pass
	else:
		$BackCamera.current=false
		$FrontCamera.current=false
		$LeftCamera.current=false
		$RightCamera.current=true
