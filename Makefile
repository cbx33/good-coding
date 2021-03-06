
# List of targets that are not files
.PHONY: all quick clean web print pdf screen quickpdf cleantmp cleanpdf cleanimages html htmlimages cleansite

all: pdf cleantmp
quick: quickpdf cleantmp
clean: cleantmp cleanpdf

# Generate a print version PDF (for lulu.com)
print:
	xelatex '\def\mediaformat{print}\input{opti}'
	makeindex opti
	xelatex '\def\mediaformat{print}\input{opti}'
	xelatex '\def\mediaformat{print}\input{opti}'

# Generate the PDF (on-screen version)
pdf:
	xelatex '\def\mediaformat{screen}\input{opti}'
	makeindex opti
	xelatex '\def\mediaformat{screen}\input{opti}'
	xelatex '\def\mediaformat{screen}\input{opti}'

# An alias for generated the PDF
screen: pdf

# Quickly update the PDF. Will not update the index or cross-references
quickpdf:
	xelatex opti

# Remove the temporary files generated by LaTeX
cleantmp:
	rm -f *.aux *.log *.out *.toc *.idx *.ind *.ilg

# Remove the generated PDF
cleanpdf:
	rm -f opti.pdf
	rm -f print.pdf

