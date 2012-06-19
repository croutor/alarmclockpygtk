PGRM_NAME=alarmclockpygtk
VERSION_MAJOR=0
VERSION_MINOR=2

tag:
	@echo "svn cp -m \"creating tag ${PGRM_NAME}-${VERSION_MAJOR}.${VERSION_MINOR}\"-rHEAD https://alarmclockpygtk.googlecode.com/svn/trunk https://alarmclockpygtk.googlecode.com/svn/tags/${PGRM_NAME}-${VERSION_MAJOR}.${VERSION_MINOR}"

