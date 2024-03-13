SOLVE_TAQUIN = src/npuzzle.py
GET_NPUZZLE =  src/npuzzle-gen.py
NPUZZLE_OUTPUT = npuzzle.txt

default:
	python3 $(SOLVE_TAQUIN) -f ${NPUZZLE_OUTPUT}

npuzzle_random:
	@if [ -z "$(SIZE)" ]; then \
		echo "Usage: make npuzzle_random SIZE=<valeur>"; \
		exit 1; \
	fi; \
	python3 $(SOLVE_TAQUIN) -r $(SIZE)

npuzzle_file:
	@if [ -z "$(FILE)" ]; then \
		echo "Usage: make npuzzle_FILE FILE=<path>"; \
		exit 1; \
	fi; \
	python3 $(SOLVE_TAQUIN) -f $(FILE)

get_npuzzle:
	@if [ -z "$(SIZE)" ]; then \
		echo "Usage: make get_npuzzle SIZE=<valeur>"; \
		exit 1; \
	fi; \
	python3 $(GET_NPUZZLE) $(SIZE) > $(NPUZZLE_OUTPUT)

get_solvable_npuzzle:
	@if [ -z "$(SIZE)" ]; then \
		echo "Usage: get_solvable_npuzzle SIZE=<valeur>"; \
		exit 1; \
	fi; \
	python3 $(GET_NPUZZLE) -s   $(SIZE) > $(NPUZZLE_OUTPUT)

get_iter_npuzzle:
	@if [ -z "$(SIZE)" ]; then \
		echo "Usage: make get_iter_npuzzle ITER=<valeur> SIZE=<valeur>";  \
		exit 1; \
	fi; 
	@if [ -z "$(ITER)" ]; then \
		echo "Usage: make get_iter_npuzzle ITER=<valeur> SIZE=<valeur>"; \
		exit 1; \
	fi; \
	python3 $(GET_NPUZZLE) -s -i ${ITER}  $(SIZE) > $(NPUZZLE_OUTPUT)

get_unsolvable_npuzzle:
	@if [ -z "$(SIZE)" ]; then \
		echo "Usage: make get_unsolvable_npuzzle SIZE=<valeur>"; \
		exit 1; \
	fi; \
	python3 $(GET_NPUZZLE) -u $(SIZE) > $(NPUZZLE_OUTPUT)

all:
	@make get_solvable_npuzzle SIZE=$(SIZE)
	@make default

# Règle pour nettoyer les fichiers temporaires
clean:
	@rm -rf *.pyc src/__pycache__

# Règle pour nettoyer les fichiers temporaires et l'exécutable
fclean: clean

# Règle pour recompiler (effectue fclean et default)
re: fclean default