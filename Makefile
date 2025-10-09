.PHONY: pdf watch clean check-tex build
.SILENT:

MAIN_TEX := tex/main.tex
OUTDIR := build

pdf: check-tex
	@mkdir -p $(OUTDIR)
	@latexmk -pdf -interaction=nonstopmode -halt-on-error -output-directory=$(OUTDIR) $(MAIN_TEX)

watch: check-tex
	@latexmk -pdf -pvc -interaction=nonstopmode -halt-on-error -output-directory=$(OUTDIR) $(MAIN_TEX)

clean:
	@latexmk -C -output-directory=$(OUTDIR) $(MAIN_TEX)
	@rm -rf $(OUTDIR)

check-tex:
	@command -v latexmk >/dev/null 2>&1 || { echo "❌ latexmk not found. Install TeX Live or MacTeX."; exit 1; }

build: pdf
