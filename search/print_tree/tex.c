

/*
 * With the -u option, TeX \special commands are used to include
 * PostScript commands into the PS file created by the PS driver
 * (dvi2ps, psdvi, dvips, dvitops, or whatever).  The driver should
 * not attempt repositioning or anything -- just copy to its output.
 * Some drivers may not be willing to do this, and others may need
 * the \special to begin with a certain keyword before they will do it.
 * Here is a list of those keywords I know about:
 *	"ps-string "
 *	"ps-string="
 *	"ps::"
 *	"pstext="
 * The following define is for this keyword; it might have to be set
 * to one of the above.  (My version of dvi2ps does not require a
 * keyword.)
 */
#ifndef SKEY
#define SKEY ""
#endif

/*
 * Dimensions are in terms of em and ex (of the current font), with
 * basic values assuming cmr 10, which has 1em = 10pt, 1ex = 4.31pt.
 *
 * Each character or space is reckoned to be 1/2 em, which is the
 * width of a digit in the cmr fonts.  However, each `col' unit in
 * the tree is a half-space wide -- 1/4 em, that is.
 *
 * The normal width of rules is .4pt, which becomes .04em.
 * The height of lines is that of a TeX \strut: 8.5pt above the
 * baseline and 3.5pt below, and in ex units:
 *	8.5pt/4.31=1.972ex
 *	3.5pt/4.31=0.81206ex
 * The horizontal bars made of "underlines" have vertical dimension
 * starting 3.5pt below the baseline and going up .4pt to:
 *	3.1pt/4.31=0.71925ex
 * The ones made of "overlines" go to 8.5pt and start .4pt lower:
 *	8.1pt/4.31=1.87935ex
 * Rule width is .4pt/4.31 = .09280742ex.
 */

float   hskip = 0;		/* amount to hskip before next box or bar */

dohskip () {
    /* must emit this even when hskip is 0 to get out of
     * vertical mode before an \hbox
     */
    printf ("\\hskip %.2fem", hskip);
    hskip = 0;
}

/* record keeping for lines connecting discontinuous constituents */
int m_ulabel[11];
int d_ulabel[11];

/*
 * Keep track of the attributes from the \M and \D label
 * commands.  For the first of a matching pair, save our treeid
 * in the ulabel array and issue PS commands to define the current
 * (x,y) coordinates with names corresponding to the treeid.  For
 * the second of a matching pair, issue PS commands to draw a
 * line back to the previous location.
 */
setiattrib(node, is_daughter)
TREE node;
int *is_daughter;
{
    int type = node->type;
    int iattrib = 0;

    if (type == VBAR && (iattrib = has(node,'D')) ) {
	/* this is a daughter label */
	*is_daughter = TRUE;
	/* ... unless we're in an inverted tree */
	/*if (node->mother && node->mother->type == OBAR)*/
	if (has(node,'U') == 'i')
		*is_daughter = FALSE;
	if (iattrib == '+') iattrib = 10;
	else iattrib -= '0';
	d_ulabel[iattrib] = node->treeid;
	/* if known already, get old treeid in iattrib, otherwise
	 * note with "-1" that current location must be defined
	 */
	if (m_ulabel[iattrib]) iattrib = m_ulabel[iattrib];
	else iattrib = -1;
    }
    else if ((type==HBAR || type==VBAR || type==OBAR)
				&& (iattrib = has(node,'M'))) {
	/* this is a mother label */
	*is_daughter = FALSE;
	/* ... unless we're an OBAR: */
	if (type == OBAR) *is_daughter = TRUE;
	if (type == VBAR && has(node,'U') == 'i') *is_daughter = TRUE;
	if (iattrib == '+') iattrib = 10;
	else iattrib -= '0';
	m_ulabel[iattrib] = node->treeid;
	if (d_ulabel[iattrib]) iattrib = d_ulabel[iattrib];
	else iattrib = -1;
    }

    if (debug_opt) printf("%% note iattrib %d\n", iattrib);

    return(iattrib);
}



/* TeX height and depth to be used in current line for strut, etc. */
float h, d;
/* used only in following routine, except also set in print_tex_tree */
int curr_row = -1;
/* look at entire row to see what the smallest height and depth we can
 * get away with are
 */
static
        set_hd (node)
        TREE node;
{   int     row_type = 0;
    int     top_row = node->row;

    if (top_row == curr_row) return;
    curr_row = top_row;
    while (node && (node->row == top_row)) {
	row_type |= node->type;
	node = node->right;
    }
    if (row_type & NODENAME) {
	if (debug_opt) printf("%% Next row needs a full size strut.\n");
	h = 1.972;
	d = .812;
    }
    else {
    /* Make rows without text for node names about 2/3 of normal size.
     */
	if (debug_opt) printf("%% Setting height + depth to 2 ex's.\n");
	h = 1.5;
	d = .5;
    }
}


