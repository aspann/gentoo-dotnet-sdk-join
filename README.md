# Dotnet SDK Join (for gentoo linux)

This small tool is used to amalgamate dotnet SDKs for gentoo.

## History

Historical source (idea):

```bash
DOTNET_BASE="/opt/dotnet*-sdk*"

function dotnet_ln() {
    local dir="${DOTNET_BASE}/${1}/*"
    for f in ${DOTNET_BASE}; do
        local v=$(basename $(find ${f}/${1}/* -maxdepth 0 -type d))
        for s in $(find ${dir} -maxdepth 0 -type d); do
            if [[ ${v%%.*} > $(t=${s##*/} echo ${t%%.*}) ]]; then
                echo "linking: ${f}/${1}/${s##*/}.."
                ln -s "${s}" "${f}/${1}/${s##*/}"
            fi
        done

        ## broken symlinks (uninstall)
        for bl in $(find ${dir} -xtype l); do
            echo "removing: ${bl}.."
            rm ${bl}
        done
    done
}

# iterate and symlink for the following runtimes
dotnet_ln shared/Microsoft.AspNetCore.App
dotnet_ln shared/Microsoft.NETCore.App

# iterate and symlink SDKs
dotnet_ln sdk
```

## Development (rework)

Development thingies.. :)

### stash: do not use any of those! (be warned)

```bash
# equivalent to(ebuild): distutils_enable_tests pytest
pytest -vv -ra -l -Wdefault --color=yes
```

```bash
flit build
pip install -e . --break-system-packages
${HOME}/.local/bin/gentoo-dotnet-sdk-join

```

the above might be destructive, you have been warned twice!
