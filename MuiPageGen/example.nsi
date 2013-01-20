; vim:foldmethod=marker:ts=2:sw=2:nowrap

!include MUI.nsh
!include components.nsh

OutFile "example.exe"

Page custom ComponentsCustomPage
!insertmacro MUI_PAGE_INSTFILES

!insertmacro MUI_UNPAGE_WELCOME

!insertmacro MUI_LANGUAGE "English"
!insertmacro MUI_LANGUAGE "Polish"

!insertmacro MUI_RESERVEFILE_LANGDLL

Section "Install"
SectionEnd

