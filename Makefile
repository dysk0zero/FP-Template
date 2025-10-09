MAIN_TEX := tex/main.tex
OUTDIR := build

pdf:
	@mkdir -p $(OUTDIR)
	@latexmk -pdf -interaction=nonstopmode -halt-on-error -output-directory=$(OUTDIR) $(MAIN_TEX)

watch:
	@latexmk -pdf -pvc -interaction=nonstopmode -halt-on-error -output-directory=$(OUTDIR) $(MAIN_TEX)

clean:
	@latexmk -C -output-directory=$(OUTDIR)
	@rm -rf $(OUTDIR)
