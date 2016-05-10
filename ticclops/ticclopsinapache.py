#!/usr/bin/env python
#-*- coding:utf-8 -*-

###############################################################
# CLAM: Computational Linguistics Application Mediator
# -- Settings --
#       by Maarten van Gompel (proycon)
#       http://ilk.uvt.nl/~mvgompel
#       Induction for Linguistic Knowledge Research Group
#       Universiteit van Tilburg
#
#       Licensed under GPLv3
#
###############################################################

from clam.common.parameters import *
from clam.common.formats import *
from clam.common.converters import *
from clam.common.viewers import *
from clam.common.data import *
from clam.common.digestauth import pwhash
from os import uname
import sys
REQUIRE_VERSION = 0.9

import os                                                                                                                                                                                                   
try:
    language = os.environ['language']
except:
    language = None
#The System ID, a short alphanumeric identifier for internal use only
SYSTEM_ID = "ticclops"

#System name, the way the system is presented to the world
SYSTEM_NAME = "Tesseract and TICCLops for @PhilosTEI"

#An informative description for this system:
SYSTEM_DESCRIPTION = "Tesseract is an open source Optical Character Recognition engine. TICCLops is the online processing system representing TICCL (Text-Induced Corpus Clean-up) developed within the CLARIN-NL framework."

CUSTOMHTML_PROJECTSTART = "<H3><a name=\"documentation2\"></a>TICCLops</H3></h1><p>The interface below allows you to define the actions you want TICCLops to perform on your input data. The possible actions to be performed depend on the kind of data you submit to the system.</p><p>If you submit scanned images of e.g. a book, the system allows you to transform these into editable, electronic text by means of Optical Character Recognition. This is currently performed by Tesseract, an open-source OCR-engine. Specify in the drop-down menu 'Input type?' below that you will upload page images.</p><p>You may also submit electronic text files. If these are in FoLiA xml format, you may specify that as input and the OCR step will be bypassed and your text submitted to TICCL for fully-automatic spelling and OCR-error correction.</p><p>It may well be the case that you cannot upload your corpus, for e.g. copyright and/or privacy issues. In that case, you can upload a frequency file of your corpus and TICCLops will offer a list of ranked correction candidates for words it deems probably incorrect. You can specify how many correction candidates you want to see returned by means of the 'N-best Ranking' drop-down menu.</p>"

#########################################################################################################
#   ADMINISTRATOR: ADAPT THE DATA IN THIS SECTION TO YOUR SPECIFIC SITUATION!!!!!!!
#########################################################################################################
hostname = uname()[1]
if hostname == 'ticclops.uvt.nl' or hostname == 'black.uvt.nl':
    HOST = 'ticclops.uvt.nl'
    BASEDIR = '/exp2/mre/ticclops/'
    if language:
        URLPREFIX = language
        ROOT = '/opensonar/ticclops/' + language
    else:
        URLPREFIX = 'ticclops'
        ROOT = '/opensonar/ticclops/'
else:
    #FOR ANY OTHER HOST!
    HOST = 'localhost'
    PORT = 8080
    BASEDIR = '/path/to/ticclops'
    raise Exception("Write a configuration for your host!")
#########################################################################################################
#########################################################################################################

#The root directory for CLAM, all project files, (input & output) and
#pre-installed corpora will be stored here. Set to an absolute path:
TICCLDIR = BASEDIR

#Users and passwords
USERS = None #no user authentication
#USERS = { 'username': pwhash('username', SYSTEM_ID, 'secret') } #Using pwhash and plaintext password in code is not secure!!
#Do you want all projects to be public to all users? Otherwise projects are
#private and only open to their owners and users explictly granted access.
PROJECTS_PUBLIC = False

#Amount of free memory required prior to starting a new process (in MB!), Free Memory + Cached (without swap!)
REQUIREMEMORY = 10

#Maximum load average at which processes are still started (first number reported by 'uptime')
#MAXLOADAVG = 1.0
#language = os.environ['language']

# ======== WEB-APPLICATION STYLING =============

#Choose a style (has to be defined as a CSS file in style/ )
STYLE = 'ticclops'

# ======== ENABLED FORMATS ===========

#Here you can specify an extra formats module
CUSTOM_FORMATS_MODULE = None

INTERFACEOPTIONS = "disableliveinput"

if language == 'nld':
    CUSTOMHTML_INDEX = "<H3><a name=\"documentation\"></a>Dutch Site</H3><p>This site currently offers a contemporary Dutch lexicon</p><H3><a name=\"documentation\"></a>@PhilosTEI homepage</H3><a href=\"http://www.axiom.humanities.uva.nl/PhilosTEI.html\" title=\"@PhilosTEI homepage\" id=\"logo\"><img src=\"http://ticclops.uvt.nl/PhilosTEI.jpg\" width=\"30%\" class=\"centeredImage\" background-color= transparent/></a><H3><a name=\"documentation\"></a>TICCLops documentation</H3></h1><p>Users are invited to first take a look at the TICClops User and Demonstrator Documentation, which can be downloaded from <a href=\"http://ticclops.uvt.nl/ticclops_manual.v101.pdf\">the TICCLops website.</a></p>"

