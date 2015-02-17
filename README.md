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

# How to do coordinate geometry in Python.

Python has support for [complex numbers](https://docs.python.org/2/library/cmath.html), that is, numbers with a real and imaginary component.

We can create complex numbers by giving the real and imaginary part:

```
>>> import cmath
>>> z = 3 + 4j
>>> z.real
3.0
>>> z.imag
4.0
>>> 
```

This can be visualised on an x-y cartesian graph as a vector from (0, 0) to (3, 4).  We can find the length of that vector, and the angle it subtends:

```
>>> abs(z)
5.0
>>> cmath.phase(z) * (180 / cmath.pi)
53.13010235415598
>>>
```

`cmath.phase()` returns an angle in radians, so here's we're converting it to degrees.

We can also create a vector by giving the magnitude and the angle.:

```
>>> z = cmath.rect(2, 45 * cmath.pi / 180)
>>> z.real
1.4142135623730951
>>> z.imag
1.414213562373095
>>>
```

And we can do vector addition:

```
>>> z1 = 1 + 2j
>>> z2 = 3 + 4j
>>> z3 = z1 + z2
>>> z3.real
4.0
>>> z3.imag
6.0
>>> 
```

4 is 1 + 3 and 6 is 2 + 4.

You can use Python's complex number support to rotate a point around a centre.  Here are two ways to generate the 12 points of a circle that correspond to where the hours are on a clock face of radius 5.

The first way works by constructing each of the twelve points:

```
>>> r = 5
>>> for segment in xrange(12):
...   angle = 2 * cmath.pi / 12 * segment
...   point = cmath.rect(r, angle)
...   print point
... 
(5+0j)
(4.33012701892+2.5j)
(2.5+4.33012701892j)
(3.06161699787e-16+5j)
(-2.5+4.33012701892j)
(-4.33012701892+2.5j)
(-5+6.12323399574e-16j)
(-4.33012701892-2.5j)
(-2.5-4.33012701892j)
(-9.18485099361e-16-5j)
(2.5-4.33012701892j)
(4.33012701892-2.5j)
>>> 
```

The second way involves constructing a vector `v`, then revolving that vector around the central point.  The `cmath.rect(abs(v), cmath.phase(v) + angle)` pattern is something I use a lot in my code.

```
>>> v = r + 0j
>>> for segment in xrange(12):
...   angle = 2 * cmath.pi / 12 * segment
...   point = cmath.rect(abs(v), cmath.phase(v) + angle)
...   print point
... 
(5+0j)
(4.33012701892+2.5j)
(2.5+4.33012701892j)
(3.06161699787e-16+5j)
(-2.5+4.33012701892j)
(-4.33012701892+2.5j)
(-5+6.12323399574e-16j)
(-4.33012701892-2.5j)
(-2.5-4.33012701892j)
(-9.18485099361e-16-5j)
(2.5-4.33012701892j)
(4.33012701892-2.5j)
>>> 
```

Finally, if we had vector `v` of radius 5, but we wanted to generate the points to only have a magnitude 80% of v, we can do it like this:

```
>>> v = r + 0j
>>> for segment in xrange(12):
...   angle = 2 * cmath.pi / 12 * segment
...   point = cmath.rect(abs(v) * 0.8, cmath.phase(v) + angle)
...   print point
... 
(4+0j)
(3.46410161514+2j)
(2+3.46410161514j)
(2.44929359829e-16+4j)
(-2+3.46410161514j)
(-3.46410161514+2j)
(-4+4.89858719659e-16j)
(-3.46410161514-2j)
(-2-3.46410161514j)
(-7.34788079488e-16-4j)
(2-3.46410161514j)
(3.46410161514-2j)
>>> 
```

The 0.8 scales the radius of the resultant vector.

These techniques are used a lot in my code.  

Note the (-4+4.89858719659e-16j) for the coordinate at the 180 degree point.  What we're seeing here is rounding errors in Python's floating point number routines.  Practically, as far as circuit boards go, we don't need to worry about it.

