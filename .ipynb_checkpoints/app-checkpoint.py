from flask import Flask, redirect, url_for, request, send_from_directory
app = Flask(__name__)

@app.route('/', methods=['GET'])
def getMain():
    return send_from_directory('templates', 'input.html') 

if __name__ == '__main__':
	from argparse import ArgumentParser
	parser = ArgumentParser()
	parser.add_argument('-p', '--port', type=int, default = 9000)
	args = parser.parse_args()
	port = args.port
	app.run(host='0.0.0.0', port=port)
