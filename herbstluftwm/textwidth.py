#!/usr/bin/env python3
import sys
import cairo
import gi
gi.require_version('Pango', '1.0')
gi.require_version('PangoCairo', '1.0')
from gi.repository import Pango
from gi.repository import PangoCairo as PC

size = 15
text = sys.argv[1] if len(sys.argv) > 1 else ""

surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 32760, 100)
cr = cairo.Context(surface)
layout = Pango.Layout.new(PC.create_context(cr))
fontdesc = Pango.FontDescription("UbuntuMono Nerd Font Mono %d" % size)
layout.set_font_description(fontdesc)
layout.set_text(text, -1)
w, h = layout.get_size()
print(int(w / Pango.SCALE))
