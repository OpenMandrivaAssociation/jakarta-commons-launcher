%define base_name       launcher
%define short_name      commons-%{base_name}
%define name            jakarta-%{short_name}
%define section         free
%define gcj_support     1

Name:           %{name}
Version:        1.1
Release:        %mkrel 1.10
Epoch:          0
Summary:        Cross-platform Java application launcher
License:        Apache License
Group:          Development/Java
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
#Vendor:         JPackage Project
#Distribution:   JPackage
URL:            http://jakarta.apache.org/commons/launcher/
Source0:        http://archive.apache.org/dist/jakarta/commons/launcher/source/%{short_name}-%{version}-src.tar.bz2
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
Buildarch:      noarch
%endif
BuildRequires:  ant
BuildRequires:  java-rpmbuild >= 0:1.5.30

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
Summary:        Javadoc for %{name}
Group:          Development/Java
BuildRequires:  java-javadoc

%description    javadoc
Javadoc for %{name}.


%prep
%setup -q -n %{short_name}


%build
mkdir lib
%ant \
  -Dbuild.sysclasspath=only \
  -Dfinal.name=%{short_name} \
  -Dj2se.javadoc=%{_javadocdir}/java \
  -Dsrcdir=. \
  jar javadoc


%install
rm -rf $RPM_BUILD_ROOT

# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p dist/bin/%{short_name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed "s|jakarta-||g"`; done)
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

# fix end-of-line
%{__perl} -pi -e 's/\r$//g' *.txt

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

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
%defattr(0644,root,root,0755)
%doc LICENSE.txt
%{_javadir}/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%ghost %doc %{_javadocdir}/%{name}




%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 0:1.1-1.10mdv2011.0
+ Revision: 665804
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.1-1.9mdv2011.0
+ Revision: 606057
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.1-1.8mdv2010.1
+ Revision: 522980
- rebuilt for 2010.1

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 0:1.1-1.7mdv2010.0
+ Revision: 425439
- rebuild

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 0:1.1-1.6mdv2009.1
+ Revision: 351286
- rebuild

* Thu Feb 14 2008 Thierry Vignaud <tv@mandriva.org> 0:1.1-1.5mdv2009.0
+ Revision: 167946
- fix no-buildroot-tag
- kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:1.1-1.5mdv2008.1
+ Revision: 120914
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:1.1-1.4mdv2008.0
+ Revision: 87412
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Sat Sep 08 2007 Pascal Terjan <pterjan@mandriva.org> 0:1.1-1.3mdv2008.0
+ Revision: 82681
- update to new version


* Thu Mar 15 2007 Christiaan Welvaart <spturtle@mandriva.org> 1.1-1.2mdv2007.1
+ Revision: 143923
- rebuild for 2007.1
- Import jakarta-commons-launcher

* Fri Aug 04 2006 David Walluck <walluck@mandriva.org> 0:1.1-1.1mdv2007.0
- no html

* Sun Jun 04 2006 David Walluck <walluck@mandriva.org> 0:1.1-1mdv2007.0
- rebuild for libgcj.so.7
- aot-compile

* Sun May 22 2005 David Walluck <walluck@mandriva.org> 0:0.9-3.1mdk
- release

* Tue Aug 24 2004 Randy Watler <rwatler at finali.com> - 0:0.9-3jpp
- Rebuild with ant-1.6.2

* Wed Jun 02 2004 Randy Watler <rwatler at finali.com> - 0:0.9-2jpp
- Upgrade to Ant 1.6.X

