#!/bin/bash

set -e

echo ':: Building package... '$(pwd)
sed -i s/-dev/".$(date +%Y%m%d.%H%M)"/g pyproject.toml


PACKAGE=$(poetry version | awk {'print $1'})
VERSION=$(poetry version | awk {'print $2'})

poetry config repositories.wlt_nexus $NEXUS_URL
poetry config http-basic.wlt_nexus $NEXUS_USER $NEXUS_PW
echo "Repository gitlab configured ..."

echo ':: Setting version... '$VERSION
poetry version $VERSION
if [ ! -f poetry.lock ]; then
    echo "No lock file found, rebuilding"
    poetry lock
else
    echo "Running poetry update"
    poetry update
fi

poetry update
#poetry add "urllib3==1.26.15" requests
poetry install
poetry publish --build --repository wlt_nexus
echo "Build/publish done ..."


echo ":: Current version of ${PACKAGE} is ${VERSION}."
