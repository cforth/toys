%{
/*
 * unpar.l: substitute indentation for parenthesization.
 * Version 0.1
 * (unpar recognizes some \tree definitions as correct which tree
 *  rejects.)
 * 			-- Greg Lee, lee@uhccux.uhcc.hawaii.edu, 6/24/90
 */
#define TRUE 1
#define FALSE 0
int tex_opt = FALSE;
int level = 0;
int havename = 0;
int wait = 0;
int i;
%}

%s T X C

%%

^".tr" {
	printf("\\tree");
	havename = 1;
	BEGIN(T);
}

\\tree[ \t]*(-([tuvLTOIFER]+|[bg][0-9]+)[ \t]*)* {
	ECHO;
	havename = 1;
	if (tex_opt) BEGIN(X);
	else BEGIN(T);
}

<T,X>^[ \t]+	;
<T,X>[ \t]+$	;

<T,X>\n	;

<T,X>\\\( {
	havename = 1;
	ECHO;
}
<T,X>[^ \t\n\(\)]/\( {
	havename = 1;
	ECHO;
	putchar(' ');
}
<T,X>"("([^\)\(]|\\\)|\\\()+"("([^\)\(]|\\\)|\\\()+")"([^\)\(]|\\\)|\\\()*")" {
	wait = 2;
	REJECT;
}
<T,X>"("[ \t\n]* {
	level++;
	if (wait == 1) printf(" - ");
	else {
		if (!havename) printf("\\Z\n");
		else putchar('\n');
		indent();
	}
	havename = 0;
	if (wait) wait--;
}
<T,X>")"[^\)\(]+ {
	if (level == 1) {REJECT;}
	else level--;
}
<T,X>")" {
	level--;
	if (!level) {
		printf("\n");
		BEGIN(0);
	}
}
<X>\$_[0-9ijkxyz]\$ {
	havename = 1;
	printf("[%c]", yytext[2]);
}
<X>\$\\overline\{\\rm\ [NAVP]\}\$ {
	havename = 1;
	printf(" %c'", yytext[15]);
}
<T,X>\\[%\(\)] {
	havename = 1;
	ECHO;
}
<T,X>% {
	BEGIN(C);
}
<C>\n {
	if (tex_opt) BEGIN(X);
	else BEGIN(T);
}
<C>. ;
<T,X>. {
	havename = 1;
	ECHO;
}

%%

indent()
{	int i;

	for (i = 0; i < 2*(level-1); i++) putchar(' ');
}

extern char *optarg;		/* from getopt */
extern int  optind;

main(argc, argv)
int     argc;
char   *argv[];
{	int c;
	char *progname = NULL, *basename();

	progname = basename (argv[0]);
	while ((c = getopt (argc, argv, "ht")) != EOF)
		switch (c) {
			case 't': tex_opt = TRUE; break;
			case 'h':
	    		default: 
		   fprintf(stderr, "Usage: %s [options] [files]\n", progname);
		   fprintf(stderr, "options = -t\t(remove TeX code)\n");
		   fprintf(stderr, "          -h\t(print this information)\n");
		   exit(1);
		}

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
		}
		else {
			(void) fprintf (stderr,
			    "Couldn't open file: %s\n", argv[optind]);
			exit (1);
		}
	}
}


char   *basename (s)
char   *s;
{
	char   *p, *strrchr();

	if (p = strrchr(s, '/'))
		return(++p);
	else return(s);
}
