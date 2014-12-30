#! /usr/bin/env python

# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import math, cmath
from cmath import phase, rect

# All dimensions in millimetres.
a4_dim = complex(297, 210)

diam = 14.63
mousebites_per_tab = 3
tabs_per_circle = 4
mousebite_hole_separation = 0.8
mousebite_hole_size = 0.3
mousebite_hole_pullback = 0.0
corner_length = 0.01
mode = "deg0" # "deg45"

# diam = 100.0
# mousebites_per_tab = 5
# tabs_per_circle = 4
# mousebite_hole_separation = 1.0
# mousebite_hole_size = 0.5
# mousebite_hole_pullback = 0.25
# corner_length = 0.1
# mode = "deg0" # "deg45"

tab_width = mousebites_per_tab * mousebite_hole_separation
route_width = 2.0
waste_width = 2.5
outline_width = 0.05

radius = diam / 2
circum = diam * math.pi
angle_between_tabs = 2 * math.pi / tabs_per_circle

# page_middle = complex(a4_dim.real / 2, a4_dim.imag / 2)
# Midpoint of Andrew's files
page_middle = complex(7.6962, -12.05991)

# Lines of the file
l = []

# def as_polar_string(p):
#     return u"(r=%f,th=%f)" % (abs(p), math.degrees(cmath.phase(p)))

# def point_to_kicad(p, origin=page_offset):
#    """ Convert a point in mm to a string in thousandths of an inch """
#    rotated_p = cmath.rect(abs(p), cmath.phase(p) + board_rotation)
#    offset_p = rotated_p + origin
#    return "%d %d" % (int((offset_p.real / 25.4) * 10000), -int((offset_p.imag / 25.4) * 10000))

def as_coord(p):
    return "%f %f" % (p.real, p.imag)

def as_coord_pm(p):
    return as_coord(p + page_middle)
    
def perimeter_distance_to_angle(d):
    percentage_of_circle = d / circum
    angle = 2 * math.pi * percentage_of_circle
    # angle = 2 * d
    # print "percentage_of_circle=", percentage_of_circle, "angle=", angle
    return angle
    
def emit_lines(l):
    print """(kicad_pcb (version 3) (host pcbnew "(2013-june-11)-stable")

  (general
    (links 0)
    (no_connects 0)
    (area 0 0 0 0)
    (thickness 1.6)
    (drawings %d)
    (tracks 0)
    (zones 0)
    (modules 0)
    (nets 1)
  )

  (page A4)
  (layers
    (15 F.Cu signal)
    (0 B.Cu signal)
    (16 B.Adhes user)
    (17 F.Adhes user)
    (18 B.Paste user)
    (19 F.Paste user)
    (20 B.SilkS user)
    (21 F.SilkS user)
    (22 B.Mask user)
    (23 F.Mask user)
    (24 Dwgs.User user)
    (25 Cmts.User user)
    (26 Eco1.User user)
    (27 Eco2.User user)
    (28 Edge.Cuts user)
  )

  (setup
    (last_trace_width 0.254)
    (trace_clearance 0.254)
    (zone_clearance 0.508)
    (zone_45_only no)
    (trace_min 0.254)
    (segment_width 0.2)
    (edge_width 0.15)
    (via_size 0.889)
    (via_drill 0.635)
    (via_min_size 0.889)
    (via_min_drill 0.508)
    (uvia_size 0.508)
    (uvia_drill 0.127)
    (uvias_allowed no)
    (uvia_min_size 0.508)
    (uvia_min_drill 0.127)
    (pcb_text_width 0.3)
    (pcb_text_size 1.5 1.5)
    (mod_edge_width 0.15)
    (mod_text_size 1.5 1.5)
    (mod_text_width 0.15)
    (pad_size 1.524 1.524)
    (pad_drill 0.762)
    (pad_to_mask_clearance 0.2)
    (aux_axis_origin 0 0)
    (visible_elements FFFFFFBF)
    (pcbplotparams
      (layerselection 268435456)
      (usegerberextensions true)
      (excludeedgelayer true)
      (linewidth 0.100000)
      (plotframeref false)
      (viasonmask false)
      (mode 1)
      (useauxorigin false)
      (hpglpennumber 1)
      (hpglpenspeed 20)
      (hpglpendiameter 15)
      (hpglpenoverlay 2)
      (psnegative false)
      (psa4output false)
      (plotreference true)
      (plotvalue true)
      (plotothertext true)
      (plotinvisibletext false)
      (padsonsilk false)
      (subtractmaskfromsilk false)
      (outputformat 1)
      (mirror false)
      (drillshape 0)
      (scaleselection 1)
      (outputdirectory gerbers/))
  )

  (net 0 "")

  (net_class Default "This is the default net class."
    (clearance 0.254)
    (trace_width 0.254)
    (via_dia 0.889)
    (via_drill 0.635)
    (uvia_dia 0.508)
    (uvia_drill 0.127)
    (add_net "")
  )""" % len(l)
    for line in l: 
        print " ", line
    print ")"

