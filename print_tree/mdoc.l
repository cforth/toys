%{
/* mdoc: utility to add \tree examples to "use" document for tree
 *		Greg Lee, July 1990
 */
char *buf, *bufp;
char *line[100];
int count = 0, last = 0, i;
#define ADDCH(c) *bufp++ = c
#define ADDS(s) strcpy(bufp,s); bufp += yyleng
%}

%s X

%%

^"\\xtwo"[ \t\n]+ {
	ECHO;
	last = 2;
	line[0] = bufp;
	BEGIN(X);
}

^"\\xthree"[ \t\n]+ {
	ECHO;
	last = 3;
	line[0] = bufp;
	BEGIN(X);
}

^"\\xfour"[ \t\n]+ {
	ECHO;
	last = 4;
	line[0] = bufp;
	BEGIN(X);
}

^"\\x"[ \t\n]+ {
	ECHO;
	last = 1;
	line[0] = bufp;
	BEGIN(X);
}
<X>"$" {
	printf("\\$");
	ADDCH('$');
}
<X>"\\ " {
	printf("\\xbs{\\ }");
	ADDS(yytext);
}
<X>\\[a-z]+ {
	printf("\\xbs{%s}", yytext+1);
	ADDS(yytext);
}
<X>\\. {
	printf("\\xbs{%c}", yytext[1]);
	ADDS(yytext);
}
<X>: {
	ECHO;
	ADDCH(0);
	count++;
	line[count] = bufp;
}
<X>"." {
	ECHO;
	if (count < last) ADDCH('.');
    else {
	ADDCH(0);

	printf("\n\\smallbreak{\\parindent=.5in\\par");
	printf("\\hskip-.2in\\it gives:\\tfont\n\\tree ");
	for (i = 0; i < count; i++)
		printf("%s\n", line[i]);
	printf("}\\smallbreak\n");

	count = last = 0;
	bufp = buf;
	BEGIN(0);
    }
}
<X>. {
	ECHO;
	ADDCH(yytext[0]);
}

%%
main()
{	char *malloc();

	buf = bufp = malloc(BUFSIZ);
	yylex();
}
