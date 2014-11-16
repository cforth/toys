%{
/* tree: format trees
 * Version 1.1.1 -- options added for ibmpc extended characters,
 *		July, 1991, gl.
 * Version 1.1 -- Greg Lee, lee@uhccux.uhcc.hawaii.edu, June 24, 1990
 *
 * This program is free and in the public domain.  Please keep future
 * versions in the public domain.
 *
 * The inspiration for and predecessor to `tree' was a program by
 * Chris Barker, of the Linguistics Board at University of California,
 * Santa Cruz, email: barker@ling.ucsc.edu.
 *
 * A pattern matching function yylex() is built, which finds tree
 * definitions in a text;  yylex() is called recursively to build
 * a tree structure in memory;  a sequence of formatting operations
 * is carried out (see printtree()); then the formatted tree is
 * displayed by tty() or, for TeX code, the function tex().
 */
#include <ctype.h>

#define TRUE 1
#define FALSE 0

/* When formatting for TeX, multiply column widths by this to get better
 * positioning:
 */
#define COLMUL 8

/* The c_ values are from the command line; the real values are taken
 * from them or from options given after the \tree command.
 */
    int     tex_opt, c_tex_opt = FALSE;	/* generate TeX code? */
    int     utex_opt, c_utex_opt = FALSE;/* generate TeX code with PS? */
    int     gap_opt, c_gap_opt = 2;	/* space between subtrees */
    int     black_opt, c_black_opt = 0;	/* black triangles */
    int     debug_opt = FALSE;	/* tracing? */
    int     stats_opt = FALSE;	/* report statistics? */
    int     quiet_opt, c_quiet_opt = FALSE;	/* no warnings */
    int     verbose_opt, c_verbose_opt = FALSE; /* show tex commands? */
    int     lexical_opt, c_lexical_opt = FALSE;  /* no lines */
    int     T_opt, c_T_opt = FALSE;
    int     O_opt, c_O_opt = FALSE;
    int     I_opt, c_I_opt = FALSE;
    int     F_opt, c_F_opt = FALSE;
    int     E_opt, c_E_opt = FALSE;
    int     R_opt, c_R_opt = FALSE;
    int     x_opt, c_x_opt = FALSE;
    int     X_opt, c_X_opt = FALSE;

/* count columns before \tree command encountered */
    int     indent = 0;
/* count caps in name to compensate for extra width */
    int     capscount = 0;
/* keep track of recursion in yylex() calls to assign nodes to rows */
    int     level = 0;
    int     maxlevel = 0;
/* for statistics report */
    int     maxcol = 0;
/* source line (not useful now -- need some error checking) */
    int     linenumber = 1;

/* types of nodes */
#define HBAR 1			/* horizontal bar */
#define VBAR 2			/* vertical bar */
#define OBAR 4			/* horizontal overbar */
#define NODENAME 8		/* named node */

#define NAMEROOM 20000		/* how much to malloc for node names */
char	*buf, *bufp;		/* for buffer storing node names */

/* A node has a:
 *	row, from row 1, telling how far from the top of the tree it is;
 *	col, from col 0, how far from the left;
 *	mid, its horizontal mid point, used for vertical alignment;
 *	l, its width in columns;
 *	treeid, an identifying number;
 *	type, whether its a name or a bar of some sort;
 *	attrib, a list of 26 values of attributes bestowed by \<cap>s;
 *	n, pointer to its name if it has one;
 *	and a bunch of pointers to contiguous nodes in the tree.
 *
 * Attributes `S' and `U' are used internally;  must change this if
 * there are to be \S or \U commands.
 */
typedef struct list {
	int row, col, mid, l, treeid, type;
	char attrib[26];
	char *n;
	struct list *daughter;
	struct list *sister;
	struct list *mother;
	struct list *right;
	struct list *left;
} LIST, *TREE;

/* next number for treeid */
int treenum = 1;

TREE newnode();

/* global reference by yylex() */
TREE tree;

#define ERROR(message) fprintf(stderr,"Tree: %s (line %d).\n", \
		message, linenumber)

/* Next is code for flex to build the yylex() function.  There are three
 * states the pattern matcher can be in:
 *	T, if it's matching text after the \tree command that defines
 *		a tree;
 *	N, if it's echoing text that is not in the scope of a \tree command;
 *	C, if it's discarding comments within the definition of a tree.
 */
%}

%s T N C

