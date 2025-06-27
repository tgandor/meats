$pathogen = "$HOME\.vim\autoload\pathogen.vim"
$autoloadDir = "$HOME\.vim\autoload"
$bundleDir = "$HOME\.vim\bundle"
$vimrc = "$HOME\.vimrc"

# Tworzenie katalogów
New-Item -ItemType Directory -Force -Path $autoloadDir, $bundleDir | Out-Null

# Pobieranie pathogen.vim, jeśli nie istnieje
if (Test-Path $pathogen) {
    Write-Host "$pathogen already present"
} else {
    Invoke-WebRequest -Uri "https://tpo.pe/pathogen.vim" -OutFile $pathogen
}

# Klonowanie vim-renamer, jeśli nie istnieje
$pluginDir = Join-Path $bundleDir "vim-renamer"
if (Test-Path $pluginDir) {
    Write-Host "vim-renamer already in $bundleDir"
} else {
    git clone https://github.com/qpkorr/vim-renamer.git $pluginDir
}

# Dodanie pathogen do .vimrc, jeśli nie istnieje
if (Select-String -Path $vimrc -Pattern "pathogen" -Quiet) {
    Write-Host "Pathogen already in .vimrc"
} else {
    Add-Content -Path $vimrc -Value "execute pathogen#infect()"
}