/* Generate PS code for Bezier curve connecting discontinuous
 * constituents (needs work).  This has to be independent of scale
 * or translation of coordinate system, since the PS driver may
 * have changed these.
 */
curvegen(sf, is_daughter)
char *sf;
int is_daughter;
{
    if (is_daughter) printf("\\lower%1.3fex",d);
    else printf("\\raise%1.3fex",h);

    printf("\\hbox{\\special{%scurrentpoint ",SKEY);

  /* Daughter is at, say, (DX,DY) and mother at (MX,MY);
   * if we're now at the daughter, we need to calculate two
   * inflexion points, somehow.  (Even though the PS variable
   * is called "mom", if we're at a mother node, it's actually
   * a daughter.)
   */
  if (is_daughter) {
    printf("currentpoint pop mom%sy ",sf);	/* (DX,MY) */
    printf("mom%sx currentpoint exch pop ",sf);	/* (MX, (DY+MY)/2 ) */
    printf("mom%sy add 2 div ",sf);
  }
  else {
  /* We're at the mother, and the first inflexion point has to bend
   * us down, then the second has be up above the daughter so we hit
   * it going more or less downward.
   */
/* cpx */
    printf("currentpoint pop ");
/* cpy 2 mul dy sub */
    printf("currentpoint exch pop 2 mul mom%sy sub ",sf);
					/* (MX, MY*2 - DY)  */
/* dx */
    printf("mom%sx ",sf);
/* dy 2 mul cpy sub */
    printf("mom%sy 2 mul currentpoint exch pop sub ",sf);
					/* (DX, DY*2 - MY)   */
/* dx dy */
  }
    /* and wind up at (DX,DY) or (MX,MY)  */
    printf("mom%sx mom%sy curveto stroke ",sf,sf);

    printf("moveto}}%%\n");
}

char    m[4], n[4];
/* m and n are suffixes for PS identifiers initialized here for
 * later use.  m is for local lines; n is for discontinuous
 * constituent lines requested through labels
 */
setsuffix(s, id)
char *s;
int id;
{
    s[0] = 'a'; s[1] = 'a'; s[2] = 'a'; s[3] = '\0';
    s[0] += id / (26*26);
    s[1] += (id / 26) % 26;
    s[2] += id % 26;
}

char *whichbar[] = {
	"",
	"\\big\\Vert",
	"\\big\\downarrow",
	"\\big\\Downarrow",
	"\\big\\uparrow",
	"\\big\\Uparrow",
	"\\big\\updownarrow",
	"\\diamondsuit",
	"\\triangle",
	""
};
char *whichobar[] = {
	"",
	"\\big\\Vert",
	"\\big\\uparrow",
	"\\big\\Uparrow",
	"\\big\\downarrow",
	"\\big\\Downarrow",
	"\\big\\updownarrow",
	"\\diamondsuit",
	"\\nabla",
	""
};

int greyness;

    /* The vertical bars start horizontally half way through a
     * character space and go .4pt further to the right.  For the
     * -u option, issue PS to draw a line to the previously defined
     * position under the node name above.  (For upside down trees,
     * the position over the node name below is unfortunately not yet
     * defined -- haven't figured out what to do about that -- not
     * sure I care enough.)
     */
