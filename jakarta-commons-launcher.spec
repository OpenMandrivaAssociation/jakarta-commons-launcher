%define base_name	launcher
%define short_name	commons-%{base_name}
%define section		free
%define gcj_support	1

Summary:	Cross-platform Java application launcher
Name:		jakarta-%{short_name}
Version:	1.1
Release:	5
License:	Apache License
Group:		Development/Java
Url:		http://jakarta.apache.org/commons/launcher/
Source0:	http://archive.apache.org/dist/jakarta/commons/launcher/source/%{short_name}-%{version}-src.tar.bz2
%if !%{gcj_support}
Buildarch:	noarch
%else
BuildRequires:	java-gcj-compat-devel
%endif
BuildRequires:	ant
BuildRequires:	java-rpmbuild >= 0:1.5.30

%description
Commons-launcher eliminates the need for a batch or shell script to 
launch a Java class. Some situations where elimination of a batch or 
shell script may be desirable are:

* You want to avoid having to determining where certain application 
  paths are e.g. your application's home directory, etc. Determining this 
  dynamically in a Windows batch scripts is very tricky on some versions 
  of Windows or when softlinks are used on Unix platforms.
* You want to avoid having to handle native file and path separators or 
  native path quoting issues.
* You need to enforce certain system properties e.g. java.endorsed.dirs 
  when running with JDK 1.4.
* You want to allow users to pass in custom JVM arguments or system 
  properties without having to parse and reorder arguments in your script. 
  This can be tricky and/or messy in batch and shell scripts.
* You want to bootstrap system properties from a configuration file 
  instead hard-coding them in your batch and shell scripts.
* You want to provide localized error messages which is very tricky to 
  do in batch and shell scripts.

%package        javadoc
Summary:	Javadoc for %{name}
Group:		Development/Java
BuildRequires:	java-javadoc

%description    javadoc
Javadoc for %{name}.

%prep
%setup -qn %{short_name}

%build
mkdir lib
%ant \
	-Dbuild.sysclasspath=only \
	-Dfinal.name=%{short_name} \
	-Dj2se.javadoc=%{_javadocdir}/java \
	-Dsrcdir=. \
	jar javadoc

%install

# jars
mkdir -p %{buildroot}%{_javadir}
cp -p dist/bin/%{short_name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed "s|jakarta-||g"`; done)
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# javadoc
mkdir -p %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr dist/docs/api/* %{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name} # ghost symlink

# fix end-of-line
sed -i -e 's/\r$//g' *.txt

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%files
%doc LICENSE.txt
%{_javadir}/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%doc %{_javadocdir}/%{name}-%{version}
%ghost %doc %{_javadocdir}/%{name}