%%
<N>\n {
	indent = 0;
	linenumber++;
	ECHO;
}
<N>\t {
	indent++;
	while (indent % 8) indent++;
	ECHO;
}
<N>. {
	indent++;
	ECHO;
}
<N>\\tree[ \t\n]*(-([tuvqLTOIFER]+|[bg][0-9]+)[ \t\n]*)*\([ \t\n]* {
	TREE root;

	setoptions(yytext + 5);
	level++;
	if (level > maxlevel) maxlevel = level;
	root = newnode(level,bufp);
	tree = root;
/* do a whole tree: in state T analyze the tree definition
 * and build the tree; format and display, and resume echoing
 * text until the next tree definition is found.
 */
	BEGIN(T);
	yylex();
	printtree(root);
	maxlevel = 0;
	BEGIN(N);
}
<N>\\tree {
	if (!quiet_opt) ERROR("ill-formed \\tree command ignored");
	ECHO;
}
<T,C>\([ \t\n]* {
	TREE node;

	notenewlines(yytext);
	level++;
	if (level > maxlevel) maxlevel = level;
	addchar('\0');	/* terminate last node name */
	capscount = 0;	/* no caps in next name yet */
	node = newnode(level,bufp);
/* nodes at same level of embedding are connected together as
 * sisters; but if current level is greater than that of
 * the node that was just being made, this next node must be
 * a daughter of that node.
 */
	if (tree->row < level) tree->daughter = node;
	else tree->sister = node;
	tree = node;
	BEGIN(T);
	yylex();
	tree = node;
}
<T,C>\) {
	level--;
	addchar('\0');
	capscount = 0;
/* discard text now until the beginning of the next node
 */
	BEGIN(C);
/* this is a return from a yylex() invocation called from yylex().
 */
	return;
}
<T>[ \t\n]+\\% {
	notenewlines(yytext);
	addchar(' ');
	if (tex_opt || verbose_opt) {
		addchar('\\');
		tree->l++;
	}
	addchar('%');
	tree->l += 2;
}
<T>\\[%#\&\$] {
	if (tex_opt || verbose_opt) {
		addchar('\\');
		tree->l++;
	}
	addchar(yytext[1]);
	tree->l++;
}
<T,C>%.*\n {
	notenewlines(yytext);
}
<T,C>[ \t\n]*%.*\n[ \t\n]*/[\)\(] {
	notenewlines(yytext);
}
<T>\\[MDB][0-9][ \t\n]+ {
	giveval(tree, yytext[1], yytext[2]);
}
<T>\\[MDB][0-9]/[^A-Za-z] {
	giveval(tree, yytext[1], yytext[2]);
}
<T>\\[A-Z][ \t\n]+ {
	give(tree, yytext[1]);
}
<T>\\[A-Z]/[^A-Za-z] {
	give(tree, yytext[1]);
}
<T>\\[ )(\\] {
	addchar(yytext[1]);
	tree->l++;
}
<T>(\\[`'"^~=.])|(\$[_^]) {
	if (tex_opt || verbose_opt) {
		addchar(yytext[0]);
		addchar(yytext[1]);
		if (verbose_opt) tree->l += 2;
	}
}
<T>[\${}] {
	if (tex_opt || verbose_opt) {
		addchar(yytext[0]);
		if (verbose_opt) tree->l++;
	}
}
<T>[A-HJ-Z] {
	addchar(yytext[0]);
	tree->l++;
	if (tex_opt && ++capscount > 3) {
		tree->l++;
		capscount = 0;
	}
}
<T>. {
	addchar(yytext[0]);
	tree->l++;
}
<T>\\tree[ \t\n]* {
	if (!quiet_opt) ERROR("\\tree command found inside tree");
	notenewlines(yytext);
	if (tex_opt || verbose_opt) {
		int i;
		for (i = 0; i < yyleng; i++) {
			addchar(yytext[i]);
			if (verbose_opt) tree->l++;
		}
	}
}
<T>\\[A-Za-z]+[ \t\n]* {
	notenewlines(yytext);
	if (tex_opt || verbose_opt) {
		int i;
		for (i = 0; i < yyleng; i++) {
			addchar(yytext[i]);
			if (verbose_opt) tree->l++;
		}
	}
}

<T>[ \t\n]+/[\)\(] {
	notenewlines(yytext);
}
<T>[ \t\n]+ {
	notenewlines(yytext);
	if (tree->l) {	
		addchar(' ');
		tree->l++;
	}
}
<C>[^ \t\n\(\)]+ {
	if (!quiet_opt) ERROR("word after node name ignored");
}
<C>.	;
<C>\n	linenumber++;

%%

/* count newlines in string; update linecount; issue warning if
 * blank line
 */
notenewlines(s)
char *s;
{	int warn = 0;
	while (*s) {
		if (*s == '\n') {
			if (warn && !quiet_opt)
				ERROR("blank line within tree");
			else warn++;
			linenumber++;
		}
		else if (*s != ' ' && *s != '\t') warn = 0;
		s++;
	}
}

/* Called for every \tree in input.  Resets option values from defaults
 * established on command line.
 */
setoptions(s)
char *s;
{   int c, gap = -1;

    tex_opt = c_tex_opt;
    utex_opt = c_utex_opt;
    gap_opt = c_gap_opt;
    black_opt = c_black_opt;
    verbose_opt = c_verbose_opt;
    quiet_opt = c_quiet_opt;
    lexical_opt = c_lexical_opt;
    T_opt = c_T_opt;
    O_opt = c_O_opt;
    I_opt = c_I_opt;
    F_opt = c_F_opt;
    E_opt = c_E_opt;
    R_opt = c_R_opt;
    x_opt = c_x_opt;
    X_opt = c_X_opt;

    while (c = *s++)
	switch (c) {
	    case 't': tex_opt = TRUE; utex_opt = FALSE; break;
	    case 'u': utex_opt = TRUE; tex_opt = TRUE; break;
	    case 'g': gap = gap_opt = atoi(s); break;
	    case 'b': black_opt = atoi(s); break;
	    case 'v': verbose_opt = TRUE; break;
	    case 'q': quiet_opt = TRUE; break;
	    case 'L': lexical_opt = TRUE; break;
	    case 'T': T_opt = TRUE; break;
	    case 'O': O_opt = TRUE; break;
	    case 'I': I_opt = TRUE; break;
	    case 'F': F_opt = TRUE; break;
	    case 'E': E_opt = TRUE; break;
	    case 'R': R_opt = TRUE; break;
	    case 'x': x_opt = TRUE; break;
	    case 'X': X_opt = TRUE; x_opt = TRUE; break;
	    case '\n': linenumber++; break;
	}
    if (gap >= 0 && tex_opt) gap_opt *= COLMUL;
}


extern char *optarg;		/* from getopt */
extern int  optind;

main(argc, argv)
int     argc;
char   *argv[];
{	int c;
	char *progname = NULL, *basename();

	if ( (bufp = buf = (char *)malloc(NAMEROOM)) == 0 ) {
		fprintf(stderr, "can't get memory space\n");
		exit(1);
	}

	progname = basename (argv[0]);
	while ((c = getopt (argc, argv, "hg:tub:vLTOIFERdqsxX")) != EOF)
		switch (c) {
			case 'g': c_gap_opt = max(0, atoi(optarg)); break;
			case 't': c_tex_opt = TRUE; break;
			case 'u': c_utex_opt = TRUE; c_tex_opt = TRUE; break;
			case 'b': c_black_opt = max(0, atoi(optarg)); break;
			case 'v': c_verbose_opt = TRUE; break;
			case 'd': debug_opt = TRUE; break;
			case 's': stats_opt = TRUE; break;
			case 'q': c_quiet_opt = TRUE; break;
			case 'L': c_lexical_opt = TRUE; break;
			case 'T': c_T_opt = TRUE; break;
			case 'O': c_O_opt = TRUE; break;
			case 'I': c_I_opt = TRUE; break;
			case 'F': c_F_opt = TRUE; break;
			case 'E': c_E_opt = TRUE; break;
			case 'R': c_R_opt = TRUE; break;
			case 'x': c_x_opt = TRUE; break;
			case 'X': c_X_opt = TRUE; c_x_opt = TRUE; break;
			case 'h':
	    		default: 
		   fprintf(stderr, "Usage: %s [options] [files]\n", progname);
		   fprintf(stderr, "options = -gnum\t(gap between subtrees)\n");
		   fprintf(stderr, "          -h\t(print this information)\n");
		   fprintf(stderr, "          -t\t(TeX code)\n");
		   fprintf(stderr, "          -u\t(TeX code w. diagonals)\n");
		   fprintf(stderr, "          -bnum\t(black triangles)\n");
		   fprintf(stderr, "          -v\t(show TeX commands)\n");
		   fprintf(stderr, "          -q\t(quiet)\n");
		   fprintf(stderr, "          -L\t(lexical)\n");
		   fprintf(stderr, "          -T\t(triangles)\n");
		   fprintf(stderr, "          -O\t(omit lines)\n");
		   fprintf(stderr, "          -I\t(invert)\n");
		   fprintf(stderr, "          -F\t(flatten)\n");
		   fprintf(stderr, "          -E\t(even)\n");
		   fprintf(stderr, "          -R\t(relational)\n");
		   fprintf(stderr, "          -x,X\t(extended screen chars)\n");
		   exit(1);
		}

	/* doubled column values for tex code */
	if (c_tex_opt) c_gap_opt *= COLMUL;

	BEGIN(N);

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
			if (level) {
			    fprintf(stderr,"Unbalanced parens in file: %s\n",
				argv[optind]);
			    exit(1);
			}
		}
		else {
			(void) fprintf (stderr,
			    "Couldn't open file: %s\n", argv[optind]);
			exit (1);
		}
	}
	if (level) {
		fprintf(stderr,"Unbalanced parens.\n");
		exit(1);
	}
	if (stats_opt) {
		if (tex_opt) maxcol /= COLMUL;
		fprintf(stderr,"Maximimum column was %d.\n", maxcol);
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

max(a, b)
int a, b;
{
	return ((a > b) ? a : b);
}

TREE newnode(row, n)
int  row;
char *n;
{	TREE temp;
	int i;

	temp = (TREE) malloc (sizeof (LIST));
	if (!temp) {
		ERROR("out of memory");
		exit(1);
	}
	temp->daughter = NULL;
	temp->sister = NULL;
	temp->mother = NULL;
	temp->right = NULL;
	temp->left = NULL;
	temp->n = n;
	temp->l = 0;
	temp->row = row;
	temp->col = 0;
	temp->mid = 0;
	temp->treeid = treenum++;
	temp->type = NODENAME;
	for (i = 0; i < 26; i++) temp->attrib[i] = '\0';
	if (lexical_opt) give(temp,'L');
	if (T_opt) give(temp,'T');
	if (O_opt) give(temp,'O');
	if (R_opt) give(temp,'R');
	return (temp);
}

/* append one node name character in buffer;  this is called only
 * from within yylex().
 */
addchar(c)
char c;
{
	*bufp++ = c;
}

/* after yylex() has built an in-memory tree structure, printtee()
 * formats and displays it.
 */
printtree(root)
TREE root;
{	TREE over;

	addbars(root, 0);		    /* put in VBARs and HBARs         */
	flatbars(root, maxlevel);	    /* interpret \E and \F commands   */
	rectify(root);			    /* `left' links for row/col order */
	addlinks(root);			    /* miscellaneous initialization   */
	over = newnode(0, NULL);	    /* preliminary to calling align:  */
	over->daughter = root;		    /*    new node is needed for the  */
	root->mother = root->left = over;   /*    case of an inverted root    */
	if (I_opt) {
	/* for side-by-side trees, interpret -I option as meaning that
	 * each tree should be inverted individually
	 */
	    if (root->l) give(root,'I');
	    else if (root->daughter) {
		TREE node = root->daughter;
		if (node->type == HBAR) node = node->daughter;
		if (node->type == VBAR)
			while (node && node->type == VBAR) {
				give(node->daughter,'I');
				node = node->sister;
		}
		else while (node) {
				give(node,'I');
				node = node->sister;
		}
	    }
	}
	align(root);			    /* assign column values for       */
					    /*    vertical alignment          */
	root = over->daughter;		    /* root will be a different node  */
					    /*    if it was just inverted     */
	free(over);
	if (debug_opt) {
		fprintf(stderr,"\n\n\t------ROOT------\n");
		debugprint(root);
	}
	if (!root->l) {			    /* remove empty top nodes to get  */
					    /*    side-by-side trees          */
		TREE old;
		if (root->daughter) {
			old = root;
			root = root->daughter;
			free(old);
		}
		if (root->type == HBAR && root->daughter) {
			TREE node;
			old = root;
			root = root->daughter;
			free(old);
		/* mothers of roots are made NULL to block the middle
		 * vertical of an HBAR for tty output
		 */
			if (root->type == VBAR && root->daughter) {
			    for (node = root; node; node = node->sister)
			      if (node->daughter) node->daughter->mother = NULL;
			    old = root;
			    root = root->daughter;
			    free(old);
			}
		}
		else if (root->type == VBAR && root->daughter) {
			old = root;
			root = root->daughter;
			free(old);
		}
		root->mother = NULL;
	}
	if (tex_opt) tex(root);	/* now display */
	else tty(root);
	bufp = buf;		/* can reuse name buffer for next tree */
	freenodes(root);
}

freenodes(tree)
TREE tree;
{	TREE next;

	while (tree) {
		next = tree->right;
		free(tree);
		tree = next;
	}
}


/* b is from the value given for the -b option */
int b;
/* these are the characters used to draw screen trees; the arrays
 * are indexed by variable b above:
 *			( >=10 with -x,-X options)
 *			  1111111111
 *	b =	01234567890123456789
 */
char tf[]    = "_-:|::|-|*H012465333";	/* triangle fill */
char itf[]   = "~-:|::|-|*H012465333";	/* inverted triangle fill */
char vb[]    = "||:|::||||VVvv465VV3";	/* vertical bar */
char lhb[]   = "_-.|:._<//HDDD465Eh3";	/* left part of horizontal bar */
char rhb[]   = "_-.|:._>BBHDDD465Fh3";	/* right part of horizontal bar */
char ilhb[]  = "~-Q|:Q^<BBHDDD465Eh3";	/* left of inverted horizontal bar */
char irhb[]  = "~-Q|:Q^>//HDDD465Fh3";	/* right of inverted horizontal bar */
char lvb[]   = "_-.|://<//HDDD465E33";	/* left of vertical centerpiece */
char mvb[]   = "|+:|:     MNKK465M33";	/* middle of vertical centerpiece */
char imvb[]  = "|+:|:     mnkk465m33";	/* i'd middle of vertical centerpiece */
char rvb[]   = "_+.|:BB>BBHDDD465F33";	/* right of vertical centerpiece */
char lcb[]   = "||:|://///VVvv465VV3";	/* vertical for left sister */
char rcb[]   = "||:|:BBBBBVVvv465VV3";	/* vertical for right sister */
char lchb[]  = "_+ |:     Idoo   II3";	/* left corner of horizontal bar */
char rchb[]  = "_+ |:     Jepp   JJ3";	/* right corner of horizontal bar */
char ilchb[] = "_+ |:     ifqq   ii3";	/* left corner of inv'd horizontal bar */
char irchb[] = "_+ |:     jgrr   jj3";	/* right corner of inv'd horizontal bar */
char headb[] = "********************";	/* head */

putxchar(c)
int c;
{	int i, cc;

	cc = c;
	switch(c) {
	    case 'B': cc = '\\'; break;
	    case 'Q': cc = '\"'; break;
	    case 'V': cc = 179; break;
	    case 'v': cc = 186; break;
	    case 'H': cc = 196; break;
	    case 'D': cc = 205; break;
	    case 'd': cc = 213; break;
	    case 'e': cc = 184; break;
	    case 'f': cc = 212; break;
	    case 'g': cc = 190; break;
	    case 'o': cc = 201; break;
	    case 'p': cc = 187; break;
	    case 'q': cc = 200; break;
	    case 'r': cc = 188; break;
	    case 'h': cc = 220; break;
	    case 'I': cc = 218; break;
	    case 'E': cc = 174; break;
	    case 'F': cc = 175; break;
	    case 'i': cc = 192; break;
	    case 'J': cc = 191; break;
	    case 'j': cc = 217; break;
	    case 'M': cc = 193; break;
	    case 'm': cc = 194; break;
	    case 'N': cc = 207; break;
	    case 'K': cc = 202; break;
	    case 'k': cc = 203; break;
	    case '0': cc = 176; break;
	    case '1': cc = 177; break;
	    case '2': cc = 178; break;
	    case '3': cc = 219; break;
	    case '4': cc = 248; break;
	    case '5': cc = 249; break;
	    case '6': cc = 250; break;
	}
	if (cc >= 128 && X_opt) putchar(27);
	putchar(cc);
	if (cc >= 128 && X_opt) putchar(28);
}

/* display tree for screen */
tty(root)
TREE root;
{	TREE node;
	int row = root->row, col = 0, i;

	if (debug_opt) {
		putchar('\n');
		for (col = 0; col < indent; col++) putchar(' ');
		col = 0;
	}

	/* display each node, left-to-right and top-to-bottom */
	for (node = root; node; node = node->right) {

		/* boldness is from \B command or -b option */
		if (b = has(node,'B')) {
			if (b == '+') b = 9;
			else if (isdigit(b)) b -= '0';
			else b = 0; /* presumably impossible */
		}
		else for (b = black_opt; b > 10; b /= 10) ;

		if (x_opt) b += 10;

		/* newline and indentation */
		if (node->row > row) {
			while (node->row > row) { putchar('\n'); row++; }
			for (col = 0; col < indent; col++) putchar(' ');
			col = 0;
		}

		/* spacing between nodes */
		for ( ; node->col > col; col++) putchar(' ');

		/* disconnect illegitimate sisters created by inversion */
		if (node->sister && node->sister->mother != node->mother)
			node->sister = NULL;

		/* display a node in a way appropriate to its type */
		switch (node->type) {
			case NODENAME:
			    if (has(node,'P')) /* space over phantom node */
				for (i = 0; i < node->l; i++) putchar(' ');
			    else printf("%s", node->n);
			    break;
			case VBAR:
			    /* join all verticals at the base of a triangle */
			    if (has(node,'T') && !has(node,'O')) {
				char hbar = tf[b];
				/* no vertical if this is not the first or
				 * only sister
				 */
				if (has(node,'S') != 'f'
				     && has(node,'S') != 'o') {
					for (i = 0; i < node->l; i++)
						putchar(' ');
					break;
				}
				/* use special fill character for base of
				 * inverted triangle
				 */
				if (node->mother && node->mother->type == OBAR)
					hbar = itf[b];
				/* make left edge of base */
				putxchar(vb[b]);
				/* when only one node at base, length of base
				 * is length of node
				 */
				if (has(node,'S') == 'o')
				    for (i = 2; i < node->l; i++)
					putxchar(hbar);
				/* but when there are several nodes at the
				 * base, the base goes from the first to the
				 * last sister
				 */
				else {
				    while (node->sister
				      && node->mother == node->sister->mother
				      && has(node,'S') != 'l'
				      && node->sister->type == VBAR)
					node = node->sister;
				    for ( ; node->col > col+1; col++)
					putxchar(hbar);
				    col++;
				}
				/* make the right edge of the base */
				putxchar(vb[b]);
				break;
			    } /* end of code for triangle bases */

			    /* space over omitted or phantom lines */
			    if (has(node,'O') || has(node,'P')) putchar(' ');
			    /* possibly do a bold vertical */
			    else if (!blackvbar(node))
				/* do a plain vertical */
				putxchar(vb[b]);
			    break;

			case HBAR:
			    /* possibly do a bold hbar */
			    if (node->l >= 4 && blackhbar(node)) break;
			    /* otherwise, make the left side, */
			    putxchar(lchb[b]);
			    for (i = 1; i < node->mid; i++) putxchar(lhb[b]);
			    /* ... then the middle */
			    if (node->mother) putxchar(mvb[b]);
			    else putxchar(lhb[b]);
			    /* ... then the right side */
			    for (i = 1; i < node->l - node->mid - 1; i++)
				putxchar(rhb[b]);
			    putxchar(rchb[b]);
			    break;

			case OBAR:
			    /* similar to hbar, above */
			    if (node->l >= 4 && blackobar(node)) break;
			    putxchar(ilchb[b]);
			    for (i = 1; i < node->mid; i++) putxchar(ilhb[b]);
			    if (node->mother && node->right) putxchar(imvb[b]);
			    else putxchar(ilhb[b]);
			    for (i = 1; i < node->l - node->mid - 1; i++)
				putxchar(irhb[b]);
			    putxchar(irchb[b]);
			    break;
		} /* end of switch */

		col += node->l;
		if (col + indent > maxcol) maxcol = col + indent;

	} /* end of loop to display each node */
}


/* draw horizontal bar with corners missing and a centerpiece */
blackhbar(node)
TREE node;
{	int i, lless;

	/* don't do it if no boldness requested or a \Head has forced
	 * the "midpoint" of the hbar to one end
	 */
	if (!b || b == 10 ||
		!node->mid || node->mid +1 >= node->l) return(FALSE);

	/* make the center of the bar a little to the left, usually,
	 * for even-length bars, so the two parts of the centerpiece
	 * tend to come under the middle two characters of the name above
	 */
	lless = (node->l % 2) ? 2 : 1;

	/* the left corner */
	putxchar(lchb[b]);

	/* the left segment before the centerpiece */
	for (i = lless; i < node->mid; i++) putxchar(lhb[b]);

	/* lower levels of bolding look better with a one-char
	 * centerpiece
	 */
	if (b < 3 || b > 9) {
		if (lless == 2) putxchar(lhb[b]);
		putxchar(mvb[b]);
		putxchar(rhb[b]);
	}
	else {
	/* the two-char centerpiece */
		putxchar(lvb[b]);
		if (lless == 2) putxchar(mvb[b]);
		putxchar(rvb[b]);
	}

	/* now the right segment before the corner */
	for (i = 3; i < node->l - node->mid; i++)
		putxchar(rhb[b]);

	/* finally the right corner */
	putxchar(rchb[b]);

	/* yes, we did one */
	return(TRUE);
}

/* as above, but for inverted trees */
blackobar(node)
TREE node;
{	int i, lless;

	if (!b || b == 10 ||
		!node->mid || node->mid +1 >= node->l) return(FALSE);

	lless = (node->l % 2) ? 2 : 1;
	putxchar(ilchb[b]);
	for (i = lless; i < node->mid; i++) putxchar(ilhb[b]);
	if (b < 3 || b > 9) {
		if (lless == 2) putxchar(ilhb[b]);
		putxchar(imvb[b]);
		putxchar(irhb[b]);
	}
	else {
		if (b % 10 == 7) putxchar(lvb[b]);
		else putxchar(rvb[b]);
		if (lless == 2) putxchar(imvb[b]);
		if (b % 10 == 7) putxchar(rvb[b]);
		else putxchar(lvb[b]);
	}
	for (i = 3; i < node->l - node->mid; i++)
		putxchar(irhb[b]);
	putxchar(irchb[b]);
	return(TRUE);
}

/* draw corner sisters appropriate to horizontal above them */
blackvbar(node)
TREE node;
{
	/* don't do it when no boldness was asked for, or there is
	 * no node name above, or the hbar above was too short to
	 * be made bold
	 */
	if (!b || b == 10 || !node->mother || node->mother->l < 4)
		return(FALSE);
	/* mark heads */
	if ((b % 10) >= 5 && has(node,'H')) {
		putxchar(headb[b]);
		return(TRUE);
	}
	/* if it's the first sister, use a corner char */
	if (has(node,'S') == 'f') {
		if (node->mother->type == HBAR) {
			putxchar(lcb[b]);
			return(TRUE);
		}
		if (node->mother->type == OBAR) {
			putxchar(rcb[b]);
			return(TRUE);
		}
	}
	/* likewise if its the last sister, but use the other corner char */
	else if (has(node,'S') == 'l') {
		if (node->mother->type == HBAR) {
			putxchar(rcb[b]);
			return(TRUE);
		}
		if (node->mother->type == OBAR) {
			putxchar(lcb[b]);
			return(TRUE);
		}
	}
	return(FALSE);
}

/* take care of spacing between daughters of a branching node, and
 * figure width of the sisters; called by align()
 */
sisterbal(tree)
TREE tree;
{
	TREE temp, first, last, head = NULL;
	int hblen, rlen, bestspace, space, numdaughters = 1, leeway;
	int join = FALSE;

	/* figure which sisters are to be covered by the bar; mark them
	 * for convenience later in display routines
	 */
	for (first = tree->daughter; has(first,'O') && first->sister;
		 first = first->sister);
	for (last = first; last->sister; last = last->sister);
	while (has(last,'O') && last != first) last = last->left;
	giveval(first,'S','f');
	giveval(last,'S','l');

	/* look for heads and nodes that came from the bottom of inverted
	 * subtrees -- we must not try to balance the latter
	 */
	for (temp = first; temp != last; temp = temp->sister) {
		numdaughters++ ;
		if (has(temp, 'H')) head = temp;
		if (has(temp->sister, 'H')) head = temp->sister;
		if (has(temp, 'I') == 2) join = TRUE;
		if (has(temp->sister, 'I') == 2) join = TRUE;
	}

	/* first approximation to the length of the bar */
	hblen = (last->col + last->l) - first->col;
	rlen = (last->col + last->mid + 1/*COLMUL*/) - (first->col + first->mid);

	/* first, try to adjust in a way that does not require
	 * widening the bar
	 */
	if (numdaughters > 2) bestspace = rlen / (numdaughters - 1);
	else bestspace = 0;
	if (!join) for (temp = first; temp != last; temp = temp->sister) {
		space = temp->sister->col + temp->sister->mid
			 - (temp->col + temp->mid);
		leeway = rightroom(temp) - gap_opt;
		if (temp == first && numdaughters == 2) leeway /= 2;
		if (space > bestspace && leeway > 0) {
			space -= bestspace;
			if (space > leeway) space = leeway;
			moveright(temp, space);
			if (temp == first) {
			    hblen = (last->col + last->l)
				 - tree->daughter->col;
			    rlen = (last->col + last->mid + 1/*COLMUL*/)
				- (first->col + first->mid);
			    bestspace = rlen / (numdaughters - 1);
			}
		}
	}
	bestspace = 0;

	/* then look for the widest space between adjacent sisters, and
	 * widen the space between others to match
	 */
	if (!join) for (temp = first; temp != last; temp = temp->sister) {
		if ((space = temp->sister->col + temp->sister->mid
			- (temp->col + temp->mid)) > bestspace)
			bestspace = space;
	}
	if (!join) for (temp = first; temp != last; temp = temp->sister) {
		if ((space = temp->sister->col + temp->sister->mid
			- (temp->col + temp->mid)) < bestspace)
			moveright(temp->sister, bestspace - space);
	}

	/* triangles with a single node at their bases are a special case */
	if (last == first && last->daughter) {
		hblen = last->daughter->l;
		last->l = last->daughter->l;
		last->col = last->daughter->col;
		giveval(last,'S','o');
	}
	/* revise hbar length and fill in lengths */
	else hblen = (last->col + last->l) - first->col;
	tree->l = hblen;
	if (head) tree->mid = head->col + head->mid - first->col;
	else tree->mid = (hblen - 1) / 2;
/* ( arguably, when slanty lines will be drawn, the length of the
 * hbar should be a little less -- must try this some day )
 */

	/* if the left edge of the hbar is to the right of the left
	 * edge of the first sister, align all the sisters now
	 */
	if ((space = tree->col - first->col) > 0) {
		for (temp = tree->daughter; temp; temp = temp->sister)
			moveright(temp, space);
		return(0);
	}
	/* otherwise, tell align() to move the hbar to the right */
	return(space);
}

/* assign col values to nodes for appropriate vertical alignments;
 * also call for inversion of trees with \Is
 */
align(tree)
TREE tree;
{	int diff, thisrow;
	TREE offspring, invert();

    if (tree) {
	/* the vbar of a relational node has already been aligned */
	if (has(tree,'R') && tree->type == VBAR) return;

	/* every node has to go at least far enough to the right to
	 * avoid bumping into the node on the left (if any)
	 */
	if (tree->left && tree->left->row == tree->row)
		tree->col = tree->left->col + tree->left->l + gap_opt;
	else tree->col = 0;

	/* force relational nodes to align on the vbar, by artifically
	 * considering the vbar to be at the "midpoint" of the node
	 */
	if (has(tree,'R') && tree->type == NODENAME && tree->sister) {
		tree->sister->col = tree->col + tree->l + gap_opt/4;
		tree->mid = tree->sister->col + tree->sister->mid - tree->col;
	}

	/* for non-terminal nodes, align the lower parts of the tree
	 * (cyclically), and calculate the displacement required to
	 * line this tree up above its offspring
	 */
        if (offspring = tree->daughter) {
	    align(offspring);
	    offspring = tree->daughter; /* may have different tree if inverted*/
	    diff = 0;
	    if (tree->type == HBAR) {
		/* do not change alignment of the top (formerly bottom)
		 * parts of an inverted subtree, since they are already
		 * properly aligned with nodes below them; but the whole
		 * subtree can be moved by its top left node
		 */
		if (has(tree,'I') == 1) diff = tree->col - offspring->col;
		else diff = sisterbal(tree);
	    }
	    /* the case of sisters which are not under an hbar can arise
	     * through use of \L; we center the tree over them
	     */
	    else if (has(offspring,'I') != 2 && has(offspring,'I') != 3
			 && offspring->sister && !has(offspring->sister,'R')) {
		TREE temp, first, last;
		for (first = offspring; has(first,'O') && first->sister;
			 first = first->sister);
		for (last = first; last->sister; last = last->sister);
		if (last == first) first = offspring;
		else while (has(last,'O') && last != first) last = last->left;
		for (temp = first; ; temp = temp->sister) {
			if (has(temp,'H')) first = last = temp;
			if (temp == last) break;
		}
		diff = tree->col + tree->mid
			- (first->col + first->mid
			   + last->col + last->mid)/2;
	    }
	    /* here the tree has a single daughter; line up the midpoints */
	    else {
		/* this propagates a mark up the tree that tells the
		 * sisterbal() routine not to change the alignment of
		 * an empty node that has been attached to part of an
		 * inverted tree, because that would undo the work we
		 * did in attaching it
		 */
		if (has(offspring,'I') == 2) giveval(tree,'I',2);
		diff = tree->col + tree->mid
			- (offspring->col + offspring->mid);
	    }

	    /* now actually do the alignment by moving either the tree
	     * or the offspring to the right, whichever is required
	     */
	    if (diff > 0) {
		moveright(offspring, diff);
		/* move the bar at the right of a relational node along
		 * with the node
		 */
		if (has(offspring->sister,'R')
			&& offspring->sister->type == VBAR)
		    offspring->sister->col += diff;
		/* this is a duplication of effort, I think, but it does
		 * have to be done here
		 */
		else align(offspring->sister);
	    }
	    else if (diff < 0) {
		tree->col -= diff;
		if (has(tree->sister,'R')) tree->sister->col -= diff;
	    }
	}

	/* in the case of a terminal node, there is ordinarily nothing
	 * to do, but it may be possible to align empty nodes with parts of
	 * an inverted subtree beneath them
	 */
	else if (tree->type == VBAR) { /* a terminal vbar is an "empty node" */
	/* An inverted subtree is connected to the rest by its upper left
	 * corner, which as been conveniently marked with an I-attribute
	 * value of 3.  We are going work our way to the left along the
	 * current row looking for such a corner, then if we find one,
	 * go down one row to the top row of the inverted subtree and
	 * work our way right an equal number of nodes to find a node to
	 * align with.  After the corner, nodes in this top row have been
	 * marked with an I-attribute value of 2, so we can tell when
	 * the search has failed.
	 */
	    TREE node = tree, invh = NULL;
	    int bcount = 1;
	    /* first work our way left: */
	    while (node->left && node->left->row == node->row) {
		if (debug_opt)
		    printf("\nAL: at #%d going left to #%d.",
			node->treeid,node->left->treeid);
		if (has(node->left->daughter,'I') == 3) {
			invh = node->left->daughter;
			break;
		}
		else {
			node = node->left;
			bcount++;
		}
	    }
	    /* then right an equal distance along top of inverted tree */
	    while (bcount && invh && has(invh->sister,'I') == 2) {
		if (debug_opt)
		    printf("\nAL: at #%d going right to #%d.",
			invh->treeid,invh->sister->treeid);
		invh = invh->sister;
		bcount--;
	    }
	    /* have we found one? yes, if we're still in the inverted
	     * tree and the node is not to the left of us (we can't
	     * move this tree node to the left -- only to the right)
	     */
	    if (has(invh,'I') == 2 && tree->col + tree->mid <= invh->col + invh->mid) {
		if (debug_opt)
		    printf("\naligning #%d over #%d.\n",
			tree->treeid,invh->treeid);
		/* do the alignment */
		tree->col = invh->col + invh->mid - tree->mid;
		/* mark as not subject to balancing by sisterbal() */
		giveval(tree,'I',2);
	    }
	} /* end alignment of terminal node */

	/* if inversion was requested, do it */
	if (has(tree,'I') == '+')
		tree = invert(tree);

	/* recurse left-to-right */
	align(tree->sister);
    }
}

/* do inversion of a tree; much global info in the tree has to be
 * kept correct, so this is hard;  the actual inversion is done
 * by inv(); invert() is called by align() just above
 */
TREE invert(tree)
TREE tree;
{	TREE mother, sister, node, inv();

	/* make all nodes in each row sisters; makes inversion easier,
	 * and makes it possible later to move the inverted tree around from
	 * above
	 */
	makelbranch(tree);
	/* save these links for later reattachment */
	mother = tree->mother;
	sister = tree->sister;
	tree->sister = NULL;
	tree = inv(tree, NULL);
	/* in the special case where a tree has VBARs at the top
	 * after inversion, put an HBAR over the VBARs
	 */
	if (tree->sister && mother && mother->type == VBAR
		&& tree->type == VBAR && tree->sister->type == VBAR
		&& (!mother->mother || mother->mother->type != HBAR)) {
			TREE last;
			for (last = tree->sister;
				last->sister && last->sister->type == VBAR;
				last = last->sister)
				 last->mother = mother;
			last->mother = mother;
			mother->type = HBAR;
			giveval(mother,'I',1);
			mother->l = last->col + last->l - tree->col;
			mother->mid = (mother->l - 1)/2;
	}
	/* otherwise mark the top row so align() can tell that these
	 * nodes are at the top of an inverted tree and can find the
	 * top left corner
	 */
	else if (mother && !(mother->type == VBAR && has(mother,'O'))) {
		for (node = tree; node; node = node->sister)
			giveval(node,'I',2);
		giveval(tree,'I',3);
	}
	/* it's possible that inversion has caused parts of the inverted
	 * tree to bump against things to the left;  now check for this
	 * and, to preserve internal alignment, when necessary move the
	 * entire subtree to the right
	 */
	for (node = tree; node; node = node->daughter) {
	    TREE temp;
	    int room;
	    if (node->left && node->left->row == node->row)
		if ((room = node->left->col + node->left->l + gap_opt
						- node->col) > 0)
		    for (temp = tree; temp; temp = temp->sister)
			moveright(temp, room);
	}
	/* if this corner of the tree is a vbar, should a line be drawn
	 * to an hbar above, or an obar below?  maybe both -- I really
	 * don't know
	 */
	tree->mother = mother; /* ?? */

	/* in -L trees, following not quite right */
	if (mother) {
		mother->daughter = tree;
	}
	/* reattach former sister to rightmost sister of top */
	while (tree->sister) tree = tree->sister;
	tree->sister = sister;

	return(tree);
}

/* see how much a tree could be moved to the right without coming
 * too close to anything following; called by sisterbal()
 */
rightroom(west)
TREE west;
{	int mingap = 10000, gap;
	TREE node, south = NULL;

	if (west) south = west->daughter;
	else return(0);
	while (west) {
		if (west->right && west->row == west->right->row) {
			gap = west->right->col - west->col - west->l;
			if (gap < mingap) mingap = gap;
		}
		node = south;
		south = west = NULL;
		while (node) {
			west = node;
			if (node->daughter) south = node->daughter;
			node = node->sister;
		}
	}
	return(mingap);
}

/* move a tree right by increasing col values */
moveright(tree, amount)
TREE tree;
int amount;
{
	while (tree) {
		tree->col += amount;
		if (tree = tree->daughter) {
			TREE sis;
			sis = tree->sister;
			while (sis) {
				moveright(sis, amount);
				sis = sis->sister;
			}
		}
	}
}

/* flip a tree organized as a stack of linked sets of sisters, keeping
 * left and right links correct; gah!; called by invert()
 */
TREE inv(tree,rest)
TREE tree, rest;
{	TREE temp, node, right, left, last, lastd;
	int row;

	if (tree) {
		temp = tree->daughter;
		tree->daughter = rest;

		for (node = tree; node; node = node->sister) {
		    if (node->type == HBAR) node->type = OBAR;
		    else if (node->type == OBAR) node->type = HBAR;
		    else if (node->type == VBAR) {
			/* this is so texvbar() can tell when to invert
			 * arrows when bold verticals have been requested
			 */
			if (has(node,'U') == 'i') giveval(node,'U','u');
			else giveval(node,'U','i');
		    }
		}

		row = tree->row;
		for (last = tree; last->sister; last = last->sister) ;
		right = last->right;
		left = tree->left;
		node = tree;
		while (node && node->daughter) {
			for (last = node; ;) {
				last->row = node->daughter->row;
				if (!last->sister) break;
				last = last->sister;
			}
			for (lastd = node->daughter; lastd->sister;
				lastd = lastd->sister) ;
			if (lastd->right) last->right = lastd->right;
			else last->right = node->daughter;
			if (node->daughter->left)
				node->left = node->daughter->left;
			last->right->left = last;
			if (node->left) node->left->right = node;
			node = node->daughter;
		}
		if (left) node->left = left;
		else node->left = last;
		for (last = node; ;) {
			last->row = row;
			if (!last->sister) break;
			last = last->sister;
		}
		last->right = right;
		if (right) right->left = last;
		if (left) left->right = node;

		if (debug_opt) { fprintf(stderr,"\n\nCalled inv():\n");
				 debugprint(tree); }
		return(inv(temp,tree));
	}
	else return(rest);
}

/* convert a tree to left-branching; this is a preliminary to inverting a tree;
 * called by invert()
 */
makelbranch(tree)
TREE tree;
{	TREE node, east, west, south, last;

	east = west = tree;
	while (tree) {
		for (node = east, last = south = NULL; ; node = node->right) {
			if (node->daughter) {
				last = node->daughter;
				if (!south) south = node->daughter;
				node->daughter = NULL;
			}
			if (node == west) break;
			else node->sister = node->right;
		}
		if (west->right == south) west->right = NULL;
		if (south && south->left == west) south->left = NULL;
		while (last && last->sister) last = last->sister;
		west = last;
		east->daughter = south;
		tree = east = south;
	}
}

/* initialize some links to contiguous nodes, and also lengths and
 * mid column values
 */
addlinks(tree)
TREE tree;
{
	while (tree) {
		if (tex_opt) tree->l *= COLMUL;
		tree->mid = (tree->l - 1) / 2;
		if (tree->right) tree->right->left = tree;
		if (tree->daughter) tree->daughter->mother = tree;
		if (tree->sister) tree->sister->mother = tree->mother;
		tree = tree->right;
	}
}

/* for debugging */
printnode(node)
TREE node;
{	int i;

	if (!node) {
		fprintf(stderr,"NIL");
		return;
	}
	if (node->type == VBAR)
		fprintf(stderr,"#%d | at %d/%d", node->treeid,
			node->col, node->row);
	else if (node->type == HBAR)
		fprintf(stderr,"#%d _|_ at %d/%d", node->treeid,
			node->col, node->row);
	else if (node->type == OBAR)
		fprintf(stderr,"#%d ^|^ at %d/%d", node->treeid,
			node->col, node->row);
	else fprintf(stderr,"#%d=%s at %d/%d", node->treeid, node->n,
			node->col, node->row);
	fprintf(stderr,"[");
	for (i = 0; i < 26; i++) {
		char c;
		if ((c = node->attrib[i]) == '+')
			fprintf(stderr,"%c", 'A'+i);
		else if (c)
			fprintf(stderr,"%c=%d", 'A'+i, c);
	}
	fprintf(stderr,"]");
}

/* for debugging */
debugprint(tree)
TREE tree;
{
	if (tree) {
		debugprint(tree->daughter);
		printnode(tree);
		if (tree->daughter) {
			fprintf(stderr," DAUGHTER:");
			printnode(tree->daughter);
		}
		if (tree->sister) {
			fprintf(stderr," SISTER:");
			printnode(tree->sister);
		}
		fprintf(stderr,"\n  ");
		if (tree->mother) {
			fprintf(stderr," MOM:");
			printnode(tree->mother);
		}
		if (tree->left) {
			fprintf(stderr," LEFT:");
			printnode(tree->left);
		}
		if (tree->right) {
			fprintf(stderr," RIGHT:");
			printnode(tree->right);
		}
		fprintf(stderr,"\n");
		debugprint(tree->sister);
	}
}

/* create new VBAR or HBAR node; called by addbars() */
TREE newbar(model, row, bartype)
TREE model;
int row, bartype;
{	TREE temp;
	int i;

	temp = newnode(row, NULL);
	temp->type = bartype;
	temp->l = 1;
	for (i = 0; i < 26; i++) temp->attrib[i] = model->attrib[i];

	/* bars get the following attributes only when above empty
	 * nodes (and that is done in addbars() when a NODENAME is
	 * removed)
	 */
	giveval(temp,'F',0);
	giveval(temp,'I',0);
	giveval(temp,'R',0);

	return(temp);
}

/* test node for value of attribute */
has(tree, attrib)
TREE tree;
char attrib;
{
	if (tree && attrib >= 'A' && attrib <= 'Z')
		return(tree->attrib[attrib - 'A']);
	else return(0);
}

/* give value of attribute to node */
giveval(tree, attrib, val)
TREE tree;
char attrib, val;
{	int prev;

	if (tree && attrib >= 'A' && attrib <= 'Z') {
		prev = tree->attrib[attrib - 'A'];
		tree->attrib[attrib - 'A'] = val;
		return(prev);
	}
	else return(0);
}

/* give `+' value of attribute to node */
give(tree, attrib)
TREE tree;
char attrib;
{
	return(giveval(tree, attrib, '+'));
}

/* stick in VBARs above name nodes, and HBARs under branching nodes;
 * also remove empty name nodes
 */
addbars(tree, addrows)
TREE tree;
int addrows;
{	TREE kin, mother, node, temp;
	int numsisters;

	if (tree) {
	    /* account for new rows created above by adding bars */
	    tree->row += addrows;
	    /* I don't think maxlevel is used now, but may as well
	     * keep it up to date
	     */
	    if (tree->row > maxlevel) maxlevel = tree->row;
	    /* add no bars directly under node with \L */
	    if (has(tree,'L')) {
		    /* for -F option, propagate F attribute up from a
		     * terminal to dominating \L nodes
		     */
		    if (F_opt && tree->daughter
			 && !has(tree->daughter->daughter,'F')) {
			give(tree,'F'); /* work up through higher \L nodes */
			giveval(tree->daughter,'F',0);
		    }
		    /* save reference for following business with R nodes */
		    node = tree;
		    /* go down and add bars to lower parts of tree */
		    tree = tree->daughter;
		    while (tree) {
			addbars(tree, addrows);
			tree = tree->sister;
		    }
		    /* for -R, propagate absence of R attribute up from
		     * terminals to dominating \L nodes
		     */
		    if (R_opt && !has(node->daughter,'R'))
			giveval(node,'R',0);
	    }
	    /* no \L command, so unless this is a terminal, we do want to
	     * add bars under it -- either just a vbar, or for branching
	     * nodes, an hbar and under that a vbar for each sister
	     */
	    else if (tree->daughter) {
		kin = mother = tree;
		tree = tree->daughter;
		/* nodes with \O will not be covered by an hbar, so count
		 * the sisters that will be covered, to decide whether
		 * this should appear as a branching node
		 */
		for (node = tree, numsisters = 0; node; node = node->sister)
			if (!has(node,'O')) numsisters++;
		/* for tty output, a triangle base needs 3 characters,
		 * and for triangles over single daughter nodes, the name
		 * may be too short
		 */
		if (!tex_opt && numsisters < 2 && tree->l < 3)
			giveval(kin,'T',0);
		/* triangles over single daughters do need an hbar, but
		 * otherwise unless there are at least 2 sisters to cover,
		 * no hbar is needed
		 */
		if (numsisters > 1 || (has(kin,'T')
				/* need at least one node at base */
					&& numsisters
				/* a vbar cannot serve as a good base */
					&& tree->l
				/* would get odd results over inverted tree */
					&& !has(tree,'I')
				      )
		   ) {
		    /* auto-evening for all branching nodes */
		    if (E_opt) give(kin,'E');
		    /* make the hbar and attach it */
		    temp = newbar(kin, tree->row + addrows, HBAR);
		    temp->mother = mother;
		    mother = temp;
		    temp->daughter = tree;
		    kin->daughter = temp;
		    /* shift lower parts of tree down one row */
		    addrows++;
		    kin = temp;
		}
		/* now add a vbar above the daughter and each sister */
		while (tree) {
		    temp = newbar(tree, tree->row + addrows, VBAR);
		    /* whether a vbar is part of a triangle is determined
		     * by node above, not the one below it, and similarly
		     * for bolding and \M labels
		     */
		    giveval(temp,'T',0);
		    giveval(temp,'B',has(mother,'B'));
		    giveval(temp,'M',0);
		    if (mother->type == NODENAME)
			giveval(temp,'M',has(mother,'M'));
		    if (has(mother,'T') && mother->type == HBAR && !has(temp,'O')) give(temp,'T');

		    /* attach the new bar */
		    temp->mother = mother;
		    if (tree == kin->daughter) kin->daughter = temp;
		    else kin->sister = temp;
		    /* finish attachment and work down the tree if this
		     * is a non-empty node
		     */
		    if (tree->l) {
			temp->daughter = tree;
			tree->mother = temp;
			addbars(tree, addrows+1);
		    }
		    /* but if it is an empty node, discard it after copying
		     * attributes that we wouldn't want to lose
		     */
		    else {
			addbars(tree, addrows);
			temp->daughter = tree->daughter;
			if (tree->daughter) tree->daughter->mother = temp;
			if (has(tree,'F')) give(temp,'F');
			if (has(tree,'I')) give(temp,'I');
		        giveval(temp,'M',has(tree,'M'));
			free(tree);
		    }
		    /* make the single-noded base of a triangle wide enough
		     * to cover the name below it, and cause the apex of
		     * such a triangle to be moved downward together with
		     * its base in case there is flattening
		     */
		    if (has(temp,'T') && numsisters == 1) {
			temp->l = tree->l;
			if (has(tree,'F')) {
				give(kin,'F');
				giveval(tree,'F',0);
			}
		    }
		    /* vbar takes over any link to sister at right */
		    kin = temp;
		    temp = tree->sister;
		    tree->sister = NULL;

		    /* add vertical to the right of relational node */
		    if (has(tree,'R') && tree->type == NODENAME && tree->l
			&& (!has(tree,'L') || has(tree->daughter,'R'))) {
			    TREE rtemp;
		    	    rtemp = newbar(tree, tree->row, VBAR);
			    give(rtemp,'R');
			    giveval(rtemp,'T',0);
			    giveval(rtemp,'O',0);
			    tree->sister = rtemp;
		    }
		    /* now loop to add vbar to sister, if any */
		    tree = temp;
		}
	    }
	    /* here it's a terminal node; do flatten it if -F option,
	     * but don't automatically display it as relational for -R opt.
	     */
	    else {
		if (F_opt) give(tree,'F');
		if (R_opt) giveval(tree,'R',0);
	    }
	} /* if (tree) */
}

/* find lowest node in tree, ignoring inverted subtrees */
howlow(tree)
TREE tree;
{	int row, low = 0;

	while (tree) {
		if (tree->row > low) low = tree->row;
		tree = tree->daughter;
		if (tree && (row = howlow(tree->sister)) > low) low = row;
		if (tree && tree->type == NODENAME && has(tree,'I')) break;
	}
	return(low);
}

/* increase row numbers */
movedown(tree, amount)
TREE tree;
int amount;
{
	while (tree) {
		tree->row += amount;
		movedown(tree->sister, amount);
		tree = tree->daughter;
	}
}

/* add VBARs to bring \F'd constituents downward */
flatbars(tree, bottom)
TREE tree;
int bottom;
{	TREE node, temp, next;
	int far = bottom;

	if (tree) {
	    if ( (tree->type == NODENAME || (tree->type == HBAR
		 	&& tree->mother && tree->mother->type == VBAR) )
		 && has(tree,'E') )
			bottom = howlow(tree);
	    if (!(node = tree->daughter)) {
		temp = tree->left;
		if (temp && temp->sister == tree) {
			node = tree;
			tree = temp;
		}
	    }
	    while (node) {
		next = node->sister;
		if (next) next->left = node;
		if (node->daughter) {
			if (has(node,'F')) far -= howlow(node) - node->row;
			else flatbars(node, bottom);
		}
		if (has(node,'F')) {
		    if (node->type == VBAR) far--;
		    while (node->row < far) {
			temp = newbar(node, node->row, VBAR);
			temp->daughter = node;
			if (has(node,'R') && node->sister) node->sister->row++;
			else {
				temp->sister = node->sister;
				node->sister = NULL;
			}
			node->row++;
			if (node == tree->sister && next) next->left = temp;
			if (node == tree->daughter) tree->daughter = temp;
			else if (node == tree->sister) tree->sister = temp;
			/*else ERROR("flatbars");*/
			if (!tree->sister) giveval(tree,'T',0);
			if (node->type == VBAR && has(node,'T'))
				giveval(node,'T',0);
			else giveval(temp,'T',0);
			node->mother = temp; /* ?? */
			tree = temp;
		    }
		    if (node->daughter) {
			movedown(node->daughter, node->row + 1
				- node->daughter->row);
		    }
		} /* end if (has(node,'F')) */
		tree = node;
		node = next;
	    } /* end if (node) */
	} /* end if (tree) */
}

/* initialize `left' links in one row of tree; called by rectify() */
TREE rectifyrow(prev, root, row)
TREE prev, root;
int row;
{	TREE node = root, last = NULL, temp;

	if (node && node->row <= row) {
		if (node->row == row) {
			prev->right = node;
			if (debug_opt) {
				fprintf(stderr,"\nLINK OF ");
				printnode(prev);
				fprintf(stderr," TO ");
				printnode(node);
			}
			last = prev = node;
		}
		else if (temp = rectifyrow(prev, node->daughter, row))
			last = prev = temp;
		if (temp = rectifyrow(prev, node->sister, row))
			last = prev = temp;
	}
	return(last);
}

/* initialize `left' links so can traverse tree in row-column order */
rectify(root)
TREE root;
{	TREE node = root;
	int row;

	for (row = 2; node = rectifyrow(node, root, row); row++) ;
}

/* all TeX code in is tex.c */
#include "tex.c"