texvbar(node, iattrib, r, is_daughter)
TREE node;
int iattrib, is_daughter;
float r;
{	TREE mom = node->mother;
	int do_a_line = FALSE,
	    do_a_bar = FALSE,
	    do_a_tbar = FALSE,
	    do_nothing = FALSE,
	    def_a_sister = FALSE,
	    def_an_osister = FALSE,
	    def_a_mother = FALSE,
	    do_a_triangle = FALSE,
	    do_a_box = FALSE,
	    do_an_obox = FALSE;

	do_a_line = (utex_opt && mom && mom->type == HBAR);
	if (mom && mom->row > node->row) do_a_line = FALSE;

	def_an_osister = (!has(node,'O') && utex_opt
				&& mom && mom->type == OBAR);
	if (def_an_osister) {
		def_a_sister = TRUE;
		if (has(node,'S') == 'f' || has(node,'S') == 'o')
			mom->left = node;
		if (has(node,'S') == 'o') def_a_mother = TRUE;
	}

	if (do_a_line && has(node,'T') && !has(node,'B')) {
		if (has(node,'S') == 'f' || has(node,'S') == 'o')
			def_a_sister = TRUE;
		if (has(node,'S') == 'o' || has(node,'S') == 'l')
			do_a_triangle = TRUE;
		if (!do_a_triangle && !def_a_sister) do_nothing = TRUE;
	}

	if (has(node,'O') || has(node,'P')) do_nothing = TRUE;
	if (iattrib && utex_opt) do_nothing = FALSE;
	if (utex_opt && iattrib == -1) def_a_mother = TRUE;
	do_a_bar = (!do_a_line && !do_nothing && !def_an_osister);
	if (has(node,'B')) do_a_bar = TRUE;
	if (do_a_bar && has(node,'T')) {
	    if (has(node,'S') == 'f' || has(node,'S') == 'o') {
		if (mom && mom->type == OBAR) do_an_obox = TRUE;
		/*else if (mom && node == mom->daughter) do_a_box = TRUE;*/
		else /*if (mom && node == mom->daughter)*/ do_a_box = TRUE;
		do_nothing = TRUE;
	    }
	    else do_nothing = TRUE;
	}
	if (has(node,'O') || has(node,'P')) do_a_bar = FALSE;
	if (do_a_bar && (!utex_opt || has(node,'B')) && whichbar[b][0]) {
		do_a_tbar = TRUE;
		do_a_bar = FALSE;
	}

	hskip += .25;

    if (do_a_box || do_an_obox) {
	TREE first = node, last;
	int len;
	while (node->sister
	      && node->mother == node->sister->mother
	      && has(node,'S') != 'l'
	      && has(node,'S') != 'o'
	      && node->sister->type == VBAR) {
		node->mother = NULL;
		node = node->sister;
	}
	last = node;
	last->mother = NULL;
	if (first != last) {
		len = last->col + last->l - first->col;
		r = len;
		r /= COLMUL;
	}
	dohskip();
	printf ("\\vrule width.04em");
	hskip -= .04;
    if (greyness) {
	    printf ("\\xleaders\\hbox to .%dem{\\hss$\\",
		greyness);
	    if (do_a_box) printf("Down");
	    else printf("Up");
	    printf ("arrow$\\hss}\\hskip%.2fem\n",
		r/2 - .50 - .04);
    }
    else {
	if (do_a_box)
	    printf ("\\vrule width%.2fem height%1.3fex depth%1.3fex%%\n",
		r/2 - .50 - .04, .09281 - d, d);
	else
	    printf ("\\vrule width%.2fem height%1.3fex depth%1.3fex%%\n",
		r/2 - .50 - .04, h, .09281 - h);
    }
	if (first != last) hskip -= (r/2 - .50);
	printf ("\\vrule width.04em");
    }



	if (do_nothing) {
		hskip += .25;
		return;
	}
	dohskip();
	if (do_a_bar) {
		printf ("\\vrule width.04em%%\n");
		hskip -= .04;
	}
	if (do_a_line) {
		setsuffix(m, mom->treeid);
		printf("\\lower%1.3fex\\hbox{\\special{%scurrentpoint",d,SKEY);
	}
	if (def_an_osister) {
		setsuffix(m, node->treeid);
		printf("\\raise%1.3fex\\hbox{\\special{%scurrentpoint",h,SKEY);
	}
	if (def_a_sister)
		printf(" /sis%sy exch def /sis%sx exch def}}%%\n",m,m);
	if (do_a_triangle) {
		if (def_a_sister) {
			hskip += r/2 - .75;
			dohskip();
			hskip += .25;
			printf("\\lower%1.3fex\\hbox{",d);
			printf("\\special{%scurrentpoint",SKEY);
		}
		printf(" sis%sx sis%sy lineto mom%sx mom%sy lineto",m,m,m,m);
		printf(" closepath");
		if (greyness)
		    printf(" .%d setgray fill 0 setgray", greyness);
		else printf(" stroke");
	}
	if (do_a_line && !do_a_tbar && !def_a_sister && !do_a_triangle
		&& !do_a_bar && !has(node,'O') && !has(node,'P'))
		printf(" mom%sx mom%sy lineto stroke",m,m);

	if (do_a_line && (do_a_triangle || !def_a_sister)) {
		printf(" moveto}}%%\n");
	}
	if (def_a_mother) {
		if (def_an_osister) {
			hskip += r/2 - .75;
			dohskip();
			hskip += .25;
			is_daughter = FALSE;
		}
		setsuffix(n, node->treeid);
		if (is_daughter) printf("\\lower%1.3fex",d);
		else printf("\\raise%1.3fex",h);
		printf("\\hbox{\\special{%s currentpoint",SKEY);
		printf(" /mom%sy exch def /mom%sx exch def}}%%\n",n,n);
	}
	if (utex_opt && iattrib > 0) {
		setsuffix(n, iattrib);
		curvegen(n, is_daughter);
	}
	if (do_a_tbar) {
		hskip -= .25 - .04;
		dohskip();
		printf("\\hbox to 0.5em{\\hss$%s$\\hss}%%\n",
			(has(node,'U') == 'i')? whichobar[b] : whichbar[b]);
		hskip -= .25 + .04;
	}

	hskip += .25;
}



    /* Horizontal bars also start half way through a space.
     * They have a vertical bar in the center and extend .4pt
     * further than half way through a character space at the
     * end to cap the vertical bar that will come below.
     * For the -u option, instead of rules, generate PS code
     * to remember the coordinates under the node name above, so
     * later can draw line from daughters back to here.
     */
