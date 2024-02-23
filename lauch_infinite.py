import subprocess

# Appel du programme Python externe
while True:
	process = subprocess.Popen(['python', 'solve_taquin.py'])

# Attendre que le programme externe se termine
	process.wait()

	print("Le programme externe s'est terminé.")