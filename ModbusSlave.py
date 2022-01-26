#!/usr/bin/python3

from pyModbusTCP.server import ModbusServer, DataHandler
from pyModbusTCP.constants import MODBUS_PORT, EXP_ILLEGAL_FUNCTION
import argparse
import wiringpi as wp
from time import sleep

''' 미해결 파트: 접속하는 client의 host address에 따라 접속 허용 여부 결정 -> srv_info 전달에 문제 있음
allowToRead  = ['localhost', '203.252.121.226']
allowToWrite = ['localhost', '203.252.121.226']

class MyDataHandler(DataHandler):
	def read_coils(self, address, count, srv_info):
		if srv_info.client.address in allowToRead:
			return super().read_coils(address, count, srv_info)
		else:
			return DataHandler.Return(exp_code=EXP_ILLEGAL_FUNCTION)
      
	def read_d_inputs(self, address, count, srv_info):
		if srv_info.client.address in allowToRead:
			return super().read_d_inputs(address, count, srv_info)
		else:
			return DataHandler.Return(exp_code=EXP_ILLEGAL_FUNCTION)
      
	def read_h_regs(self, address, count, srv_info):
		if srv_info.client.address in allowToRead:
			return super().read_h_regs(address, count, srv_info)
		else:
			return DataHandler.Return(exp_code=EXP_ILLEGAL_FUNCTION)
	
  def read_i_regs(self, address, count, srv_info):
		if srv_info.client.address in allowToRead:
			return super().read_i_regs(address, count, srv_info)
		else:
			return DataHandler.Return(exp_code=EXP_ILLEGAL_FUNCTION)
	
  def write_coils(self, address, bits_l, srv_info):
		if srv_info.client.address in allowToWrite:
			return super().write_coils(address, bits_l, srv_info)
		else:
			return DataHandler.Return(exp_code=EXP_ILLEGAL_FUNCTION)
  
  def write_h_regs(self, address, words_l, srv_info):
		if srv_info.client.address in allowToWrite:
			return super().write_h_regs(address, words_l, srv_info)
		else:
			return DataHandler.Return(exp_code=EXP_ILLEGAL_FUNCTION)
'''

if __name__ == '__main__':
	# Parse arguments
	parser = argparse.ArgumentParser(description = 'Simple Modbus TCP/IP slave (server) for testing with Raspberry Pi 4')
	parser.add_argument('-H', '--host', type = str, default = 'localhost', help = 'Host (default: localhost)')
	parser.add_argument('-p', '--port', type = int, default = MODBUS_PORT, help = 'TCP port (default: 502)')
	args = parser.parse_args()

	# Initialize a Modbus TCP/IP slave
	server = ModbusServer(host = args.host, port = args.port, no_block = True)

	# Wiring Pi Setup
	if wp.wiringPiSetup() == -1:
		quit()

	try:
		print('Start a Modbus TCP/IP slave ...')
		server.start()
		print('Slave is online')

		prevState = [0]

		while True:
			# DataBank.get_words() 방식은 deprecated되었기에, 최신 버전에서는 아래와 같은 방식을 써야 함
			currState = server.data_hdl.read_h_regs(0, 3, None).data

			if prevState != currState:
				prevState = currState
				wp.pinMode(prevState[0], prevState[1])			# INPUT = 0, OUTPUT = 1
				wp.digitalWrite(prevState[0], prevState[2])	# LOW = 0, HIGH = 1

			sleep(0.5)
	except KeyboardInterrupt:
		print('Shutdown the Modbus TCP/IP slave ...')
		server.stop()
		print('Slave is offline')