texhbar(node, iattrib, r, rm, is_daughter)
TREE node;
int iattrib, is_daughter;
float r, rm;
{	TREE mom = node->mother;

    if (utex_opt && !has(node,'B')) {
/* REVISE HERE */
/* rm/2 + (r - rm)/2 = rm/2 + r/2 - rm/2 = r/2 */

	hskip += rm/2 + .25;
	dohskip ();
	if (debug_opt) printf("%% Here is mom [%d]\n", node->treeid);
	printf("\\raise%1.3fex\\hbox{\\special{%scurrentpoint",h,SKEY);
        setsuffix(m, node->treeid);
	printf(" /mom%sy exch def /mom%sx exch def}}%%\n",m,m);
	if (iattrib > 0) {
		setsuffix(n, iattrib);
		curvegen(n, is_daughter);
	}
	hskip += (r - rm)/2 - .25;
    } else {
	float w;
	hskip += .25;
	dohskip ();
	if (b == 9 && r >= 6)
		printf("\\hbox to %.2fem{\\downbracefill}%%\n",
			r/2 - .50 + .04);
	else if (!node->mother)
		printf ("\\vrule width%.2fem height%1.3fex depth%1.3fex%%\n",
			r/2 - .50 + .04, .09281 - d, d);
	else {
	    if ((w = rm/2) > .01)
		printf ("\\vrule width%.2fem height%1.3fex depth%1.3fex%%\n",
			w, .09281 - d, d);
	    printf ("\\vrule width.04em");
	    if ((w = r/2 - w - .50) > .01)
		printf ("\\vrule width%.2fem height%1.3fex depth%1.3fex%%\n",
			w, .09281 - d, d);
	}
	hskip += .25 -.04;
    }
}



texobar(node, iattrib, r, rm, is_daughter)
TREE node;
int iattrib, is_daughter;
float r, rm;
{
    /* "left" is actually a pointer up to first daughter */
    if (utex_opt && !has(node,'B') && node->left && node->left->mother == node
					&& node->left->type == VBAR) {
	TREE sis = node->left;
	hskip += rm/2 + .25;
	dohskip ();
	if (debug_opt) printf("%% Here is bottom pt [%d]\n", node->treeid);
	printf("\\lower%1.3fex\\hbox{\\special{%scurrentpoint",d,SKEY);

	if (iattrib == -1) {
		setsuffix(n, node->treeid);
		printf(" currentpoint /mom%sy exch def /mom%sx exch def",n,n);
	}

	while (sis && sis->mother == node) {
	    if (has(sis,'O') || has(sis,'P')) {
		sis = sis->sister;
		continue;
	    }
            setsuffix(m, sis->treeid);
	    if (has(node,'T')) {
		if (has(node,'S') == 'f'
			|| has(node,'S') == 'l'
			|| has(node,'S') == 'o')
		    printf(" sis%sx sis%sy lineto",m,m);
	    }
	    else printf(" currentpoint sis%sx sis%sy lineto moveto",m,m);
	    if (has(node,'T') && has(node,'S') == 'o')
		    printf(" mom%sx mom%sy lineto",m,m);
	    sis = sis->sister;
	}
	if (has(node,'T')) {
		printf(" closepath");
		if (greyness)
		    printf(" .%d setgray fill 0 setgray", greyness);
		else printf(" stroke");
	}
	else printf(" stroke");
	printf(" moveto}}%%\n");
	if (iattrib > 0) {
		setsuffix(n, iattrib);
		curvegen(n, is_daughter);
	}
	hskip += (r - rm)/2 - .25;

    }
    else {
	float w;
	hskip += .25;
	dohskip ();
	if (b == 9 && r >= 6)
		printf("\\hbox to %.2fem{\\upbracefill}%%\n",
			r/2 - .50 + .04);
	else if (node->mother && node->right) {
	    if ((w = rm/2) > .01)
		printf ("\\vrule width%.2fem height%1.3fex depth%1.3fex%%\n",
			w, h, .09281 - h);
	    printf ("\\vrule width.04em");
	    if ((w = r/2 - w - .50) > .01)
		printf ("\\vrule width%.2fem height%1.3fex depth%1.3fex%%\n",
			w, h, .09281 - h);
	}
	else printf ("\\vrule width%.2fem height%1.3fex depth%1.3fex%%\n",
			r/2 - .50 + .04, h, .09281 - h);
	hskip += .25 - .04;
    }
}

