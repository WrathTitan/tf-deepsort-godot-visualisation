extends Control
tool

export(bool) var btn =false setget set_btn

var socket = PacketPeerUDP.new()

func set_btn(new_val):
	print("Connecting to Host...")
	socket.connect_to_host("127.0.0.1", 6000)
	# socket.set_dest_address("127.0.0.1", 6000)
	var data = socket.get_packet()
	print(data)
	# socket.put_packet("Time to stop".to_ascii())
