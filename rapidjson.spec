%define debug_package %nil

%define oname RapidJSON
%define lname %(echo %oname | tr [:upper:] [:lower:])

%define devname %mklibname %{name} -d

Summary:	A fast JSON parser/generator for C++ with both SAX/DOM style API
Name:		%{lname}
Version:	1.1.0
Release:	1
License:	MIT
Group:		System/Libraries
URL:		https://rapidjson.org/
Source0:	https://github.com/miloyip/%{oname}/archive/v%{version}/%{name}-%{version}.tar.gz
Patch0:		%{name}-1.1.0-test-CMakeLists.patch

BuildRequires:	cmake
BuildRequires:	gtest-devel
BuildRequires:	valgrind

%description
RapidJSON is a JSON parser and generator for C++. It was inspired
by RapidXml.

 *  RapidJSON is small but complete. It supports both SAX and DOM
    style API. The SAX parser is only a half thousand lines of code.

 *  RapidJSON is fast. Its performance can be comparable to strlen().
    It also optionally supports SSE2/SSE4.2 for acceleration.

 *  RapidJSON is self-contained and header-only. It does not depend
    on external libraries such as BOOST. It even does not depend on STL.

 *  RapidJSON is memory-friendly. Each JSON value occupies exactly 16/20
    bytes for most 32/64-bit machines (excluding text string). By default
    it uses a fast memory allocator, and the parser allocates memory
    compactly during parsing.

 *  RapidJSON is Unicode-friendly. It supports UTF-8, UTF-16, UTF-32
    (LE & BE), and their detection, validation and transcoding internally.
    For example, you can read a UTF-8 file and let RapidJSON transcode the
    JSON strings into UTF-16 in the DOM. It also supports surrogates and
    "\u0000" (null character).

JSON(JavaScript Object Notation) is a light-weight data exchange format.
RapidJSON should be in fully compliance with RFC7159/ECMA-404.

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Headers, libraries and docs for the %{oname} library
Group:		Development/C++

Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
RapidJSON is a JSON parser and generator for C++. It was inspired
by RapidXml.

 *  RapidJSON is small but complete. It supports both SAX and DOM
    style API. The SAX parser is only a half thousand lines of code.

 *  RapidJSON is fast. Its performance can be comparable to strlen().
    It also optionally supports SSE2/SSE4.2 for acceleration.

 *  RapidJSON is self-contained and header-only. It does not depend
    on external libraries such as BOOST. It even does not depend on STL.

 *  RapidJSON is memory-friendly. Each JSON value occupies exactly 16/20
    bytes for most 32/64-bit machines (excluding text string). By default
    it uses a fast memory allocator, and the parser allocates memory
    compactly during parsing.

 *  RapidJSON is Unicode-friendly. It supports UTF-8, UTF-16, UTF-32
    (LE & BE), and their detection, validation and transcoding internally.
    For example, you can read a UTF-8 file and let RapidJSON transcode the
    JSON strings into UTF-16 in the DOM. It also supports surrogates and
    "\u0000" (null character).

JSON(JavaScript Object Notation) is a light-weight data exchange format.
RapidJSON should be in fully compliance with RFC7159/ECMA-404.

This package contains the include files and the other resources for C++
devlopper.

%files -n %{devname}
%{_includedir}/%{name}
%{_libdir}/cmake
%{_libdir}/pkgconfig/%{oname}.pc
%doc %{_docdir}/%{oname}
%doc readme.md
%doc CHANGELOG.md
%doc license.txt

#----------------------------------------------------------------------------

%prep
%setup -q

# Apply all patches
%patch0 -p1 -b .orig

%build
%cmake \
	-DRAPIDJSON_BUILD:BOOL=ON \
	-DRAPIDJSON_BUILD_DOC:BOOL=ON \
	-DRAPIDJSON_BUILD_EXAMPLES:BOOL=ON \
	-DRAPIDJSON_BUILD_TESTS:BOOL=ON \
	-DRAPIDJSON_BUILD_THIRDPARTY_GTEST:BOOL=ON \
	-DGTESTSRC_FOUND=TRUE \
	-DGTEST_SOURCE_DIR=. \
	-DRAPIDJSON_BUILD_CXX11:BOOL=ON \
	-DRAPIDJSON_HAS_STDSTRING:BOOL=ON \
	%{nil}
%make

%install
%makeinstall_std -C build

%check
pushd build
ctest -E ".*valgrind.*" --force-new-ctest-process -V .
popd

