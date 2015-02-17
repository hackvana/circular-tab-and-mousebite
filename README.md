# circular-tab-and-mousebite
Creating KiCad pcb outline and NPTH holes to assist with panelisation of circular designs.

A customer sent me a circular PCB, and asked me to panelise it.

Panelising of boards with straight sides is relatively easy.  I use gerbmerge.

Panelisation of round boards is quite a bit harder.  Basically, it needs to be done with tabs-and-mousebites.

Here's a good reference to tabs-and-mousebites:

  http://blogs.mentor.com/tom-hausherr/blog/2011/06/23/pcb-design-perfection-starts-in-the-cad-library-part-19/
  
Here's the customer's design:

![Image](../master/images/Selection_714.png?raw=true)

(Note that any position errors in these pics, such as arcs not lining up, and small variances in the NPTH hole position, are due gerbv rendering bugs)

And the code in this repo generates a KiCad file, which KiCad can turn into gerbers which look like this:

![Image](../master/images/Selection_718.png?raw=true)

Then I used gerbv to merge the customer's gerber/excellon files, with the KiCad output.  It looks like this:

![Image](../master/images/Selection_715.png?raw=true)

Note the small ⌜⌝⌞⌟ marks in the corners.  Gerbmerge panelises boards according to the maximum size of the source board's outline layer.  The corner marks are there to force the board to be a certain size.

After panelisation, the board looks like this:

![Image](../master/images/Selection_716.png?raw=true)

I then send these gerbers back to the customer for review.