def emit_bites(l):
    distance_to_last_mousebite_hole = (mousebites_per_tab - 1.0) / 2 * mousebite_hole_separation
    distance_to_first_mousebite = float((mousebites_per_tab + 1) % 2) / 2 * mousebite_hole_separation
    # print "# distance_to_last_mousebite_hole=", distance_to_last_mousebite_hole
    # print "# distance_to_first_mousebite=", distance_to_first_mousebite
    for tab in xrange(tabs_per_circle):
        if mode == 'deg0':
            angle_from_base = tab * math.pi / 2
        else:
            angle_from_base = (tab + 0.5) * math.pi / 2
        distance = distance_to_first_mousebite
        mousebite_baseline_vector = rect(radius - mousebite_hole_pullback, angle_from_base)
        # print "mousebite_baseline_vector=", mousebite_baseline_vector
        # print "circum=", circum
        while distance <= distance_to_last_mousebite_hole:
            # print "# distance=", distance
            angle = perimeter_distance_to_angle(distance)
            # print "# angle=", angle
            mousebite_cw = rect(abs(mousebite_baseline_vector), phase(mousebite_baseline_vector) - angle)
            # print "mousebite_cw=", mousebite_cw
            l.append('(module MOUSEBITE_HOLE (at %s) (pad "" np_thru_hole circle (at 0 0) (size 0.4 0.4) (drill 0.5) (layers *.Cu *.Mask F.SilkS)))' % as_coord(page_middle + mousebite_cw))
            mousebite_ccw = rect(abs(mousebite_baseline_vector), phase(mousebite_baseline_vector) + angle)
            if mousebite_cw != mousebite_ccw:
                # print "mousebite_ccw=", mousebite_ccw
                l.append('(module MOUSEBITE_HOLE (at %s) (pad "" np_thru_hole circle (at 0 0) (size 0.4 0.4) (drill 0.5) (layers *.Cu *.Mask F.SilkS)))' % as_coord(page_middle + mousebite_ccw))
            distance += mousebite_hole_separation

def emit_corners(l):
    # (gr_line (start 136.12 115.11) (end 137.58 94.1) (angle 90) (layer Eco1.User) (width 0.2))
    length_to_edge = radius + route_width + (waste_width / 2)
    length_to_corner = length_to_edge * math.sqrt(2)
    angle_135_deg = 0.75 * math.pi
    
    for c in xrange(4):
        angle_from_base = (c + 0.5) * math.pi / 2
        corner = rect(length_to_corner, angle_from_base)
        # l.append('(gr_line (start %s) (end %s) (angle 90) (layer Eco1.User) (width %s))' % (as_coord_pm(complex(0, 0)), as_coord_pm(corner), outline_width))
        corner_away_ccw = rect(corner_length, phase(corner) - angle_135_deg)
        corner_away_cw = rect(corner_length, phase(corner) + angle_135_deg)
        l.append('(gr_line (start %s) (end %s) (angle 90) (layer Edge.Cuts) (width %s))' % (as_coord_pm(corner), as_coord_pm(corner + corner_away_ccw), outline_width))
        l.append('(gr_line (start %s) (end %s) (angle 90) (layer Edge.Cuts) (width %s))' % (as_coord_pm(corner), as_coord_pm(corner + corner_away_cw), outline_width))

