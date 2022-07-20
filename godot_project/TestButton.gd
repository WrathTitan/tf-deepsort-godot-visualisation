extends Button

var socket = PacketPeerUDP.new()
var mb_car = preload("res://green_car.tscn")
# Called when the node enters the scene tree for the first time.
func _ready():
	#print(get_viewport_rect().size)
	#socket.connect_to_host("127.0.0.1",65432)
	$HTTPRequest.connect("request_completed",self,"_on_HTTPRequest_request_completed")
	pass

func _process(delta):
	print(get_viewport_rect().size)
	print(get_viewport_rect().abs())
	print(get_viewport_rect().position)

func _on_Button_pressed():
	#var data = socket.get_packet()
	#print(data)
	#get_parent().get_node("Label").text = data
	#pass
	#print("Started Connecting...")
	$HTTPRequest.request("http://127.0.0.1:5000/getbb",PoolStringArray([]),false)

func despawn_objects():
	print("Freeing Queue")
	for n in get_parent().get_parent().get_parent().get_node("SpawnL1").get_children():
		get_parent().get_parent().get_parent().get_node("SpawnL1").remove_child(n)
		n.queue_free()
		
	for n in get_parent().get_parent().get_parent().get_node("SpawnL2").get_children():
		get_parent().get_parent().get_parent().get_node("SpawnL2").remove_child(n)
		n.queue_free()
		
	for n in get_parent().get_parent().get_parent().get_node("SpawnL3").get_children():
		get_parent().get_parent().get_parent().get_node("SpawnL3").remove_child(n)
		n.queue_free()
		
	for n in get_parent().get_parent().get_parent().get_node("SpawnR1").get_children():
		get_parent().get_parent().get_parent().get_node("SpawnR1").remove_child(n)
		n.queue_free()
		
	for n in get_parent().get_parent().get_parent().get_node("SpawnR2").get_children():
		get_parent().get_parent().get_parent().get_node("SpawnR2").remove_child(n)
		n.queue_free()
		
	for n in get_parent().get_parent().get_parent().get_node("SpawnR3").get_children():
		get_parent().get_parent().get_parent().get_node("SpawnR3").remove_child(n)
		n.queue_free()

func _on_HTTPRequest_request_completed(result, response_code, headers, body):
	if (response_code==200):
		despawn_objects()
			
		var results = JSON.parse(body.get_string_from_utf8())
		for obj in results.result["data"]:
			
			#var bb = obj["bounding_box"]
			var obj_class_name = obj["class"]
			#var x_norm = obj["bb_x_center"]/obj["width"]
			#var y_norm = obj["bb_y_center"]/obj["height"]
			var depth_info = obj["depth_info"]
			var width = obj["width"]
			var height = obj["height"]
			
			var x_center = obj["bb_x_center"]
			var y_center = obj["bb_y_center"]
			
			var obj_instance = mb_car.instance()
			if (x_center > (width/2) and obj_class_name=="car"):
				if (depth_info>900):
					get_parent().get_parent().get_parent().get_node("SpawnR3").add_child(obj_instance)
				elif (depth_info>600):
					get_parent().get_parent().get_parent().get_node("SpawnR2").add_child(obj_instance)
				else:
					get_parent().get_parent().get_parent().get_node("SpawnR1").add_child(obj_instance)
			else:
				if (depth_info>900):
					get_parent().get_parent().get_parent().get_node("SpawnL3").add_child(obj_instance)
				elif (depth_info>600):
					get_parent().get_parent().get_parent().get_node("SpawnL2").add_child(obj_instance)
				else:
					get_parent().get_parent().get_parent().get_node("SpawnL1").add_child(obj_instance)
		
		get_parent().get_node("Label").text = body.get_string_from_utf8()
		$HTTPRequest.request("http://127.0.0.1:5000/getbb",PoolStringArray([]),false)
	else:
		pass
