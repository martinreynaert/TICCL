# TICCL and TICCLops #

Text-induced Corpus Clean-up is the stand-alone command line version of the spelling correction and OCR post-correction system we have been developing since about 2008.  

TICCLops is TICCL as an 'online processing system'. It is a fully
fledged web application and web service due to [CLAM]
(http://proycon.github.io/clam/), developed  by Maarten van Gompel.

The current repository mainly houses the wrapper scripts, variably Perl and Python scripts.  

The main TICCL modules were developed by Ko van der Sloot in C++ in
various projects over the past years. These are available from:
[TICCLtools at LanguageMachines] (https://github.com/LanguageMachines/ticcltools)  

We have prepared TICCL for work in many languages, mainly on the basis of available open source lexicons due to Aspell. The language specific files are available here:  

[All languages]
(http://ticclops.uvt.nl/TICCL.languagefiles.ALLavailable.20160421.tar.gz)  
[Dutch] (http://ticclops.uvt.nl/TICCL.languagefiles.nld.20160421.tar.gz)  
[English] (http://ticclops.uvt.nl/TICCL.languagefiles.eng.20160421.tar.gz)  
[Finnish] (http://ticclops.uvt.nl/TICCL.languagefiles.fin.20160421.tar.gz)  
[French] (http://ticclops.uvt.nl/TICCL.languagefiles.fra.20160421.tar.gz)  
[Friesian] (http://ticclops.uvt.nl/TICCL.languagefiles.fry.20160421.tar.gz)  
[German]
(http://ticclops.uvt.nl/TICCL.languagefiles.deu.20160421.tar.gz)  
[German Fraktur]
(http://ticclops.uvt.nl/TICCL.languagefiles.deu-frak.20160421.tar.gz)  
[Greek (antique)] (http://ticclops.uvt.nl/TICCL.languagefiles.grc.20160421.tar.gz)  
[Greek (modern)] (http://ticclops.uvt.nl/TICCL.languagefiles.ell.20160421.tar.gz)  
[Icelandic] (http://ticclops.uvt.nl/TICCL.languagefiles.isl.20160421.tar.gz)  
[Italian] (http://ticclops.uvt.nl/TICCL.languagefiles.ita.20160421.tar.gz)  
[Latin] (http://ticclops.uvt.nl/TICCL.languagefiles.lat.20160421.tar.gz)  
[Polish] (http://ticclops.uvt.nl/TICCL.languagefiles.pol.20160421.tar.gz)  
[Portuguese] (http://ticclops.uvt.nl/TICCL.languagefiles.por.20160421.tar.gz)  
[Romanian] (http://ticclops.uvt.nl/TICCL.languagefiles.ron.20160421.tar.gz)  
[Russian] (http://ticclops.uvt.nl/TICCL.languagefiles.rus.20160421.tar.gz)  
[Spanish] (http://ticclops.uvt.nl/TICCL.languagefiles.spa.20160421.tar.gz)  
[Swedish]
(http://ticclops.uvt.nl/TICCL.languagefiles.swe.20160421.tar.gz)  

Unpack in your main TICCL directory. A subdirectory data/int/ will be
created to house the required files for the specific language(s).  

We also provide some sample corpora. These come with TICCLops for demonstration and test purposes. These are available here:  

[All demo and test sets]
(http://ticclops.uvt.nl/TICCL.SampleCorpora.20160504.ALL.tar.gz)  
[DjVu format]
(http://ticclops.uvt.nl/TICCL.SampleCorpora.DJVU.20160504.tar.gz)  
[FoLiA XML format]
(http://ticclops.uvt.nl/TICCL.SampleCorpora.FOLIA.20160504.tar.gz)  
[OCR] (http://ticclops.uvt.nl/TICCL.SampleCorpora.OCR.20160504.tar.gz)  
[PDF with embedded page images] (http://ticclops.uvt.nl/TICCL.SampleCorpora.PDF.20160504.tar.gz)  
[Tab-separated list] (http://ticclops.uvt.nl/TICCL.SampleCorpora.TSV.20160504.tar.gz)  
[Text files] (http://ticclops.uvt.nl/TICCL.SampleCorpora.TXT.20160504.tar.gz)  
[TIFF image files]
(http://ticclops.uvt.nl/TICCL.SampleCorpora.TIFF.20160504.tar.gz)

## Running TICCL from the command line  ##

Use ``TICCLops.PICCL.pl`` to run TICCL from the command line.  

Examples of input parameters with some further documentation are to be found in file: ``TICCL.Black.config`` .

Edit file ``TICCL.Template.config`` in order to specify the specific settings and file locations for your own installation.

You can then start TICCL by running the following command: ``$
perl TICCLops.PICCL.pl TICCL.Template.config``  

## TICCLops available online as demonstrator system ##

We have a demonstrator system online in an official Dutch CLARIN Center at
[TICCLopsCLAM] (http://ticclops.clarin.inl.nl/ticclops/). An interface
developed specifically for philosopher-users is available here:
[TICCLopsPhilosTEI] (http://ticclops.clarin.inl.nl/ticclops/).

In fact, both systems are geared at letting you upload scanned images of
book pages, to have them automatically converted into electronic text
by way of the Tesseract OCR engine and then to have them
OCR post-corrected by TICCL. For e.g. PDF files for book chapters, you
will receive back a full, reconstituted book in both FoLiA and TEI
formats. Please take into account that this process requires, well,
the time required.
