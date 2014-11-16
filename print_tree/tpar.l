%{
/*
 * tpar: pre-processor for tree; adds parens according to indentation.
 * Version 0.1
 * 
 * Blank line ends the tree.
 * ` - ' adds following item on same line as single child.
 * Does not do forests -- add outer parens in source as part of
 * 	beginning and ending node names or use null command \Z.
 * Option -t converts N',V',A',P' by adding TeX \overline commands,
 * 	and [<digit or i,j,k,x,y,z>] by adding TeX subscripting
 * 	commands.
 * Option -v puts right parentheses on new lines, with indentation
 * 	the same as the preceding matching paren.
 * 
 * 			Greg, lee@uhccux.uhcc.hawaii.edu, 6/24/90
 */

#define TRUE 1
#define FALSE 0
int tex_opt = FALSE;
int v_opt = FALSE;

int outercol = 0;
int linenumber = 0;
int indent = 0;
int minindent = 0;
int level = 0;
int buried[100];
int extra = 0;
%}

%s T O X

%%

<O>\n {
	outercol = 0;
	indent = 0;
	linenumber++;
	ECHO;
}

<T,X>[ \t]*\n {
	if (!outercol) {
		descend(minindent);
		ECHO;
		BEGIN(O);
	}
	indent = outercol = 0;
	linenumber++;
}

<O>\t {
	outercol++;
	while (outercol % 8) outercol++;
	ECHO;
}

<T,X>\t {
	outercol++;
	while (outercol % 8) outercol++;
}

<T,X>" " {
	outercol++;
	if (indent) ECHO;
}

<T,X>[ \t]+"-"[ \t]+ {
	extra++;
	printf("(");
}

\\tree[ \t]*(-([tuvLTOIFER]+|[bg][0-9]+)[ \t]*)* {
	outercol += yyleng;
	level = extra = 0;
	minindent = 200;
	buried[0] = -1;
	if (tex_opt) BEGIN(X);
	else BEGIN(T);
	ECHO;
}

<O>. {
	outercol++;
	ECHO;
}

<X>[NVAP]' {
	ascend();
	outercol += 2;
	printf("$\\overline{\\rm %c}$", yytext[0]);
}

<X>\[[0-9ijkxyz]\] {
	ascend();
	outercol += 3;
	printf("$_%c$", yytext[1]);
}

<T,X>\\Z[ \t]*$ {
	ascend();
	outercol += 2;
}

<T,X>. {
	ascend();
	outercol++;
	ECHO;
}

%%

descend(indent)
int indent;
{	int i;

	if (extra) do printf(")"); while (--extra);
	if (indent > buried[level]) {
		buried[++level] = indent;
	}
	else {
		printf(")");
		while (level >= 0 && indent < buried[level]) {
			level--;
			if (v_opt) {
				printf("\n");
				for (i = 1; i < buried[level]; i++)
					printf(" ");
			}
			printf(")");
		}
	}
	printf("\n");
}

ascend()
{	int i;

	if (indent) return;
	descend(indent = outercol+1);
	if (indent < minindent) minindent = indent;
	for (i = 1; i < indent; i++) printf(" ");
	printf("(");
}

extern char *optarg;		/* from getopt */
extern int  optind;

main(argc, argv)
int     argc;
char   *argv[];
{	int c;
	char *progname = NULL, *basename();

	progname = basename (argv[0]);
	while ((c = getopt (argc, argv, "htv")) != EOF)
		switch (c) {
			case 't': tex_opt = TRUE; break;
			case 'v': v_opt = TRUE; break;
			case 'h':
	    		default: 
		   fprintf(stderr, "Usage: %s [options] [files]\n", progname);
		   fprintf(stderr, "options = -t\t(TeX code)\n");
		   fprintf(stderr, "          -v\t(parens on new lines)\n");
		   fprintf(stderr, "          -h\t(print this information)\n");
		   exit(1);
		}

	BEGIN(O);

	if (optind >= argc) {
		(void) yylex ();
	}
	else for (; (optind < argc); optind++) {
		if (yyin == NULL) yyin = stdin;
		if (freopen (argv[optind], "r", stdin) != NULL) {
#ifdef FLEX_SCANNER	
			/* to get flex to look at > 1 file */
			yy_init = 1;
#endif
			(void) yylex ();
    			if (level > 1) descend(minindent);
			outercol = linenumber = indent = minindent = 0;
			level = extra = 0;
		}
		else {
			(void) fprintf (stderr,
			    "Couldn't open file: %s\n", argv[optind]);
			exit (1);
		}
	}
    if (level > 1) descend(minindent);
}


char   *basename (s)
char   *s;
{
	char   *p, *strrchr();

	if (p = strrchr(s, '/'))
		return(++p);
	else return(s);
}
