[![Build Status](https://travis-ci.com/hasii2011/PyUt.svg?branch=master)](https://travis-ci.com/hasii2011/PyUt)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![macOS](https://svgshare.com/i/ZjP.svg)](https://svgshare.com/i/ZjP.svg)
<img width="34" height="17" src="./src/org/pyut/resources/img/gplv3-with-text-136x68.png"/> 

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

This project is intended to be used by [Pyut Plugin](https://github.com/hasii2011/pyutplugincore) developers to convert [Pyut](https://github.com/hasii2011/PyUt) XML files to the [Ogl Model](https://github.com/hasii2011/ogl) classes.  These model classes can then be used by the Pyut UI to display as UML Diagrams.

------

Use as follows:

```python
from untanglepyut.UnTangler import Document
from untanglepyut.UnTangler import UnTangler
from untanglepyut.UnTangler import UntangledOglClasses
from untanglepyut.UnTangler import UntangledOglLinks

untangler: UnTangler = UnTangler(fqFileName='MultiDocumentProject.xml')


document:   Document            = untangler.documents['Diagram-1']
oglClasses: UntangledOglClasses = document.oglClasses
oglLinks:   UntangledOglLinks   = document.oglLinks

```



The following is the UML diagram for the Pyut Untangler

![UntanglePyut](https://github.com/hasii2011/untanglepyut/blob/master/docs/UntanglePyut.png)



------


![Humberto's Modified Logo](https://raw.githubusercontent.com/wiki/hasii2011/gittodoistclone/images/SillyGitHub.png)

I am concerned about GitHub's Copilot project



I urge you to read about the
[Give up GitHub](https://GiveUpGitHub.org) campaign from
[the Software Freedom Conservancy](https://sfconservancy.org).

While I do not advocate for all the issues listed there I do not like that
a company like Microsoft may profit from open source projects.

I continue to use GitHub because it offers the services I need for free.  But, I continue
to monitor their terms of service.

Any use of this project's code by GitHub Copilot, past or present, is done
without my permission.  I do not consent to GitHub's use of this project's
code in Copilot.

A repository owner may opt out of Copilot by changing Settings --> GitHub Copilot.

I have done so.