texnodename(node, r)
TREE node;
float r;
{
	if (has(node,'P')) hskip += r/2;
	else {
		dohskip ();
		if (has(node,'R'))
			printf ("\\hbox to %.2fem{\\hss{%s}}%%\n",
				r/2, node->n);
		else printf ("\\hbox to %.2fem{\\hss{%s}\\hss}%%\n",
				r/2, node->n);
	}
}

/* emit TeX code for a bar or a box containing a node name */
boxitup (node)
TREE node;
{
	float   r = node->l, rm;
	int     iattrib = 0;
	int     is_daughter;
	int     i;
	TREE    mom = node->mother;

	if (b = has(node,'B')) {
		if (b == '+') b = 9;
		else if (isdigit(b)) b -= '0';
		else b = 0;
		greyness = b;
	}
	else {
		for (b = black_opt; b > 10; b /= 10) ;
		for (greyness = black_opt; greyness >= 100; greyness /= 10);
	}
	if (greyness > 9) greyness = 100 - greyness;
	else if (greyness) greyness = 10 - greyness;

	if (mom && node != mom->daughter && node->sister) mom = NULL;

	/* set height and depth for raising and lowering and for strut
	 * at end of line
	 */
	set_hd(node);

	iattrib = setiattrib(node, &is_daughter);

	/* halve width to compensate for doubling col values */
	r /= COLMUL;
	i = node->mid;
	if (COLMUL > 2) i /= (COLMUL/2);
	rm = i;
	if (COLMUL > 1) rm /= 2;

  /* now generate TeX code for VBARs, HBARs, and NODENAMEs */
	switch(node->type) {
		case VBAR:	texvbar(node, iattrib, r, is_daughter);
				break;
		case HBAR:	texhbar(node, iattrib, r, rm, is_daughter);
				break;
		case OBAR:	texobar(node, iattrib, r, rm, is_daughter);
				break;
		case NODENAME:	texnodename(node, r);
				break;
	}
}


/* Like preceding routine tex(), except collect spaces and
 * emit globs of TeX \hskip, \hbox, and \vrule commands (for
 * respectively space, node names, and tree lines).
 */
tex(tree)
TREE tree;
{
    int     row = tree->row,
	    col = 0,
	    i;

    hskip = (float) indent / 2;

    /* mark all labels as undefined */
    for (i = 0; i < 11; i++) {
	m_ulabel[i] = 0;
	d_ulabel[i] = 0;
    }
     /* make sure set_hd looks at first row */
    curr_row = -1;

    /* Each line of the tree will be a paragraph, so prevent white space
     * breaking up segments of vertical rules; put a strut at the
     * end of each line to make it high enough.  I'm not using regular
     * \strut commands, because my own TeX code is not careful about
     * keeping \strut defined appropriately for the font in use.
     */
    printf ("\n\n{\\parskip=0pt\\offinterlineskip%%\n");

    while (1) {
	if (!tree) {
	    printf ("\\vrule width0em height%1.3fex depth%1.3fex",h,d);
	    printf ("\\par}\n");
	    bufp = buf; /* can reuse string buffer for next tree */
	    return;
	}
	if (tree->row > row) {
	    /* Put a strut at the end of each line.  The height and
	     * depth were determined by set_hd, called by boxitup.
	     */
	    printf ("\\vrule width0em height%1.3fex depth%1.3fex",h,d);
	    /* prevent page breaks in midst of tree */
	    printf ("\\par\\penalty10000\n");
	    row++;
	    col = 0;
	    hskip = (float) indent / 2;
	}
	else if ((tree->row == row)
	      && (tree->col == col)) {
	    boxitup(tree);
	    col += tree->l;
	    tree = tree->right;
	}
	else {
	    /* to advance one column, hskip 1/4 em, which is only 1/2
	     * en space, since we doubled all the col values
	     */
	    hskip +=.50/COLMUL;
	    col++;
	}
	if (col + indent > maxcol) maxcol = col + indent;
    }
}