##COPYPART--BEGIN
#We put this in a variable because we will use this same input template in TWO profiles.
    lexiconinputtemplate = InputTemplate('lexicon', PlainTextFormat,  'Lexicon',
    StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),

    InputSource(id='contempNLD', label="Contemporary Dutch Lexicon",
        path=TICCLDIR + "/data/int/nld/nld.aspell.dict",
        metadata=PlainTextFormat(None, encoding='utf-8',language='nld')
    ),
    filename='lexicon.lst',
    unique=True,
    )

    INPUTSOURCES = [
    InputSource(id='dutchimages', label="Demonstrator data: Martinet DPO_35 Tiff-images",
        path=TICCLDIR + "corpora/TIFF/NLD/",
        metadata=TiffImageFormat(None),
        inputtemplate='image'
    ),
    ]

    PROFILES = [
    Profile(
        InputTemplate('textinput', PlainTextFormat, 'Plain-Text Input',
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
            #MSWordConverter(id='msword',label='Convert from MS Word Document'),
            #PDFtoTextConverter(id='pdf',label='Convert from PDF Document'),
            acceptarchive=True,
            extension='.txt',
            multi=True,
        ),
        lexiconinputtemplate,  #variable containing the input template defined earlier
        OutputTemplate('ranked', PlainTextFormat, 'Variant Output',
           SetMetaField('encoding','utf-8'),
           filename='ranked',
           unique=True,
        ),
    ),

    Profile(
        InputTemplate('frqlistinput', PlainTextFormat, 'Frequency List Input',
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
            extension='.tsv',
            unique=True,
        ),
        lexiconinputtemplate,  #variable containing the input template defined earlier
        OutputTemplate('ranked', PlainTextFormat, 'Variant Output',
            SetMetaField('encoding','utf-8'),
            filename='ranked',
            unique=True,
        ),
    ),

    Profile(
        InputTemplate('FoLiAxmlinput', FoLiAXMLFormat, 'FoLiA XML',
            extension='.xml',
            acceptarchive=True,
            multi=True,
        ),
        lexiconinputtemplate, #variable containing the input template defined earlier
        OutputTemplate('ranked', FoLiAXMLFormat, 'Ranked List of Correction Candidates',
            filename='ranked',
            unique=True,
        ),
    ),

    Profile(
        InputTemplate('image', TiffImageFormat, 'Image',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    Profile(
        InputTemplate('PDF', PDFFormat, 'PDF',
           extension='.pdf',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            removeextension='.pdf',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    Profile(
        InputTemplate('DJVU', DjVuFormat, 'DJVU',
           extension='.djvu',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            removeextension='.djvu',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    ]

##COPYPART--END
elif language == 'deu': 
    CUSTOMHTML_INDEX = "<H3><a name=\"documentation\"></a>German Language Site</H3><p>This site currently offers a contemporary German lexicons</p><H3><a name=\"documentation\"></a>@PhilosTEI homepage</H3><a href=\"http://www.axiom.humanities.uva.nl/PhilosTEI.html\" title=\"@PhilosTEI homepage\" id=\"logo\"><img src=\"http://ticclops.uvt.nl/PhilosTEI.jpg\" width=\"30%\" class=\"centeredImage\" background-color= transparent/></a><H3><a name=\"documentation\"></a>TICCLops documentation</H3></h1><p>Users are invited to first take a look at the TICClops User and Demonstrator Documentation, which can be downloaded from <a href=\"http://ticclops.uvt.nl/ticclops_manual.v101.pdf\">the TICCLops website.</a></p>"
##COPYPART--BEGIN
#We put this in a variable because we will use this same input template in TWO profiles.
    lexiconinputtemplate = InputTemplate('lexicon', PlainTextFormat,  'Lexicon',
    StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
    InputSource(id='contempDE', label="Contemporary German Lexicon",
        path=TICCLDIR + "/data/int/deu/deu.aspell.dict",
        metadata=PlainTextFormat(None, encoding='utf-8',language='deu')
    ),
    filename='lexicon.lst',
    unique=True,
)

    INPUTSOURCES = [
    InputSource(id='germandata', label="Demonstrator data: Bolzano Gold Standard post-OCR FoLiA xml",
        path=TICCLDIR + "corpora/FOLIA/DEU-FRAK/",
        metadata=FoLiAXMLFormat(None, encoding='utf-8'),
        inputtemplate='FoLiAxmlinput'
    ),
    InputSource(id='germanPDFbook', label="Demonstrator data: Bolzano Wissenschaftslehre PDF-images - full book",
        path=TICCLDIR + "corpora/PDF/DEU-FRAK/BolzanoWLfull",
        metadata=PDFFormat(None),
        inputtemplate='PDF'
    ),
    InputSource(id='germanPDFdemo', label="Demonstrator data: Bolzano Wissenschaftslehre PDF-image - Vorrede",
        path=TICCLDIR + "corpora/PDF/DEU-FRAK/BolzanoWLdemo",
        metadata=PDFFormat(None),
        inputtemplate='PDF'
    ),
    ]

    PROFILES = [
    Profile(
        InputTemplate('textinput', PlainTextFormat, 'Plain-Text Input',
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
            acceptarchive=True,
            extension='.txt',
            multi=True,
        ),
        lexiconinputtemplate,  #variable containing the input template defined earlier
        OutputTemplate('ranked', PlainTextFormat, 'Variant Output',
           SetMetaField('encoding','utf-8'),
           filename='ranked',
           unique=True,
        ),
    ),

    Profile(
        InputTemplate('frqlistinput', PlainTextFormat, 'Frequency List Input',
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
            extension='.tsv',
            unique=True,
        ),
        lexiconinputtemplate,  #variable containing the input template defined earlier
        OutputTemplate('ranked', PlainTextFormat, 'Variant Output',
            SetMetaField('encoding','utf-8'),
            filename='ranked',
            unique=True,
        ),
    ),

    Profile(
        InputTemplate('FoLiAxmlinput', FoLiAXMLFormat, 'FoLiA XML',
            extension='.xml',
            acceptarchive=True,
            multi=True,
        ),
        lexiconinputtemplate, #variable containing the input template defined earlier
        OutputTemplate('ranked', FoLiAXMLFormat, 'Ranked List of Correction Candidates',
            filename='ranked',
            unique=True,
        ),
    ),

    Profile(
        InputTemplate('image', TiffImageFormat, 'Image',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            extension='.folia.xml',
            multi=True,
        ),
        ),

    Profile(
        InputTemplate('PDF', PDFFormat, 'PDF',
           extension='.pdf',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            removeextension='.pdf',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    Profile(
        InputTemplate('DJVU', DjVuFormat, 'DJVU',
           extension='.djvu',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            removeextension='.djvu',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    ]
##COPYPART--END
##DEU-FRAK--begin
elif language == 'deu-frak': 
    CUSTOMHTML_INDEX = "<H3><a name=\"documentation\"></a>German (Fraktur) Language Site</H3><p>This site currently offers a recent historic German lexicon</p><H3><a name=\"documentation\"></a>@PhilosTEI homepage</H3><a href=\"http://www.axiom.humanities.uva.nl/PhilosTEI.html\" title=\"@PhilosTEI homepage\" id=\"logo\"><img src=\"http://ticclops.uvt.nl/PhilosTEI.jpg\" width=\"30%\" class=\"centeredImage\" background-color= transparent/></a><H3><a name=\"documentation\"></a>TICCLops documentation</H3></h1><p>Users are invited to first take a look at the TICClops User and Demonstrator Documentation, which can be downloaded from <a href=\"http://ticclops.uvt.nl/ticclops_manual.v101.pdf\">the TICCLops website.</a></p>"
##COPYPART--BEGIN
#We put this in a variable because we will use this same input template in TWO profiles.
    lexiconinputtemplate = InputTemplate('lexicon', PlainTextFormat,  'Lexicon',
    StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
    InputSource(id='historDEU', label="Historical German Lexicon",
        path=TICCLDIR + "/data/int/deu-frak/deu-frak.aspell.dict",
        metadata=PlainTextFormat(None, encoding='utf-8',language='deu-frak')
    ),
    filename='lexicon.lst',
    unique=True,
)

    INPUTSOURCES = [
    InputSource(id='germandata', label="Demonstrator data: Bolzano Gold Standard post-OCR FoLiA xml",
        path=TICCLDIR + "corpora/FOLIA/DEU-FRAK/",
        metadata=FoLiAXMLFormat(None, encoding='utf-8'),
        inputtemplate='FoLiAxmlinput'
    ),
    InputSource(id='germanPDFbook', label="Demonstrator data: Bolzano Wissenschaftslehre PDF-images - full book",
        path=TICCLDIR + "corpora/PDF/DEU-FRAK/BolzanoWLfull",
        metadata=PDFFormat(None),
        inputtemplate='PDF'
    ),
    InputSource(id='germanPDFdemo', label="Demonstrator data: Bolzano Wissenschaftslehre PDF-image - Vorrede",
        path=TICCLDIR + "corpora/PDF/DEU-FRAK/BolzanoWLdemo",
        metadata=PDFFormat(None),
        inputtemplate='PDF'
    ),
    ]

    PROFILES = [
    Profile(
        InputTemplate('textinput', PlainTextFormat, 'Plain-Text Input',
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
            acceptarchive=True,
            extension='.txt',
            multi=True,
        ),
        lexiconinputtemplate,  #variable containing the input template defined earlier
        OutputTemplate('ranked', PlainTextFormat, 'Variant Output',
           SetMetaField('encoding','utf-8'),
           filename='ranked',
           unique=True,
        ),
    ),

    Profile(
        InputTemplate('frqlistinput', PlainTextFormat, 'Frequency List Input',
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
            extension='.tsv',
            unique=True,
        ),
        lexiconinputtemplate,  #variable containing the input template defined earlier
        OutputTemplate('ranked', PlainTextFormat, 'Variant Output',
            SetMetaField('encoding','utf-8'),
            filename='ranked',
            unique=True,
        ),
    ),

    Profile(
        InputTemplate('FoLiAxmlinput', FoLiAXMLFormat, 'FoLiA XML',
            extension='.xml',
            acceptarchive=True,
            multi=True,
        ),
        lexiconinputtemplate, #variable containing the input template defined earlier
        OutputTemplate('ranked', FoLiAXMLFormat, 'Ranked List of Correction Candidates',
            filename='ranked',
            unique=True,
        ),
    ),

    Profile(
        InputTemplate('image', TiffImageFormat, 'Image',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            extension='.folia.xml',
            multi=True,
        ),
        ),

    Profile(
        InputTemplate('PDF', PDFFormat, 'PDF',
           extension='.pdf',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            removeextension='.pdf',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    Profile(
        InputTemplate('DJVU', DjVuFormat, 'DJVU',
           extension='.djvu',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            removeextension='.djvu',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    ]
##DEU-FRAK--begin
##COPYPART--END

##ELL--begin
##COPYPART--BEGIN
elif language == 'ell': 
    CUSTOMHTML_INDEX = "<H3><a name=\"documentation\"></a>Greek Site</H3><p>This site currently offers a contemporary Greek lexicon</p><H3><a name=\"documentation\"></a>@PhilosTEI homepage</H3><a href=\"http://www.axiom.humanities.uva.nl/PhilosTEI.html\" title=\"@PhilosTEI homepage\" id=\"logo\"><img src=\"http://ticclops.uvt.nl/PhilosTEI.jpg\" width=\"30%\" class=\"centeredImage\" background-color= transparent/></a><H3><a name=\"documentation\"></a>TICCLops documentation</H3></h1><p>Users are invited to first take a look at the TICClops User and Demonstrator Documentation, which can be downloaded from <a href=\"http://ticclops.uvt.nl/ticclops_manual.v101.pdf\">the TICCLops website.</a></p>"
##COPYPART--BEGIN
#We put this in a variable because we will use this same input template in TWO profiles.
    lexiconinputtemplate = InputTemplate('lexicon', PlainTextFormat,  'Lexicon',
    StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
    InputSource(id='contempELL', label="Contemporary Greek Lexicon",
        path=TICCLDIR + "/data/int/ell/ell.aspell.dict",
        metadata=PlainTextFormat(None, encoding='utf-8',language='ell')
    ),

    filename='lexicon.lst',
    unique=True,
    )

    PROFILES = [
    Profile(
        InputTemplate('textinput', PlainTextFormat, 'Plain-Text Input',
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
            acceptarchive=True,
            extension='.txt',
            multi=True,
        ),
        lexiconinputtemplate,  #variable containing the input template defined earlier
        OutputTemplate('ranked', PlainTextFormat, 'Variant Output',
           SetMetaField('encoding','utf-8'),
           filename='ranked',
           unique=True,
        ),
    ),

    Profile(
        InputTemplate('frqlistinput', PlainTextFormat, 'Frequency List Input',
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
            extension='.tsv',
            unique=True,
        ),
        lexiconinputtemplate,  #variable containing the input template defined earlier
        OutputTemplate('ranked', PlainTextFormat, 'Variant Output',
            SetMetaField('encoding','utf-8'),
            filename='ranked',
            unique=True,
        ),
    ),

    Profile(
        InputTemplate('FoLiAxmlinput', FoLiAXMLFormat, 'FoLiA XML',
            extension='.xml',
            acceptarchive=True,
            multi=True,
        ),
        lexiconinputtemplate, #variable containing the input template defined earlier
        OutputTemplate('ranked', FoLiAXMLFormat, 'Ranked List of Correction Candidates',
            filename='ranked',
            unique=True,
        ),
    ),

    Profile(
        InputTemplate('image', TiffImageFormat, 'Image',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    Profile(
        InputTemplate('PDF', PDFFormat, 'PDF',
           extension='.pdf',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            removeextension='.pdf',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    Profile(
        InputTemplate('DJVU', DjVuFormat, 'DJVU',
           extension='.djvu',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            removeextension='.djvu',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    ]
##COPYPART--END
##ELL-end
##GRC--begin
##COPYPART--END
elif language == 'grc': 
    CUSTOMHTML_INDEX = "<H3><a name=\"documentation\"></a>Classical Greek Site</H3><p>This site currently offers a Classical Greek lexicon</p><H3><a name=\"documentation\"></a>@PhilosTEI homepage</H3><a href=\"http://www.axiom.humanities.uva.nl/PhilosTEI.html\" title=\"@PhilosTEI homepage\" id=\"logo\"><img src=\"http://ticclops.uvt.nl/PhilosTEI.jpg\" width=\"30%\" class=\"centeredImage\" background-color= transparent/></a><H3><a name=\"documentation\"></a>TICCLops documentation</H3></h1><p>Users are invited to first take a look at the TICClops User and Demonstrator Documentation, which can be downloaded from <a href=\"http://ticclops.uvt.nl/ticclops_manual.v101.pdf\">the TICCLops website.</a></p>"
##COPYPART--BEGIN
#We put this in a variable because we will use this same input template in TWO profiles.
    lexiconinputtemplate = InputTemplate('lexicon', PlainTextFormat,  'Lexicon',
    StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
    InputSource(id='contempGRC', label="Classical Greek Lexicon",
        path=TICCLDIR + "/data/int/grc/grc.aspell.dict",
        metadata=PlainTextFormat(None, encoding='utf-8',language='ell')
    ),

    filename='lexicon.lst',
    unique=True,
    )

    PROFILES = [
    Profile(
        InputTemplate('textinput', PlainTextFormat, 'Plain-Text Input',
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
            acceptarchive=True,
            extension='.txt',
            multi=True,
        ),
        lexiconinputtemplate,  #variable containing the input template defined earlier
        OutputTemplate('ranked', PlainTextFormat, 'Variant Output',
           SetMetaField('encoding','utf-8'),
           filename='ranked',
           unique=True,
        ),
    ),

    Profile(
        InputTemplate('frqlistinput', PlainTextFormat, 'Frequency List Input',
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
            extension='.tsv',
            unique=True,
        ),
        lexiconinputtemplate,  #variable containing the input template defined earlier
        OutputTemplate('ranked', PlainTextFormat, 'Variant Output',
            SetMetaField('encoding','utf-8'),
            filename='ranked',
            unique=True,
        ),
    ),

    Profile(
        InputTemplate('FoLiAxmlinput', FoLiAXMLFormat, 'FoLiA XML',
            extension='.xml',
            acceptarchive=True,
            multi=True,
        ),
        lexiconinputtemplate, #variable containing the input template defined earlier
        OutputTemplate('ranked', FoLiAXMLFormat, 'Ranked List of Correction Candidates',
            filename='ranked',
            unique=True,
        ),
    ),

    Profile(
        InputTemplate('image', TiffImageFormat, 'Image',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    Profile(
        InputTemplate('PDF', PDFFormat, 'PDF',
           extension='.pdf',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            removeextension='.pdf',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    Profile(
        InputTemplate('DJVU',  DjVuFormat, 'DJVU',
           extension='.djvu',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            removeextension='.djvu',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    ]
##COPYPART--END
##GRC--end
elif language == 'spa': 
    CUSTOMHTML_INDEX = "<H3><a name=\"documentation\"></a>Spanish Site</H3><p>This site currently offers a contemporary Spanish lexicon</p><H3><a name=\"documentation\"></a>@PhilosTEI homepage</H3><a href=\"http://www.axiom.humanities.uva.nl/PhilosTEI.html\" title=\"@PhilosTEI homepage\" id=\"logo\"><img src=\"http://ticclops.uvt.nl/PhilosTEI.jpg\" width=\"30%\" class=\"centeredImage\" background-color= transparent/></a><H3><a name=\"documentation\"></a>TICCLops documentation</H3></h1><p>Users are invited to first take a look at the TICClops User and Demonstrator Documentation, which can be downloaded from <a href=\"http://ticclops.uvt.nl/ticclops_manual.v101.pdf\">the TICCLops website.</a></p>"
##COPYPART--BEGIN
#We put this in a variable because we will use this same input template in TWO profiles.
    lexiconinputtemplate = InputTemplate('lexicon', PlainTextFormat,  'Lexicon',
    StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
    InputSource(id='contempSPA', label="Contemporary Spanish Lexicon",
        path=TICCLDIR + "/data/int/spa/spa.aspell.dict",
        metadata=PlainTextFormat(None, encoding='utf-8',language='spa')
    ),
    filename='lexicon.lst',
    unique=True,
    )

    INPUTSOURCES = [
    InputSource(id='spanishdata', label="Demonstrator data: Spaanse brieven",
        path=TICCLDIR + "corpora/OCR/List/",
        metadata=PlainTextFormat(None, encoding='utf-8'),
        inputtemplate='frqlistinput'
    ),

    ]

    PROFILES = [
    Profile(
        InputTemplate('textinput', PlainTextFormat, 'Plain-Text Input',
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
            acceptarchive=True,
            extension='.txt',
            multi=True,
        ),
        lexiconinputtemplate,  #variable containing the input template defined earlier
        OutputTemplate('ranked', PlainTextFormat, 'Variant Output',
           SetMetaField('encoding','utf-8'),
           filename='ranked',
           unique=True,
        ),
    ),

    Profile(
        InputTemplate('frqlistinput', PlainTextFormat, 'Frequency List Input',
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
            extension='.tsv',
            unique=True,
        ),
        lexiconinputtemplate,  #variable containing the input template defined earlier
        OutputTemplate('ranked', PlainTextFormat, 'Variant Output',
            SetMetaField('encoding','utf-8'),
            filename='ranked',
            unique=True,
        ),
    ),

    Profile(
        InputTemplate('FoLiAxmlinput', FoLiAXMLFormat, 'FoLiA XML',
            extension='.xml',
            acceptarchive=True,
            multi=True,
        ),
        lexiconinputtemplate, #variable containing the input template defined earlier
        OutputTemplate('ranked', FoLiAXMLFormat, 'Ranked List of Correction Candidates',
            filename='ranked',
            unique=True,
        ),
    ),

    Profile(
        InputTemplate('image', TiffImageFormat, 'Image',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    Profile(
        InputTemplate('PDF', PDFFormat, 'PDF',
           extension='.pdf',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            removeextension='.pdf',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    Profile(
        InputTemplate('DJVU',  DjVuFormat, 'DJVU',
           extension='.djvu',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            removeextension='.djvu',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    ]
##SPA_OLD--begin
elif language == 'spa_old': 
    CUSTOMHTML_INDEX = "<H3><a name=\"documentation\"></a>Spanish (Old) Site</H3><p>This site currently only offers a contemporary Spanish lexicon</p><H3><a name=\"documentation\"></a>@PhilosTEI homepage</H3><a href=\"http://www.axiom.humanities.uva.nl/PhilosTEI.html\" title=\"@PhilosTEI homepage\" id=\"logo\"><img src=\"http://ticclops.uvt.nl/PhilosTEI.jpg\" width=\"30%\" class=\"centeredImage\" background-color= transparent/></a><H3><a name=\"documentation\"></a>TICCLops documentation</H3></h1><p>Users are invited to first take a look at the TICClops User and Demonstrator Documentation, which can be downloaded from <a href=\"http://ticclops.uvt.nl/ticclops_manual.v101.pdf\">the TICCLops website.</a></p>"
##COPYPART--BEGIN
#We put this in a variable because we will use this same input template in TWO profiles.
    lexiconinputtemplate = InputTemplate('lexicon', PlainTextFormat,  'Lexicon',
    StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
    InputSource(id='contempSPA', label="Contemporary Spanish Lexicon",
        path=TICCLDIR + "/data/int/spa/spa.aspell.dict",
        metadata=PlainTextFormat(None, encoding='utf-8',language='spa')
    ),
    filename='lexicon.lst',
    unique=True,
    )

    INPUTSOURCES = [
    InputSource(id='spanishdata', label="Demonstrator data: Spaanse brieven",
        path=TICCLDIR + "corpora/OCR/List/",
        metadata=PlainTextFormat(None, encoding='utf-8'),
        inputtemplate='frqlistinput'
    ),

    ]

    PROFILES = [
    Profile(
        InputTemplate('textinput', PlainTextFormat, 'Plain-Text Input',
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
            acceptarchive=True,
            extension='.txt',
            multi=True,
        ),
        lexiconinputtemplate,  #variable containing the input template defined earlier
        OutputTemplate('ranked', PlainTextFormat, 'Variant Output',
           SetMetaField('encoding','utf-8'),
           filename='ranked',
           unique=True,
        ),
    ),

    Profile(
        InputTemplate('frqlistinput', PlainTextFormat, 'Frequency List Input',
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
            extension='.tsv',
            unique=True,
        ),
        lexiconinputtemplate,  #variable containing the input template defined earlier
        OutputTemplate('ranked', PlainTextFormat, 'Variant Output',
            SetMetaField('encoding','utf-8'),
            filename='ranked',
            unique=True,
        ),
    ),

    Profile(
        InputTemplate('FoLiAxmlinput', FoLiAXMLFormat, 'FoLiA XML',
            extension='.xml',
            acceptarchive=True,
            multi=True,
        ),
        lexiconinputtemplate, #variable containing the input template defined earlier
        OutputTemplate('ranked', FoLiAXMLFormat, 'Ranked List of Correction Candidates',
            filename='ranked',
            unique=True,
        ),
    ),

    Profile(
        InputTemplate('image', TiffImageFormat, 'Image',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    Profile(
        InputTemplate('PDF', PDFFormat, 'PDF',
           extension='.pdf',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            removeextension='.pdf',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    Profile(
        InputTemplate('DJVU', DjVuFormat, 'DJVU',
           extension='.djvu',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            removeextension='.djvu',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    ]
##SPA_OLD--end
##ENG--begin
##COPYPART--END
elif language == 'eng': 
    CUSTOMHTML_INDEX = "<H3><a name=\"documentation\"></a>English Site</H3><p>This site currently offers a contemporary English lexicon</p><H3><a name=\"documentation\"></a>@PhilosTEI homepage</H3><a href=\"http://www.axiom.humanities.uva.nl/PhilosTEI.html\" title=\"@PhilosTEI homepage\" id=\"logo\"><img src=\"http://ticclops.uvt.nl/PhilosTEI.jpg\" width=\"30%\" class=\"centeredImage\" background-color= transparent/></a><H3><a name=\"documentation\"></a>TICCLops documentation</H3></h1><p>Users are invited to first take a look at the TICClops User and Demonstrator Documentation, which can be downloaded from <a href=\"http://ticclops.uvt.nl/ticclops_manual.v101.pdf\">the TICCLops website.</a></p>"
##COPYPART--BEGIN
#We put this in a variable because we will use this same input template in TWO profiles.
    lexiconinputtemplate = InputTemplate('lexicon', PlainTextFormat,  'Lexicon',
    StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
    InputSource(id='contempENG', label="Contemporary English Lexicon",
        path=TICCLDIR + "/data/int/eng/eng.aspell.dict",
        metadata=PlainTextFormat(None, encoding='utf-8',language='eng')
    ),
    filename='lexicon.lst',
    unique=True,
    )

    INPUTSOURCES = [
        InputSource(id='englishimagessmall', label="Demonstrator data: English PDF: Eel disease",
        path=TICCLDIR + "corpora/PDF/ENG/",
                    metadata=PDFFormat(None),
        inputtemplate='PDF'
    ),
        InputSource(id='englishimageslarge', label="Demonstrator data: English DJVU: Russell -- Western Philosophy ",
        path=TICCLDIR + "corpora/DJVU/ENG/",
        metadata=DjVuFormat(None),
        inputtemplate='DJVU'
    ),
        InputSource(id='englishtxt', label="Demonstrator data: English TXT: Russell -- Western Philosophy ",
        path=TICCLDIR + "corpora/TXT/ENG/",
        metadata=PlainTextFormat(None, encoding='utf-8'),
        inputtemplate='textinput'
    ),
    ]

    PROFILES = [
    Profile(
        InputTemplate('textinput', PlainTextFormat, 'Plain-Text Input',
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
            acceptarchive=True,
            extension='.txt',
            multi=True,
        ),
        lexiconinputtemplate,  #variable containing the input template defined earlier
        OutputTemplate('ranked', PlainTextFormat, 'Variant Output',
           SetMetaField('encoding','utf-8'),
           filename='ranked',
           unique=True,
        ),
    ),

    Profile(
        InputTemplate('frqlistinput', PlainTextFormat, 'Frequency List Input',
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
            extension='.tsv',
            unique=True,
        ),
        lexiconinputtemplate,  #variable containing the input template defined earlier
        OutputTemplate('ranked', PlainTextFormat, 'Variant Output',
            SetMetaField('encoding','utf-8'),
            filename='ranked',
            unique=True,
        ),
    ),

    Profile(
        InputTemplate('FoLiAxmlinput', FoLiAXMLFormat, 'FoLiA XML',
            extension='.xml',
            acceptarchive=True,
            multi=True,
        ),
        lexiconinputtemplate, #variable containing the input template defined earlier
        OutputTemplate('ranked', FoLiAXMLFormat, 'Ranked List of Correction Candidates',
            filename='ranked',
            unique=True,
        ),
    ),

    Profile(
        InputTemplate('image', TiffImageFormat, 'Image',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    Profile(
        InputTemplate('PDF', PDFFormat, 'PDF',
           extension='.pdf',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            removeextension='.pdf',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    Profile(
        InputTemplate('DJVU', DjVuFormat, 'DJVU',
           extension='.djvu',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            removeextension='.djvu',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    ]
##COPYPART--END
##ENG-end

##ITA--begin
##COPYPART--END
elif language == 'ita': 
    CUSTOMHTML_INDEX = "<H3><a name=\"documentation\"></a>Italian Site</H3><p>This site currently offers a contemporary Italian lexicon</p><H3><a name=\"documentation\"></a>@PhilosTEI homepage</H3><a href=\"http://www.axiom.humanities.uva.nl/PhilosTEI.html\" title=\"@PhilosTEI homepage\" id=\"logo\"><img src=\"http://ticclops.uvt.nl/PhilosTEI.jpg\" width=\"30%\" class=\"centeredImage\" background-color= transparent/></a><H3><a name=\"documentation\"></a>TICCLops documentation</H3></h1><p>Users are invited to first take a look at the TICClops User and Demonstrator Documentation, which can be downloaded from <a href=\"http://ticclops.uvt.nl/ticclops_manual.v101.pdf\">the TICCLops website.</a></p>"
##COPYPART--BEGIN
#We put this in a variable because we will use this same input template in TWO profiles.
    lexiconinputtemplate = InputTemplate('lexicon', PlainTextFormat,  'Lexicon',
    StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
    InputSource(id='contempITA', label="Contemporary Italian Lexicon",
        path=TICCLDIR + "/data/int/ita/ita.aspell.dict",
        metadata=PlainTextFormat(None, encoding='utf-8',language='ita')
    ),

    filename='lexicon.lst',
    unique=True,
    )

    PROFILES = [
    Profile(
        InputTemplate('textinput', PlainTextFormat, 'Plain-Text Input',
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
            acceptarchive=True,
            extension='.txt',
            multi=True,
        ),
        lexiconinputtemplate,  #variable containing the input template defined earlier
        OutputTemplate('ranked', PlainTextFormat, 'Variant Output',
           SetMetaField('encoding','utf-8'),
           filename='ranked',
           unique=True,
        ),
    ),

    Profile(
        InputTemplate('frqlistinput', PlainTextFormat, 'Frequency List Input',
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
            extension='.tsv',
            unique=True,
        ),
        lexiconinputtemplate,  #variable containing the input template defined earlier
        OutputTemplate('ranked', PlainTextFormat, 'Variant Output',
            SetMetaField('encoding','utf-8'),
            filename='ranked',
            unique=True,
        ),
    ),

    Profile(
        InputTemplate('FoLiAxmlinput', FoLiAXMLFormat, 'FoLiA XML',
            extension='.xml',
            acceptarchive=True,
            multi=True,
        ),
        lexiconinputtemplate, #variable containing the input template defined earlier
        OutputTemplate('ranked', FoLiAXMLFormat, 'Ranked List of Correction Candidates',
            filename='ranked',
            unique=True,
        ),
    ),

    Profile(
        InputTemplate('image', TiffImageFormat, 'Image',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    Profile(
        InputTemplate('PDF', PDFFormat, 'PDF',
           extension='.pdf',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            removeextension='.pdf',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    Profile(
        InputTemplate('DJVU', DjVuFormat, 'DJVU',
           extension='.djvu',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            removeextension='.djvu',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    ]

##COPYPART--END
##ITA--end
##COPYPART--BEGIN
##ITA_OLD--begin
elif language == 'ita_old': 
    CUSTOMHTML_INDEX = "<H3><a name=\"documentation\"></a>Italian (Old) Site</H3><p>This site currently offers only a contemporary Italian lexicon</p><H3><a name=\"documentation\"></a>@PhilosTEI homepage</H3><a href=\"http://www.axiom.humanities.uva.nl/PhilosTEI.html\" title=\"@PhilosTEI homepage\" id=\"logo\"><img src=\"http://ticclops.uvt.nl/PhilosTEI.jpg\" width=\"30%\" class=\"centeredImage\" background-color= transparent/></a><H3><a name=\"documentation\"></a>TICCLops documentation</H3></h1><p>Users are invited to first take a look at the TICClops User and Demonstrator Documentation, which can be downloaded from <a href=\"http://ticclops.uvt.nl/ticclops_manual.v101.pdf\">the TICCLops website.</a></p>"
##COPYPART--BEGIN
#We put this in a variable because we will use this same input template in TWO profiles.
    lexiconinputtemplate = InputTemplate('lexicon', PlainTextFormat,  'Lexicon',
    StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
    InputSource(id='contempITA', label="Contemporary Italian Lexicon",
        path=TICCLDIR + "/data/int/ita/ita.aspell.dict",
        metadata=PlainTextFormat(None, encoding='utf-8',language='ita')
    ),

    filename='lexicon.lst',
    unique=True,
    )

    PROFILES = [
    Profile(
        InputTemplate('textinput', PlainTextFormat, 'Plain-Text Input',
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
            acceptarchive=True,
            extension='.txt',
            multi=True,
        ),
        lexiconinputtemplate,  #variable containing the input template defined earlier
        OutputTemplate('ranked', PlainTextFormat, 'Variant Output',
           SetMetaField('encoding','utf-8'),
           filename='ranked',
           unique=True,
        ),
    ),

    Profile(
        InputTemplate('frqlistinput', PlainTextFormat, 'Frequency List Input',
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
            extension='.tsv',
            unique=True,
        ),
        lexiconinputtemplate,  #variable containing the input template defined earlier
        OutputTemplate('ranked', PlainTextFormat, 'Variant Output',
            SetMetaField('encoding','utf-8'),
            filename='ranked',
            unique=True,
        ),
    ),

    Profile(
        InputTemplate('FoLiAxmlinput', FoLiAXMLFormat, 'FoLiA XML',
            extension='.xml',
            acceptarchive=True,
            multi=True,
        ),
        lexiconinputtemplate, #variable containing the input template defined earlier
        OutputTemplate('ranked', FoLiAXMLFormat, 'Ranked List of Correction Candidates',
            filename='ranked',
            unique=True,
        ),
    ),

    Profile(
        InputTemplate('image', TiffImageFormat, 'Image',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    Profile(
        InputTemplate('PDF', PDFFormat, 'PDF',
           extension='.pdf',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            removeextension='.pdf',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    Profile(
        InputTemplate('DJVU', DjVuFormat, 'DJVU',
           extension='.djvu',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            removeextension='.djvu',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    ]

##COPYPART--END
##ITA_OLD--end
##COPYPART--END
##LAT-begin
##COPYPART--END
elif language == 'lat': 
    CUSTOMHTML_INDEX = "<H3><a name=\"documentation\"></a>Latin Site</H3><p>This site currently offers only a historical Latin lexicon</p><H3><a name=\"documentation\"></a>@PhilosTEI homepage</H3><a href=\"http://www.axiom.humanities.uva.nl/PhilosTEI.html\" title=\"@PhilosTEI homepage\" id=\"logo\"><img src=\"http://ticclops.uvt.nl/PhilosTEI.jpg\" width=\"30%\" class=\"centeredImage\" background-color= transparent/></a><H3><a name=\"documentation\"></a>TICCLops documentation</H3></h1><p>Users are invited to first take a look at the TICClops User and Demonstrator Documentation, which can be downloaded from <a href=\"http://ticclops.uvt.nl/ticclops_manual.v101.pdf\">the TICCLops website.</a></p>"
##COPYPART--BEGIN
#We put this in a variable because we will use this same input template in TWO profiles.
    lexiconinputtemplate = InputTemplate('lexicon', PlainTextFormat,  'Lexicon',
    StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
    InputSource(id='historLAT', label="Historical Latin Lexicon",
        path=TICCLDIR + "/data/int/lat/lat.aspell.dict",
        metadata=PlainTextFormat(None, encoding='utf-8',language='lat')
    ),

    filename='lexicon.lst',
    unique=True,
    )

    PROFILES = [
    Profile(
        InputTemplate('textinput', PlainTextFormat, 'Plain-Text Input',
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
            acceptarchive=True,
            extension='.txt',
            multi=True,
        ),
        lexiconinputtemplate,  #variable containing the input template defined earlier
        OutputTemplate('ranked', PlainTextFormat, 'Variant Output',
           SetMetaField('encoding','utf-8'),
           filename='ranked',
           unique=True,
        ),
    ),

    Profile(
        InputTemplate('frqlistinput', PlainTextFormat, 'Frequency List Input',
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
            extension='.tsv',
            unique=True,
        ),
        lexiconinputtemplate,  #variable containing the input template defined earlier
        OutputTemplate('ranked', PlainTextFormat, 'Variant Output',
            SetMetaField('encoding','utf-8'),
            filename='ranked',
            unique=True,
        ),
    ),

    Profile(
        InputTemplate('FoLiAxmlinput', FoLiAXMLFormat, 'FoLiA XML',
            extension='.xml',
            acceptarchive=True,
            multi=True,
        ),
        lexiconinputtemplate, #variable containing the input template defined earlier
        OutputTemplate('ranked', FoLiAXMLFormat, 'Ranked List of Correction Candidates',
            filename='ranked',
            unique=True,
        ),
    ),

    Profile(
        InputTemplate('image', TiffImageFormat, 'Image',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    Profile(
        InputTemplate('PDF', PDFFormat, 'PDF',
           extension='.pdf',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            removeextension='.pdf',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    Profile(
        InputTemplate('DJVU', DjVuFormat, 'DJVU',
           extension='.djvu',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            removeextension='.djvu',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    ]

##COPYPART--END
##LAT-end
##POL--begin
##COPYPART--END
elif language == 'pol': 
    CUSTOMHTML_INDEX = "<H3><a name=\"documentation\"></a>Polish Site</H3><p>This site currently offers a contemporary Polish lexicon</p><H3><a name=\"documentation\"></a>@PhilosTEI homepage</H3><a href=\"http://www.axiom.humanities.uva.nl/PhilosTEI.html\" title=\"@PhilosTEI homepage\" id=\"logo\"><img src=\"http://ticclops.uvt.nl/PhilosTEI.jpg\" width=\"30%\" class=\"centeredImage\" background-color= transparent/></a><H3><a name=\"documentation\"></a>TICCLops documentation</H3></h1><p>Users are invited to first take a look at the TICClops User and Demonstrator Documentation, which can be downloaded from <a href=\"http://ticclops.uvt.nl/ticclops_manual.v101.pdf\">the TICCLops website.</a></p>"
##COPYPART--BEGIN
#We put this in a variable because we will use this same input template in TWO profiles.
    lexiconinputtemplate = InputTemplate('lexicon', PlainTextFormat,  'Lexicon',
    StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
    InputSource(id='contempPOL', label="Contemporary Polish Lexicon",
        path=TICCLDIR + "/data/int/pol/pol.aspell.dict",
        metadata=PlainTextFormat(None, encoding='utf-8',language='pol')
    ),

    filename='lexicon.lst',
    unique=True,
    )

    PROFILES = [
    Profile(
        InputTemplate('textinput', PlainTextFormat, 'Plain-Text Input',
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
            acceptarchive=True,
            extension='.txt',
            multi=True,
        ),
        lexiconinputtemplate,  #variable containing the input template defined earlier
        OutputTemplate('ranked', PlainTextFormat, 'Variant Output',
           SetMetaField('encoding','utf-8'),
           filename='ranked',
           unique=True,
        ),
    ),

    Profile(
        InputTemplate('frqlistinput', PlainTextFormat, 'Frequency List Input',
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
            extension='.tsv',
            unique=True,
        ),
        lexiconinputtemplate,  #variable containing the input template defined earlier
        OutputTemplate('ranked', PlainTextFormat, 'Variant Output',
            SetMetaField('encoding','utf-8'),
            filename='ranked',
            unique=True,
        ),
    ),

    Profile(
        InputTemplate('FoLiAxmlinput', FoLiAXMLFormat, 'FoLiA XML',
            extension='.xml',
            acceptarchive=True,
            multi=True,
        ),
        lexiconinputtemplate, #variable containing the input template defined earlier
        OutputTemplate('ranked', FoLiAXMLFormat, 'Ranked List of Correction Candidates',
            filename='ranked',
            unique=True,
        ),
    ),

    Profile(
        InputTemplate('image', TiffImageFormat, 'Image',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    Profile(
        InputTemplate('PDF', PDFFormat, 'PDF',
           extension='.pdf',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            removeextension='.pdf',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    Profile(
        InputTemplate('DJVU', DjVuFormat, 'DJVU',
           extension='.djvu',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            removeextension='.djvu',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    ]
##COPYPART--END
##POL--end
##POR--begin
##COPYPART--END
elif language == 'por': 
    CUSTOMHTML_INDEX = "<H3><a name=\"documentation\"></a>Portuguese Site</H3><p>This site currently offers a contemporary Portuguese lexicon</p><H3><a name=\"documentation\"></a>@PhilosTEI homepage</H3><a href=\"http://www.axiom.humanities.uva.nl/PhilosTEI.html\" title=\"@PhilosTEI homepage\" id=\"logo\"><img src=\"http://ticclops.uvt.nl/PhilosTEI.jpg\" width=\"30%\" class=\"centeredImage\" background-color= transparent/></a><H3><a name=\"documentation\"></a>TICCLops documentation</H3></h1><p>Users are invited to first take a look at the TICClops User and Demonstrator Documentation, which can be downloaded from <a href=\"http://ticclops.uvt.nl/ticclops_manual.v101.pdf\">the TICCLops website.</a></p>"
##COPYPART--BEGIN
#We put this in a variable because we will use this same input template in TWO profiles.
    lexiconinputtemplate = InputTemplate('lexicon', PlainTextFormat,  'Lexicon',
    StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
    InputSource(id='contempPOR', label="Contemporary Portuguese Lexicon",
        path=TICCLDIR + "/data/int/por/por.aspell.dict",
        metadata=PlainTextFormat(None, encoding='utf-8',language='por')
    ),

    filename='lexicon.lst',
    unique=True,
    )

    PROFILES = [
    Profile(
        InputTemplate('textinput', PlainTextFormat, 'Plain-Text Input',
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
            acceptarchive=True,
            extension='.txt',
            multi=True,
        ),
        lexiconinputtemplate,  #variable containing the input template defined earlier
        OutputTemplate('ranked', PlainTextFormat, 'Variant Output',
           SetMetaField('encoding','utf-8'),
           filename='ranked',
           unique=True,
        ),
    ),

    Profile(
        InputTemplate('frqlistinput', PlainTextFormat, 'Frequency List Input',
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
            extension='.tsv',
            unique=True,
        ),
        lexiconinputtemplate,  #variable containing the input template defined earlier
        OutputTemplate('ranked', PlainTextFormat, 'Variant Output',
            SetMetaField('encoding','utf-8'),
            filename='ranked',
            unique=True,
        ),
    ),

    Profile(
        InputTemplate('FoLiAxmlinput', FoLiAXMLFormat, 'FoLiA XML',
            extension='.xml',
            acceptarchive=True,
            multi=True,
        ),
        lexiconinputtemplate, #variable containing the input template defined earlier
        OutputTemplate('ranked', FoLiAXMLFormat, 'Ranked List of Correction Candidates',
            filename='ranked',
            unique=True,
        ),
    ),

    Profile(
        InputTemplate('image', TiffImageFormat, 'Image',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    Profile(
        InputTemplate('PDF', PDFFormat, 'PDF',
           extension='.pdf',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            removeextension='.pdf',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    Profile(
        InputTemplate('DJVU', DjVuFormat, 'DJVU',
           extension='.djvu',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            removeextension='.djvu',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    ]

##COPYPART--END
##POR--end
##RUS--begin
##COPYPART--END
elif language == 'rus': 
    CUSTOMHTML_INDEX = "<H3><a name=\"documentation\"></a>Russian Site</H3><p>This site currently offers a contemporary Russian lexicon</p><H3><a name=\"documentation\"></a>@PhilosTEI homepage</H3><a href=\"http://www.axiom.humanities.uva.nl/PhilosTEI.html\" title=\"@PhilosTEI homepage\" id=\"logo\"><img src=\"http://ticclops.uvt.nl/PhilosTEI.jpg\" width=\"30%\" class=\"centeredImage\" background-color= transparent/></a><H3><a name=\"documentation\"></a>TICCLops documentation</H3></h1><p>Users are invited to first take a look at the TICClops User and Demonstrator Documentation, which can be downloaded from <a href=\"http://ticclops.uvt.nl/ticclops_manual.v101.pdf\">the TICCLops website.</a></p>"
##COPYPART--BEGIN
#We put this in a variable because we will use this same input template in TWO profiles.
    lexiconinputtemplate = InputTemplate('lexicon', PlainTextFormat,  'Lexicon',
    StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
    InputSource(id='contempRUS', label="Contemporary Russian Lexicon",
        path=TICCLDIR + "/data/int/rus/rus.aspell.dict",
        metadata=PlainTextFormat(None, encoding='utf-8',language='rus')
    ),

    filename='lexicon.lst',
    unique=True,
    )

    PROFILES = [
    Profile(
        InputTemplate('textinput', PlainTextFormat, 'Plain-Text Input',
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
            acceptarchive=True,
            extension='.txt',
            multi=True,
        ),
        lexiconinputtemplate,  #variable containing the input template defined earlier
        OutputTemplate('ranked', PlainTextFormat, 'Variant Output',
           SetMetaField('encoding','utf-8'),
           filename='ranked',
           unique=True,
        ),
    ),

    Profile(
        InputTemplate('frqlistinput', PlainTextFormat, 'Frequency List Input',
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
            extension='.tsv',
            unique=True,
        ),
        lexiconinputtemplate,  #variable containing the input template defined earlier
        OutputTemplate('ranked', PlainTextFormat, 'Variant Output',
            SetMetaField('encoding','utf-8'),
            filename='ranked',
            unique=True,
        ),
    ),

    Profile(
        InputTemplate('FoLiAxmlinput', FoLiAXMLFormat, 'FoLiA XML',
            extension='.xml',
            acceptarchive=True,
            multi=True,
        ),
        lexiconinputtemplate, #variable containing the input template defined earlier
        OutputTemplate('ranked', FoLiAXMLFormat, 'Ranked List of Correction Candidates',
            filename='ranked',
            unique=True,
        ),
    ),

    Profile(
        InputTemplate('image', TiffImageFormat, 'Image',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    Profile(
        InputTemplate('PDF', PDFFormat, 'PDF',
           extension='.pdf',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            removeextension='.pdf',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    Profile(
        InputTemplate('DJVU', DjVuFormat, 'DJVU',
           extension='.djvu',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            removeextension='.djvu',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    ]
##COPYPART--END
##RUS--end
##SWE--begin
##COPYPART--END
elif language == 'swe': 
    CUSTOMHTML_INDEX = "<H3><a name=\"documentation\"></a>Swedish Site</H3><p>This site currently offers a contemporary Swedish lexicon</p><H3><a name=\"documentation\"></a>@PhilosTEI homepage</H3><a href=\"http://www.axiom.humanities.uva.nl/PhilosTEI.html\" title=\"@PhilosTEI homepage\" id=\"logo\"><img src=\"http://ticclops.uvt.nl/PhilosTEI.jpg\" width=\"30%\" class=\"centeredImage\" background-color= transparent/></a><H3><a name=\"documentation\"></a>TICCLops documentation</H3></h1><p>Users are invited to first take a look at the TICClops User and Demonstrator Documentation, which can be downloaded from <a href=\"http://ticclops.uvt.nl/ticclops_manual.v101.pdf\">the TICCLops website.</a></p>"
##COPYPART--BEGIN
#We put this in a variable because we will use this same input template in TWO profiles.
    lexiconinputtemplate = InputTemplate('lexicon', PlainTextFormat,  'Lexicon',
    StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
    InputSource(id='contempSWE', label="Contemporary Swedish Lexicon",
        path=TICCLDIR + "/data/int/swe/swe.aspell.dict",
        metadata=PlainTextFormat(None, encoding='utf-8',language='swe')
    ),

    filename='lexicon.lst',
    unique=True,
    )

    PROFILES = [
    Profile(
        InputTemplate('textinput', PlainTextFormat, 'Plain-Text Input',
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
            acceptarchive=True,
            extension='.txt',
            multi=True,
        ),
        lexiconinputtemplate,  #variable containing the input template defined earlier
        OutputTemplate('ranked', PlainTextFormat, 'Variant Output',
           SetMetaField('encoding','utf-8'),
           filename='ranked',
           unique=True,
        ),
    ),

    Profile(
        InputTemplate('frqlistinput', PlainTextFormat, 'Frequency List Input',
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
            extension='.tsv',
            unique=True,
        ),
        lexiconinputtemplate,  #variable containing the input template defined earlier
        OutputTemplate('ranked', PlainTextFormat, 'Variant Output',
            SetMetaField('encoding','utf-8'),
            filename='ranked',
            unique=True,
        ),
    ),

    Profile(
        InputTemplate('FoLiAxmlinput', FoLiAXMLFormat, 'FoLiA XML',
            extension='.xml',
            acceptarchive=True,
            multi=True,
        ),
        lexiconinputtemplate, #variable containing the input template defined earlier
        OutputTemplate('ranked', FoLiAXMLFormat, 'Ranked List of Correction Candidates',
            filename='ranked',
            unique=True,
        ),
    ),

    Profile(
        InputTemplate('image', TiffImageFormat, 'Image',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    Profile(
        InputTemplate('PDF', PDFFormat, 'PDF',
           extension='.pdf',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            removeextension='.pdf',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    Profile(
        InputTemplate('DJVU', DjVuFormat, 'DJVU',
           extension='.djvu',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            removeextension='.djvu',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    ]
##COPYPART--END
##SWE-end
##FIN--begin
##COPYPART--BEGIN
elif language == 'fin': 
    CUSTOMHTML_INDEX = "<H3><a name=\"documentation\"></a>Finnish Site</H3><p>This site currently offers a contemporary Finnish lexicon</p><H3><a name=\"documentation\"></a>@PhilosTEI homepage</H3><a href=\"http://www.axiom.humanities.uva.nl/PhilosTEI.html\" title=\"@PhilosTEI homepage\" id=\"logo\"><img src=\"http://ticclops.uvt.nl/PhilosTEI.jpg\" width=\"30%\" class=\"centeredImage\" background-color= transparent/></a><H3><a name=\"documentation\"></a>TICCLops documentation</H3></h1><p>Users are invited to first take a look at the TICClops User and Demonstrator Documentation, which can be downloaded from <a href=\"http://ticclops.uvt.nl/ticclops_manual.v101.pdf\">the TICCLops website.</a></p>"

#We put this in a variable because we will use this same input template in TWO profiles.
    lexiconinputtemplate = InputTemplate('lexicon', PlainTextFormat,  'Lexicon',
    StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
    InputSource(id='contempFIN', label="Contemporary Finnish Lexicon",
        path=TICCLDIR + "/data/int/fin/fin.aspell.dict",
        metadata=PlainTextFormat(None, encoding='utf-8',language='fin')
    ),
    filename='lexicon.lst',
    unique=True,
    )

    PROFILES = [
    Profile(
        InputTemplate('textinput', PlainTextFormat, 'Plain-Text Input',
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
            acceptarchive=True,
            extension='.txt',
            multi=True,
        ),
        lexiconinputtemplate,  #variable containing the input template defined earlier
        OutputTemplate('ranked', PlainTextFormat, 'Variant Output',
           SetMetaField('encoding','utf-8'),
           filename='ranked',
           unique=True,
        ),
    ),

    Profile(
        InputTemplate('frqlistinput', PlainTextFormat, 'Frequency List Input',
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
            extension='.tsv',
            unique=True,
        ),
        lexiconinputtemplate,  #variable containing the input template defined earlier
        OutputTemplate('ranked', PlainTextFormat, 'Variant Output',
            SetMetaField('encoding','utf-8'),
            filename='ranked',
            unique=True,
        ),
    ),

    Profile(
        InputTemplate('FoLiAxmlinput', FoLiAXMLFormat, 'FoLiA XML',
            extension='.xml',
            acceptarchive=True,
            multi=True,
        ),
        lexiconinputtemplate, #variable containing the input template defined earlier
        OutputTemplate('ranked', FoLiAXMLFormat, 'Ranked List of Correction Candidates',
            filename='ranked',
            unique=True,
        ),
    ),

    Profile(
        InputTemplate('image', TiffImageFormat, 'Image',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    Profile(
        InputTemplate('PDF', PDFFormat, 'PDF',
           extension='.pdf',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            removeextension='.pdf',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    Profile(
        InputTemplate('DJVU', DjVuFormat, 'DJVU',
           extension='.djvu',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            removeextension='.djvu',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    ]

##COPYPART--END
##FIN--end
##FRA-begin
##COPYPART--END
elif language == 'fra': 
    CUSTOMHTML_INDEX = "<H3><a name=\"documentation\"></a>French Site</H3><p>This site currently offers a contemporary French lexicon</p><H3><a name=\"documentation\"></a>@PhilosTEI homepage</H3><a href=\"http://www.axiom.humanities.uva.nl/PhilosTEI.html\" title=\"@PhilosTEI homepage\" id=\"logo\"><img src=\"http://ticclops.uvt.nl/PhilosTEI.jpg\" width=\"30%\" class=\"centeredImage\" background-color= transparent/></a><H3><a name=\"documentation\"></a>TICCLops documentation</H3></h1><p>Users are invited to first take a look at the TICClops User and Demonstrator Documentation, which can be downloaded from <a href=\"http://ticclops.uvt.nl/ticclops_manual.v101.pdf\">the TICCLops website.</a></p>"
##COPYPART--BEGIN
#We put this in a variable because we will use this same input template in TWO profiles.
    lexiconinputtemplate = InputTemplate('lexicon', PlainTextFormat,  'Lexicon',
    StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
    InputSource(id='contempFRA', label="Contemporary French Lexicon",
        path=TICCLDIR + "/data/int/fra/fra.aspell.dict",
        metadata=PlainTextFormat(None, encoding='utf-8',language='fra')
    ),

    filename='lexicon.lst',
    unique=True,
    )

    INPUTSOURCES = [
        InputSource(id='frenchimagessmall', label="Demonstrator data: French PDF-images Delpher dpo-7270",
        path=TICCLDIR + "corpora/PDF/FRA/",
        metadata=PDFFormat(None),
        inputtemplate='PDF'
    ),
    ]

    PROFILES = [
    Profile(
        InputTemplate('textinput', PlainTextFormat, 'Plain-Text Input',
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
            acceptarchive=True,
            extension='.txt',
            multi=True,
        ),
        lexiconinputtemplate,  #variable containing the input template defined earlier
        OutputTemplate('ranked', PlainTextFormat, 'Variant Output',
           SetMetaField('encoding','utf-8'),
           filename='ranked',
           unique=True,
        ),
    ),

    Profile(
        InputTemplate('frqlistinput', PlainTextFormat, 'Frequency List Input',
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
            extension='.tsv',
            unique=True,
        ),
        lexiconinputtemplate,  #variable containing the input template defined earlier
        OutputTemplate('ranked', PlainTextFormat, 'Variant Output',
            SetMetaField('encoding','utf-8'),
            filename='ranked',
            unique=True,
        ),
    ),

    Profile(
        InputTemplate('FoLiAxmlinput', FoLiAXMLFormat, 'FoLiA XML',
            extension='.xml',
            acceptarchive=True,
            multi=True,
        ),
        lexiconinputtemplate, #variable containing the input template defined earlier
        OutputTemplate('ranked', FoLiAXMLFormat, 'Ranked List of Correction Candidates',
            filename='ranked',
            unique=True,
        ),
    ),

    Profile(
        InputTemplate('image', TiffImageFormat, 'Image',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    Profile(
        InputTemplate('PDF', PDFFormat, 'PDF',
           extension='.pdf',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            removeextension='.pdf',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    Profile(
        InputTemplate('DJVU', DjVuFormat, 'DJVU',
           extension='.djvu',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            removeextension='.djvu',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    ]

##COPYPART--END
##FRA--end
##ISL-begin
##COPYPART--END
elif language == 'isl': 
    CUSTOMHTML_INDEX = "<H3><a name=\"documentation\"></a>Icelandic Site</H3><p>This site currently offers a contemporary Icelandic lexicon</p><H3><a name=\"documentation\"></a>@PhilosTEI homepage</H3><a href=\"http://www.axiom.humanities.uva.nl/PhilosTEI.html\" title=\"@PhilosTEI homepage\" id=\"logo\"><img src=\"http://ticclops.uvt.nl/PhilosTEI.jpg\" width=\"30%\" class=\"centeredImage\" background-color= transparent/></a><H3><a name=\"documentation\"></a>TICCLops documentation</H3></h1><p>Users are invited to first take a look at the TICClops User and Demonstrator Documentation, which can be downloaded from <a href=\"http://ticclops.uvt.nl/ticclops_manual.v101.pdf\">the TICCLops website.</a></p>"
##COPYPART--BEGIN
#We put this in a variable because we will use this same input template in TWO profiles.
    lexiconinputtemplate = InputTemplate('lexicon', PlainTextFormat,  'Lexicon',
    StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
    InputSource(id='contempISL', label="Contemporary Icelandic Lexicon",
        path=TICCLDIR + "/data/int/isl/isl.aspell.dict",
        metadata=PlainTextFormat(None, encoding='utf-8',language='isl')
    ),
    filename='lexicon.lst',
    unique=True,
    )

    PROFILES = [
    Profile(
        InputTemplate('textinput', PlainTextFormat, 'Plain-Text Input',
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
            acceptarchive=True,
            extension='.txt',
            multi=True,
        ),
        lexiconinputtemplate,  #variable containing the input template defined earlier
        OutputTemplate('ranked', PlainTextFormat, 'Variant Output',
           SetMetaField('encoding','utf-8'),
           filename='ranked',
           unique=True,
        ),
    ),

    Profile(
        InputTemplate('frqlistinput', PlainTextFormat, 'Frequency List Input',
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
            extension='.tsv',
            unique=True,
        ),
        lexiconinputtemplate,  #variable containing the input template defined earlier
        OutputTemplate('ranked', PlainTextFormat, 'Variant Output',
            SetMetaField('encoding','utf-8'),
            filename='ranked',
            unique=True,
        ),
    ),

    Profile(
        InputTemplate('FoLiAxmlinput', FoLiAXMLFormat, 'FoLiA XML',
            extension='.xml',
            acceptarchive=True,
            multi=True,
        ),
        lexiconinputtemplate, #variable containing the input template defined earlier
        OutputTemplate('ranked', FoLiAXMLFormat, 'Ranked List of Correction Candidates',
            filename='ranked',
            unique=True,
        ),
    ),

    Profile(
        InputTemplate('image', TiffImageFormat, 'Image',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    Profile(
        InputTemplate('PDF', PDFFormat, 'PDF',
           extension='.pdf',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            removeextension='.pdf',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    Profile(
        InputTemplate('DJVU', DjVuFormat, 'DJVU',
           extension='.djvu',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            removeextension='.djvu',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    ]
##COPYPART--END
##ISL-end
else :
    CUSTOMHTML_INDEX = "<H3><a name=\"documentation\"></a>Welcome to the @PhilosTEI Language Independent Site!</H3><p>Links to specific language versions of TICCLops that offer resources for the particular language:</p><p><a href=\"http://ticclops.uvt.nl/nld/\">Dutch @PhilosTEI Tesseract & TICCLops</a><p><a href=\"http://ticclops.uvt.nl/eng/\">English @PhilosTEI Tesseract & TICCLops</a></p><p><a href=\"http://ticclops.uvt.nl/fin/\">Finnish @PhilosTEI Tesseract & TICCLops</a></p><p><a href=\"http://ticclops.uvt.nl/fra/\">French @PhilosTEI Tesseract & TICCLops</a></p></p><p><a href=\"http://ticclops.uvt.nl/deu/\">German @PhilosTEI Tesseract & TICCLops</a></p><p><a href=\"http://ticclops.uvt.nl/deu-frak/\">German (Fraktur) @PhilosTEI Tesseract & TICCLops</a></p><p><a href=\"http://ticclops.uvt.nl/ell/\">Greek (Contemporary) @PhilosTEI Tesseract & TICCLops</a></p><p><a href=\"http://ticclops.uvt.nl/grc/\">Greek (Classical) @PhilosTEI Tesseract & TICCLops</a></p><p><a href=\"http://ticclops.uvt.nl/isl/\">Icelandic @PhilosTEI Tesseract & TICCLops</a></p><p><a href=\"http://ticclops.uvt.nl/ita/\">Italian @PhilosTEI Tesseract & TICCLops</a></p><p><a href=\"http://ticclops.uvt.nl/ita_old/\">Italian (Old) @PhilosTEI Tesseract & TICCLops</a></p><p><a href=\"http://ticclops.uvt.nl/lat/\">Latin @PhilosTEI Tesseract & TICCLops</a></p><p><a href=\"http://ticclops.uvt.nl/pol/\">Polish @PhilosTEI Tesseract & TICCLops</a></p><p><a href=\"http://ticclops.uvt.nl/por/\">Portuguese @PhilosTEI Tesseract & TICCLops</a></p><p><a href=\"http://ticclops.uvt.nl/rus/\">Russian @PhilosTEI Tesseract & TICCLops</a></p></p><p><a href=\"http://ticclops.uvt.nl/spa/\">Spanish @PhilosTEI Tesseract & TICCLops</a></p><p><a href=\"http://ticclops.uvt.nl/spa_old/\">Spanish (Old) @PhilosTEI Tesseract & TICCLops</a></p><p><a href=\"http://ticclops.uvt.nl/swe/\">Swedish @PhilosTEI Tesseract & TICCLops</a></p><H3><a name=\"documentation\"></a>@PhilosTEI homepage</H3><a href=\"http://www.axiom.humanities.uva.nl/PhilosTEI.html\" title=\"@PhilosTEI homepage\" id=\"logo\"><img src=\"http://ticclops.uvt.nl/PhilosTEI.jpg\" width=\"30%\" class=\"centeredImage\" background-color= transparent/></a><H3><a name=\"documentation\"></a>TICCLops documentation</H3><p>Users are invited to first take a look at the TICClops User and Demonstrator Documentation, which can be downloaded from <a href=\"http://ticclops.uvt.nl/ticclops_manual.v101.pdf\">the TICCLops website.</a></p>"
##COPYPART--BEGIN
#We put this in a variable because we will use this same input template in TWO profiles.
    lexiconinputtemplate = InputTemplate('lexicon', PlainTextFormat,  'Lexicon',
    StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
    ChoiceParameter(id='language',name='Language',description='The language this text is in', choices=[('eng','English'),('nld','Dutch'),('fra','French'),('deu','German'),('ita','Italian'),('spa','Spanish')]),

    InputSource(id='contempNLD', label="Contemporary Dutch Lexicon (Aspell)",
        path=TICCLDIR + "/data/int/nld/nld.aspell.dict",
        metadata=PlainTextFormat(None, encoding='utf-8',language='nld')
    ),
    InputSource(id='contempNLD2', label="Contemporary Dutch Lexicon (Compilation)",
        path=TICCLDIR + "/data/int/nld/ARG4.SGDLEX.UTF8.TICCL.v.4.lst",
        metadata=PlainTextFormat(None, encoding='utf-8',language='nld')
    ),
    InputSource(id='histNLD', label="Historical and Contemporary Dutch Lexicon, with names",
        path=TICCLDIR + "/data/int/nld/nuTICCL.OldandINLlexandINLNamesAspell.v2.COL1.tsv",
        metadata=PlainTextFormat(None, encoding='utf-8',language='nld')
    ),
##KALLIOPI LEXICONS DUTCH HERE!!
    InputSource(id='contempDEU', label="Contemporary German Lexicon",
        path=TICCLDIR + "/data/int/deu/deu.aspell.dict",
        metadata=PlainTextFormat(None, encoding='utf-8',language='deu')
    ),
    InputSource(id='historDEU', label="Historical German Lexicon",
        path=TICCLDIR + "/data/int/deu-frak/deu-frak.aspell.dict",
        metadata=PlainTextFormat(None, encoding='utf-8',language='deu')
    ),
    InputSource(id='contempELL', label="Contemporary Greek Lexicon",
        path=TICCLDIR + "/data/int/ell/ell.aspell.dict",
        metadata=PlainTextFormat(None, encoding='utf-8',language='ell')
    ),
    InputSource(id='contempGRC', label="Classical Greek Lexicon",
        path=TICCLDIR + "/data/int/grc/grc.aspell.dict",
        metadata=PlainTextFormat(None, encoding='utf-8',language='ell')
    ),
    InputSource(id='contempSPA', label="Contemporary Spanish Lexicon",
        path=TICCLDIR + "/data/int/spa/spa.aspell.dict",
        metadata=PlainTextFormat(None, encoding='utf-8',language='spa')
    ),
    InputSource(id='contempENG', label="Contemporary English Lexicon",
        path=TICCLDIR + "/data/int/eng/eng.aspell.dict",
        metadata=PlainTextFormat(None, encoding='utf-8',language='eng')
    ),
    InputSource(id='contempFIN', label="Contemporary Finnish Lexicon",
        path=TICCLDIR + "/data/int/fin/fin.aspell.dict",
        metadata=PlainTextFormat(None, encoding='utf-8',language='fin')
    ),
    InputSource(id='contempFRA', label="Contemporary French Lexicon",
        path=TICCLDIR + "/data/int/fra/fra.aspell.dict",
        metadata=PlainTextFormat(None, encoding='utf-8',language='fra')
    ),
    InputSource(id='contempISL', label="Contemporary Icelandic Lexicon",
        path=TICCLDIR + "/data/int/isl/isl.aspell.dict",
        metadata=PlainTextFormat(None, encoding='utf-8',language='isl')
    ),
    InputSource(id='historLAT', label="Historical Latin Lexicon",
        path=TICCLDIR + "/data/int/lat/lat.aspell.dict",
        metadata=PlainTextFormat(None, encoding='utf-8',language='lat')
    ),
    InputSource(id='contempPOL', label="Contemporary Polish Lexicon",
        path=TICCLDIR + "/data/int/pol/pol.aspell.dict",
        metadata=PlainTextFormat(None, encoding='utf-8',language='pol')
    ),
    InputSource(id='contempITA', label="Contemporary Italian Lexicon",
        path=TICCLDIR + "/data/int/ita/ita.aspell.dict",
        metadata=PlainTextFormat(None, encoding='utf-8',language='ita')
    ),
    InputSource(id='contempPOR', label="Contemporary Portuguese Lexicon",
        path=TICCLDIR + "/data/int/por/por.aspell.dict",
        metadata=PlainTextFormat(None, encoding='utf-8',language='por')
    ),
    InputSource(id='contempRUS', label="Contemporary Russian Lexicon",
        path=TICCLDIR + "/data/int/rus/rus.aspell.dict",
        metadata=PlainTextFormat(None, encoding='utf-8',language='rus')
    ),
    InputSource(id='contempSWE', label="Contemporary Swedish Lexicon",
        path=TICCLDIR + "/data/int/swe/swe.aspell.dict",
        metadata=PlainTextFormat(None, encoding='utf-8',language='swe')
    ),
    filename='lexicon.lst',
    unique=True,
    )

    INPUTSOURCES = [
    InputSource(id='dutchnew', label="TEST data: VUDNC Kalliopi Selection",
        path=TICCLDIR + "corpora/OCR/VUDNCtest/",
        metadata=FoLiAXMLFormat(None, encoding='utf-8'),
        inputtemplate='FoLiAxmlinput'
    ),
    InputSource(id='dutchold', label="TEST data: DPO35 Kalliopi Selection",
        path=TICCLDIR + "corpora/OCR/DPO35test/",
        metadata=FoLiAXMLFormat(None, encoding='utf-8'),
        inputtemplate='FoLiAxmlinput'
    ),
    ]
##HERE ABOVE KALLIOPI INPUT FILES VUDNC and DPO35

    PROFILES = [
    Profile(
        InputTemplate('textinput', PlainTextFormat, 'Plain-Text Input',
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
            ChoiceParameter(id='language',name='Language',description='The language this text is in', choices=[('eng','English'),('nld','Dutch'),('fra','French'),('deu','German'),('ita','Italian'),('spa','Spanish')]),
            acceptarchive=True,
            extension='.txt',
            multi=True,
        ),
        lexiconinputtemplate,  #variable containing the input template defined earlier
        OutputTemplate('ranked', PlainTextFormat, 'Variant Output',
           SetMetaField('encoding','utf-8'),
           filename='ranked',
           unique=True,
        ),
    ),

    Profile(
        InputTemplate('frqlistinput', PlainTextFormat, 'Frequency List Input',
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
            ChoiceParameter(id='language',name='Language',description='The language this text is in', choices=[('eng','English'),('nld','Dutch'),('fra','French'),('deu','German'),('ita','Italian'),('spa','Spanish')]),
            #acceptarchive=True,
            extension='.tsv',
            unique=True,
        ),
        lexiconinputtemplate,  #variable containing the input template defined earlier
        OutputTemplate('ranked', PlainTextFormat, 'Variant Output',
            SetMetaField('encoding','utf-8'),
            filename='ranked',
            unique=True,
        ),
    ),

    Profile(
        InputTemplate('FoLiAxmlinput', FoLiAXMLFormat, 'FoLiA XML',
            extension='.xml',
            acceptarchive=True,
            multi=True,
        ),
        lexiconinputtemplate, #variable containing the input template defined earlier
        OutputTemplate('ranked', FoLiAXMLFormat, 'Ranked List of Correction Candidates',
            filename='ranked',
            unique=True,
        ),
    ),

    Profile(
        InputTemplate('image', TiffImageFormat, 'Image',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    Profile(
        InputTemplate('PDF', PDFFormat, 'PDF',
           extension='.pdf',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            removeextension='.pdf',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    Profile(
        InputTemplate('DJVU', DjVuFormat, 'DJVU',
           extension='.djvu',
           multi=True,
        ),
        OutputTemplate('folia', FoLiAXMLFormat, 'resultaat',
            removeextension='.djvu',
            extension='.folia.xml',
            multi=True,
        ),
        ),
    ]

#The system command. It is recommended you set this to small wrapper
#script around your actual system. Full shell syntax is supported. Using
#absolute paths is preferred. The current working directory will be
#set to the project directory.
#
#You can make use of the following special variables,
#which will be automatically set by CLAM:
#     $INPUTDIRECTORY  - The directory where input files are uploaded.
#     $OUTPUTDIRECTORY - The directory where the system should output
#                        its output files.
#     $STATUSFILE      - Filename of the .status file where the system
#                        should output status messages.
#     $CONFFILE        - Filename of the clam.xml file describing the
#                        system and chosen configuration.
#     $USERNAME        - The username of the currently logged in user
#                        (set to "anonymous" if there is none)
#     $PARAMETERS      - List of chosen parameters, using the specified flags
#

COMMAND = TICCLDIR +  "/ticclops/ticclopswrapper.pl $PARAMETERS " + TICCLDIR + " $INPUTDIRECTORY $OUTPUTDIRECTORY $STATUSFILE $PROJECT"

#The parameters are subdivided into several groups. In the form of a list of (groupname, parameters) tuples. The parameters are a list of instances from common/parameters.py
PARAMETERS = [
    ('Language Selection', [
        ChoiceParameter('lang','Language?','Which language do you want to work with?', choices=[('eng','English'),('nld','Dutch'),('fin','Finnish'),('fra','French'),('deu','German'),('deu-frak','German Fraktur'),('ell','Greek (Modern)'),('grc','Greek (Classical)'),('isl','Icelandic'),('ita','Italian'),('lat','Latin'),('pol','Polish'),('por','Portuguese'),('rus','Russian'),('spa','Spanish'),('swe','Swedish')], nospace=True,paramflag='-t')
    ]),
    ('Input Selection', [
        ChoiceParameter('input','Input Type?','Which input types do you have?', choices=[('TXT','Plain texts'),('FOLIA','Texts in FoLiA xml format'),('TIFF','Images in TIFF format'),('IM','Images in non-TIFF format'),('TSV','Tab-separated Frequency List'),('PDF','Images in PDF format'),('DJVU','Images in DJVU format')], nospace=True,paramflag='-b')
    ]),
    ('N-best Ranking', [
            ChoiceParameter('top','How many ranked variants?','Return N best-first ranked variants',choices=[('3','Up to three N-best ranked'),('1','First-best Only'),('2','Up to two N-best ranked'),('5','Up to five N-best ranked'),('10','Up to ten N-best ranked'),('20','Up to twenty N-best ranked')], nospace=True,paramflag='-r')
    ]),
    ('Edit/Levenshtein Distance', [
            ChoiceParameter('ld','How many edits?','Search a distance of N characters for variants',choices=[('2','Up to two edits'),('1','Only one edit')], nospace=True, paramflag='-L')
    ]),
    ('Focus Word Selection', [
        IntegerParameter('minlength','Minimum Word Length','Integer between zero and one hundred',default=5,minvalue=0, maxvalue=100, paramflag='-x'),
        IntegerParameter('maxlength','Maximum Word Length','Integer between zero and one hundred',default=100,minvalue=0, maxvalue=100, paramflag='-y'),
    ]),
]
