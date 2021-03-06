# -*- coding: utf8 -*-

# Copyright (C) 2014  Ben Ockmore

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""This module provides an easy way to import all the models defined within
the wpschema package.
"""

from wpschema.waveplot import Edit, Editor, Question, WavePlot, WavePlotContext
from wpschema.musicbrainz import (
    Area, AreaType, Artist, ArtistCredit, ArtistType, Gender, Language, Medium,
    Recording, RecordingRedirect, Release, ReleaseRedirect, ReleaseGroup,
    ReleaseGroupPrimaryType, ReleasePackaging, ReleaseStatus, Script, Track,
    TrackRedirect
)
