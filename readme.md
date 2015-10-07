# Tanuki - creating dynamic forms

## Install

Currently in only can be installed from the git repository. A package on PYPI
will be available as soon as possible.

`pip install -e git+https://github.com/jibaku/tanuki.git#egg=tanuki`

# Documentation

Read the [documentation](http://tanuki.readthedocs.org/en/latest/)

## About

Using the admin interface you can create surveys, add questions, give questions
categories, and mark them as required or not. the front-end survey view then
automatically populates based on the questions that have been defined in the
admin interface.

Submitted responses can also be viewed via the admin backend and signal is sended
when a survey is completed, to allow the use of data in another app.

## Credits 

Some inspiration came from olders app ([django-survey](https://github.com/flynnguy/django-survey) by *flynnguy* and [django-survey](https://github.com/jessykate/django-survey) by jessykate) app, but this app
uses a different model architecture and different mechanism for dynamic form
generation. 

## License

this code is licensed under the [affero general public license](http://www.gnu.org/licenses/agpl-3.0.html). 

The GNU General Public License permits making a modified version and letting the public access it on a server without ever releasing its source code to the public... The GNU Affero General Public License is designed specifically to ensure that, in such cases, the modified source code becomes available to the community. It requires the operator of a network server to provide the source code of the modified version running there to the users of that server. 

## Code status

[![Build Status](https://travis-ci.org/jibaku/tanuki.svg?branch=master)](https://travis-ci.org/jibaku/tanuki)
[![codecov.io](https://codecov.io/github/jibaku/tanuki/coverage.svg?branch=master)](https://codecov.io/github/jibaku/tanuki?branch=master)