def emit_arcs(l):
    print "# tab_width=", tab_width
    print "# route_width=", route_width
    # aip = arc intersection point
    perimeter_distance_to_aip = (tab_width + route_width) / 2
    print "# perimeter_distance_to_aip=", perimeter_distance_to_aip
    angle_to_aip = perimeter_distance_to_angle(perimeter_distance_to_aip)
    distance_to_corner_arc_centre = radius + route_width / 2
    print "# angle_to_aip=", angle_to_aip
    for tab in xrange(4):
        if mode == 'deg0':
            angle_from_base = tab * math.pi / 2
        else:
            angle_from_base = (tab + 0.5) * math.pi / 2
        aip_baseline_vector = rect(radius, angle_from_base) # , tab * angle_between_tabs)
        aip_ccw = rect(abs(aip_baseline_vector), phase(aip_baseline_vector) - angle_to_aip)
        aip_cw = rect(abs(aip_baseline_vector), phase(aip_baseline_vector) + angle_to_aip)
        print "# aip_ccw=", aip_ccw
        diff = aip_ccw - aip_baseline_vector
        print "# diff=", diff, "abs=", abs(diff)
        # l.append('(module MOUSEBITE_HOLE (at %s) (pad "" np_thru_hole circle (at 0 0) (size 0.1 0.1) (drill 0.05) (layers *.Cu *.Mask F.SilkS)))' % as_coord_pm(aip_ccw))
        # l.append('(module MOUSEBITE_HOLE (at %s) (pad "" np_thru_hole circle (at 0 0) (size 0.1 0.1) (drill 0.05) (layers *.Cu *.Mask F.SilkS)))' % as_coord_pm(aip_cw))
        # Now extend the aip_ccw vector to find the centre of the corner arc
        corner_arc_ccw = rect(abs(aip_ccw) + route_width / 2, phase(aip_ccw))
        corner_arc_cw = rect(abs(aip_cw) + route_width / 2, phase(aip_cw))
        # l.append('(module MOUSEBITE_HOLE (at %s) (pad "" np_thru_hole circle (at 0 0) (size 0.1 0.1) (drill 0.05) (layers *.Cu *.Mask F.SilkS)))' % as_coord(page_middle + corner_arc_ccw))
        # l.append('(module MOUSEBITE_HOLE (at %s) (pad "" np_thru_hole circle (at 0 0) (size 0.1 0.1) (drill 0.05) (layers *.Cu *.Mask F.SilkS)))' % as_coord(page_middle + corner_arc_cw))
        # l.append('(gr_circle (center %s) (end %s) (layer Edge.Cuts) (width 0.15))' % (as_coord(page_middle + corner_arc_ccw), as_coord(page_middle + aip_ccw)))
        
        # Draw corner arc
        # l.append('(module MOUSEBITE_HOLE (at %s) (pad "" np_thru_hole circle (at 0 0) (size 1 1) (drill 0.05) (layers *.Cu *.Mask F.SilkS)))' % as_coord(page_middle + corner_arc_stop_spot_ccw))
        l.append('(gr_arc (start %s) (end %s) (angle %f) (layer Edge.Cuts) (width %f))' % (as_coord_pm(corner_arc_ccw), as_coord_pm(aip_ccw), -180, outline_width))
        l.append('(gr_arc (start %s) (end %s) (angle %f) (layer Edge.Cuts) (width %f))' % (as_coord_pm(corner_arc_cw), as_coord_pm(aip_cw), 180, outline_width))
    
        angle_of_board_edge = 2 * math.pi / tabs_per_circle - (2 * angle_to_aip)
        angle_of_board_edge_deg = angle_of_board_edge * 180 / math.pi
        corner_arc_outside_ccw = rect(abs(aip_ccw) + route_width, phase(aip_ccw))
        # Draw board edge arc
        l.append('(gr_arc (start %s) (end %s) (angle %f) (layer Edge.Cuts) (width %f))' % (as_coord_pm(complex(0,0)), as_coord_pm(aip_ccw), -angle_of_board_edge_deg, outline_width))
        l.append('(gr_arc (start %s) (end %s) (angle %f) (layer Edge.Cuts) (width %f))' % (as_coord_pm(complex(0,0)), as_coord_pm(corner_arc_outside_ccw), -angle_of_board_edge_deg, outline_width))

def main():
    l = []
    # print "page_middle=", page_middle
    centre = complex(0, 0)
    inside_rim = complex(radius, 0)
    outside_rim = complex(radius + route_width, 0)
    # l.append('(gr_circle (center %s) (end %s) (layer Eco1.User) (width %f))' % (as_coord_pm(centre), as_coord_pm(inside_rim), outline_width))
    # l.append('(gr_circle (center %s) (end %s) (layer Eco1.User) (width %f))' % (as_coord_pm(centre), as_coord_pm(outside_rim), outline_width))
    emit_bites(l)
    # emit_arc_experiment(l)
    
    emit_corners(l)
    emit_arcs(l)

    emit_lines(l)
    
if __name__ == "__main__":
    main()
