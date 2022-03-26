#
# Conditional build:
%bcond_with	doc	# don't build doc
%bcond_with	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module		pykka
%define		egg_name	Pykka
Summary:	Python library that provides concurrency using actor model
Name:		python-%{module}
Version:	1.2.1
Release:	5
License:	Apache v2.0
Group:		Libraries/Python
Source0:	https://github.com/jodal/pykka/archive/v%{version}/%{module}-%{version}.tar.gz
# Source0-md5:	0148bd046e0c265b834ffd7c454761e4
URL:		http://www.pykka.org/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-gevent
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules
BuildRequires:	python3-setuptools
%endif
%if %{with doc}
BuildRequires:	sphinx-pdg
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The goal of Pykka is to provide easy to use concurrency abstractions
for Python by using the actor model.

Pykka provides an actor API with two different implementations:

 - ThreadingActor is built on the Python Standard Library's threading
   and Queue modules, and has no dependencies outside Python itself. It
   plays well together with non-actor threads.
 - GeventActor is built on the gevent library. gevent is a
   coroutine-based Python networking library that uses greenlet to
   provide a high-level synchronous API on top of libevent event loop. It
   is generally faster, but doesn't like playing with other threads.

Much of the naming in Pykka is inspired by the Akka project which
implements actors on the JVM. Though, Pykka does not aim to be a
Python port of Akka.

This package provides Pykka's Python 2 libraries.

%package -n python3-pykka
Summary:	Python library that provides concurrency using actor model
Group:		Libraries/Python

%description -n python3-%{module}
The goal of Pykka is to provide easy to use concurrency abstractions
for Python by using the actor model.

Pykka for Python 3 provides an actor API with one implementation:

 - ThreadingActor is built on the Python Standard Library's threading
   and Queue modules, and has no dependencies outside Python itself. It
   plays well together with non-actor threads.

Much of the naming in Pykka is inspired by the Akka project which
implements actors on the JVM. Though, Pykka does not aim to be a
Python port of Akka.

This package provides Pykka's Python 3 libraries.

%package docs
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	devhelp

%description docs
This package provides the documentation for %{name}, e.g. the API as
devhelp docs, and examples.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
%{__make} -C docs devhelp
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python2}
%py_install
%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%if %{with doc}
install -d $RPM_BUILD_ROOT%{_datarootdir}/devhelp/Pykka
cp -a docs/_build/devhelp $RPM_BUILD_ROOT%{_datarootdir}/devhelp/Pykka
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.rst
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif

%if %{with python2}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc README.rst
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif

%if %{with doc}
%files docs
%defattr(644,root,root,755)
%doc examples/
%{_datarootdir}/devhelp/Pykka
%endif
